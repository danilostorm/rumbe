const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const p=await b.newPage({viewport:{width:1280,height:800}});
p.on('pageerror',e=>console.log('PAGEERROR',e.message));
p.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text().slice(0,220))});
await p.goto('http://127.0.0.1:18883/recomp/',{waitUntil:'domcontentloaded'});
await p.waitForFunction(()=>!document.querySelector('#start').disabled,null,{timeout:60000});
await p.locator('#start').click();
await p.waitForFunction(()=>typeof Module._nascar_web_diag==='function',{timeout:90000});
for(let t=0;t<12;t++){
 await p.waitForTimeout(4000);
 const sample=await p.evaluate(()=>({v:Module._psx_web_perf_vblanks(),d:Array.from({length:47},(_,i)=>Module._nascar_web_diag(i)),draw:Module.fishWebPresenter?.draws}));
 console.log('SAMPLE',t,JSON.stringify(sample));
 if(t===8)await p.locator('#nascarFastCanvas').screenshot({path:'/project/recomp/test-client/diag-end.png'});
}
await b.close();
})().catch(e=>{console.error('FAILED',e.stack);process.exitCode=1});
