const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('static/js/analytics-consent.js', 'utf8');
function browser({host='gifts.aimuse.ae', choice=null, storageBlocked=false}={}) {
  const events={}, scripts=[], cookieWrites=[], stored=new Map();
  const key='muse-gifts-analytics-consent-v1';
  if(choice)stored.set(key,JSON.stringify({value:choice,at:Date.now()}));
  const buttons=['granted','denied'].map(value=>({dataset:{analyticsChoice:value},addEventListener(_,fn){this.click=fn;},focus(){}}));
  const panel={hidden:true,dataset:{measurementId:'G-TEST1234'},querySelectorAll(){return buttons;},querySelector(){return buttons[0];}};
  const settings={hidden:true,addEventListener(_,fn){this.click=fn;},focus(){}};
  const context={URL,Date,JSON,encodeURIComponent,navigator:{},location:{hostname:host,origin:'https://'+host,pathname:'/ar/',search:'?email=private@example.com',hash:'#sensitive',reload(){context.reloaded=true;}},localStorage:{getItem(k){if(storageBlocked)throw Error('disabled');return stored.get(k)||null;},setItem(k,v){if(storageBlocked)throw Error('disabled');stored.set(k,v);}},document:{referrer:'https://example.com/private?email=person@example.com',getElementById(){return panel;},querySelector(){return settings;},createElement(){return {};},head:{appendChild(s){scripts.push(s);}}}};
  Object.defineProperty(context.document,'cookie',{get(){return '_ga=example; _ga_TEST1234=example; unrelated=keep';},set(v){cookieWrites.push(v);}});
  context.window=context;context.addEventListener=(name,fn)=>{events[name]=fn;};
  vm.runInNewContext(source,context);
  return {context,panel,settings,scripts,cookieWrites,buttons,events,stored,key};
}
test('unanswered and declined visitors make no Google request',()=>{
  const fresh=browser();assert.equal(fresh.scripts.length,0);assert.equal(fresh.panel.hidden,false);
  fresh.buttons[1].click();assert.equal(fresh.scripts.length,0);assert.equal(fresh.panel.hidden,true);
  assert.equal(browser({choice:'denied'}).scripts.length,0);
  assert.equal(browser({storageBlocked:true}).scripts.length,0);
});
test('opt-in starts once and strips URL/referrer private data',()=>{
  const b=browser();b.buttons[0].click();b.buttons[0].click();assert.equal(b.scripts.length,1);
  const calls=b.context.dataLayer.map(a=>Array.from(a));
  assert.equal(calls[0][0],'consent');assert.equal(calls[0][2].analytics_storage,'denied');
  assert.equal(calls[1][2].analytics_storage,'granted');
  const config=calls.find(c=>c[0]==='config')[2];
  assert.equal(config.page_location,'https://gifts.aimuse.ae/ar/');
  assert.equal(config.page_referrer,'https://example.com/');
  assert.equal(config.allow_google_signals,false);assert.equal(config.allow_ad_personalization_signals,false);
  assert.equal(JSON.stringify(calls).includes('private@example.com'),false);
});
test('withdrawal disables future events, expires only analytics cookies and stops timers',()=>{
  const b=browser({choice:'granted'});assert.equal(b.scripts.length,1);
  b.settings.click();assert.equal(b.panel.hidden,false);b.buttons[1].click();
  assert.equal(b.context['ga-disable-G-TEST1234'],true);assert.equal(b.context.reloaded,true);
  assert.ok(b.cookieWrites.length>0);assert.ok(b.cookieWrites.every(v=>v.startsWith('_ga')));
  assert.ok(!b.cookieWrites.some(v=>v.includes('Domain=aimuse.ae')));
});
test('a different preview hostname never collects, even with saved consent',()=>{
  const b=browser({host:'127.0.0.1',choice:'granted'});assert.equal(b.scripts.length,0);assert.equal(b.settings.hidden,true);
});
test('consent withdrawal in another tab stops an active tag',()=>{
  const b=browser({choice:'granted'});b.stored.delete(b.key);b.events.storage({key:b.key});
  assert.equal(b.context.reloaded,true);assert.equal(b.context['ga-disable-G-TEST1234'],true);
});
