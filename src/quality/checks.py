"""Deterministic issue detectors, not truth labels or greenwashing verdicts."""
import ast
from collections import defaultdict
from decimal import Decimal, InvalidOperation
import re

from src.quality.dictionary import identify_metric, load_dictionary


def record_checks(snapshot):
    fields=snapshot['fields']
    key=identify_metric(snapshot.get('label') or '')
    findings=[]
    def flag(code,message):
        findings.append({'record_id':snapshot['record_id'],'code':code,'message':message,'status':'NeedsReview'})
    if snapshot.get('physical_page') is None or not snapshot.get('anchor'):
        flag('SOURCE_LOCATION_MISSING','Missing source page/anchor; cannot confirm this record from extraction alone.')
    if key:
        allowed=load_dictionary()['local_metrics'][key]['units']
        if fields.get('unit') and fields['unit'] not in allowed:
            flag('METRIC_UNIT_REVIEW','Observed unit is not the local metric base unit. Check scale/conversion and metric mapping; do not auto-reject.')
    if key=='employee_headcount_at_date' and fields.get('value') is not None:
        try:
            value=Decimal(str(fields['value']))
            if value<0 or value!=value.to_integral_value():
                flag('HEADCOUNT_NON_INTEGER_OR_NEGATIVE','Headcount candidate is negative or non-integer; check OCR/decimal convention.')
        except InvalidOperation:
            flag('NUMERIC_VALUE_UNRESOLVED','Numeric candidate is not parseable.')
    if fields.get('observation_year') is None:
        flag('OBSERVATION_YEAR_UNKNOWN','Report year is not a substitute for observation year.')
    return findings


def _sum_expression(expression,values):
    # Statement formulas use item codes, not constants, and only +/−/parentheses.
    if not re.fullmatch(r'[\d+\-()\s]+',expression):
        raise ValueError('Unsupported formula.')
    tree=ast.parse(re.sub(r'\d+',lambda m:'code_'+m[0],expression),mode='eval')
    def walk(node):
        if isinstance(node,ast.Expression): return walk(node.body)
        if isinstance(node,ast.Name): return values[node.id[5:]]
        if isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub)):
            return walk(node.left)+walk(node.right) if isinstance(node.op,ast.Add) else walk(node.left)-walk(node.right)
        raise ValueError('Unsupported formula AST.')
    return walk(tree)


def financial_formula_checks(native):
    groups=defaultdict(list)
    for r in native.get('records',[]):
        p=r.get('payload',{})
        if r['record_type']!='measurement' or not re.fullmatch(r'\d{2,3}',(p.get('item_code_raw') or '').strip()):
            continue
        if p.get('parsed_value') is None or not p.get('unit') or not p.get('statement_scope') or not p.get('table_anchor_id') or p.get('column_index') is None or not (r.get('content_period') or {}).get('year'):
            continue
        key=(p.get('table_anchor_id'),p.get('column_index'),r['content_period']['year'],p['unit'],p.get('scale'),p['statement_scope'])
        groups[key].append(r)
    findings=[]
    evaluated=skipped=0
    for group,rows in groups.items():
        by_code=defaultdict(list)
        for r in rows: by_code[r['payload']['item_code_raw'].strip()].append(r)
        values={code:Decimal(str(rs[0]['payload']['parsed_value'])) for code,rs in by_code.items() if len(rs)==1}
        for r in rows:
            formula=re.search(r'\((\d{2,3})\s*=\s*([\d+\-()\s]+)\)',r['payload'].get('row_label_raw') or '')
            if not formula or formula[1]!=r['payload']['item_code_raw'].strip(): continue
            needed=set(re.findall(r'\d+',formula[2]))
            if not needed <= values.keys() or formula[1] not in values:
                skipped+=1
                continue
            try:
                expected=_sum_expression(formula[2],values)
            except (ValueError,SyntaxError,KeyError):
                skipped+=1
                continue
            evaluated+=1
            actual=values[formula[1]]
            if actual!=expected:
                findings.append({'code':'FINANCIAL_FORMULA_RESIDUAL','record_id':r['record_id'],'status':'NeedsReview',
                                 'formula':formula[0],'actual':str(actual),'expected_from_components':str(expected),
                                 'residual':str(actual-expected),'scope':list(group),
                                 'component_record_ids':[by_code[c][0]['record_id'] for c in sorted(needed)],
                                 'note':'Check source transcription, rounding, code/year/column/unit and statement scope. This is not Contradicted.'})
    return {'formulas_evaluated':evaluated,'formulas_skipped_incomplete':skipped,'findings':findings,
            'limits':'Only explicit same-table, same-column, same-year, same-unit/scale/scope formulas with unique codes are evaluated.'}
