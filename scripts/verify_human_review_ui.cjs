const {chromium}=require('playwright');
const assert=require('assert/strict');
const fs=require('fs');
(async()=>{
  const browser=await chromium.launch({channel:'msedge',headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  try {
    await page.goto(process.env.ESG_QA_URL || 'http://127.0.0.1:8052/',{waitUntil:'domcontentloaded'});
    await page.locator('#analysis-records input[type=radio]').first().waitFor({timeout:60000});
    await page.locator('#analysis-records input[type=radio]').first().check();
    await page.locator('#human-review-current').filter({hasText:/pending_human_review|partially_reviewed/}).waitFor();
    await page.locator('#human-review-reviewer').fill('UI TEST FIXTURE ONLY');
    await page.locator('#human-review-action input').fill('Lưu bản sửa');
    await page.keyboard.press('ArrowDown');await page.keyboard.press('Enter');
    const labels=page.locator('#human-review-fields label');
    await labels.filter({hasText:/^value$/}).locator('input').check();
    await page.locator('#human-review-patch').fill('{"value":"10"}');
    await page.locator('#human-review-reason').fill('SYNTHETIC QA ONLY: exercise correction persistence, not a real PDF label.');
    await page.locator('#human-review-confirm input').check();
    await page.locator('#human-review-save').click();
    await page.locator('#human-review-feedback').filter({hasText:'partially_reviewed'}).waitFor({timeout:30000});
    await page.locator('#human-review-current').filter({hasText:'partially_reviewed'}).waitFor();
    assert((await page.locator('#human-review-current').innerText()).includes('"value": "10"'));
    await page.reload({waitUntil:'domcontentloaded'});
    await page.locator('#analysis-records input[type=radio]').first().waitFor({timeout:60000});
    await page.locator('#analysis-records input[type=radio]').first().check();
    await page.locator('#human-review-current').filter({hasText:'partially_reviewed'}).waitFor();
    assert((await page.locator('#human-review-current').innerText()).includes('"value": "10"'));
    await page.setViewportSize({width:390,height:844});
    await page.locator('#human-review-reviewer').scrollIntoViewIfNeeded();
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth+1));
    await page.screenshot({path:'outputs/human_review_mobile_20261021.png'});
    assert.deepEqual(errors,[]);
    console.log(JSON.stringify({passed:true,correction_persists_after_reload:true,mobile_no_overflow:true,errors}));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
