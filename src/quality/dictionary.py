"""Versioned dictionary entry point; legacy ESG config remains an explicit import."""
from hashlib import sha256
from pathlib import Path
from functools import lru_cache
import re
import yaml

from src.extraction.financial_context_v2 import normalized

ROOT=Path(__file__).resolve().parents[2]


@lru_cache(maxsize=4)
def load_dictionary(root=ROOT):
    root=Path(root).resolve()
    path=root/'config/metric_dictionary.yml'
    data=yaml.safe_load(path.read_text(encoding='utf-8'))
    legacy=(root/data['legacy_esg_source']).resolve()
    if not legacy.is_relative_to(root):
        raise ValueError('Unsafe dictionary import.')
    legacy_data=yaml.safe_load(legacy.read_text(encoding='utf-8'))
    for key,item in data['local_metrics'].items():
        if not item.get('definition') or not item.get('topic') or not item.get('units'):
            raise ValueError('Incomplete metric: '+key)
        re.compile(item['pattern'])
        if item.get('exclude'):
            re.compile(item['exclude'])
        item.setdefault('source_references',[])
        item['status']='pending_expert_validation'
    data['legacy_esg_metrics']=legacy_data['metrics']
    data['sha256']=sha256(path.read_bytes()+legacy.read_bytes()).hexdigest()
    return data


def identify_metric(label, dictionary=None):
    dictionary=dictionary or load_dictionary()
    text=normalized(label)
    matches=[key for key,item in dictionary['local_metrics'].items() if re.search(item['pattern'],text) and
             not (item.get('exclude') and re.search(item['exclude'],text))]
    return matches[0] if len(matches)==1 else None
