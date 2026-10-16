const {chromium}=require('playwright'),crypto=require('crypto');
(async()=>{
 const b=await chromium.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const p=await b.newPage({viewport:{width:1280,height:850}});
 const errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('console',e=>{if(e.type()==='error')errors.push(e.text().slice(0,280))});
 await p.goto('https://rumble.hoststorm.cloud/recomp/',{waitUntil:'domcontentloaded'});
 await p.waitForFunction(()=>!document.querySelector('#start').disabled,null,{timeout:60000});await p.locator('#start').click();
 await p.waitForFunction(()=>typeof Module._psx_web_set_pad_buttons==='function',{timeout:90000});
 await p.waitForTimeout(23000);
 const state=async(label)=>{
   const ss=await p.locator('#canvas').screenshot({path:'/project/recomp/test-client/directpad-'+label+'.png'});
   const v=await p.evaluate(()=>({v:Module._psx_web_perf_vblanks(),bits:Module._psx_web_get_pad_buttons?.(),status:document.getElementById('status')?.textContent}));
   console.log('FRAME',label,crypto.createHash('sha1').update(ss).digest('hex').slice(0,12),JSON.stringify(v));
 };
 await state('before');
 for(const key of ['Enter','x','ArrowDown','Enter']){
   await p.locator('#canvas').focus();
   await p.keyboard.down(key);await p.waitForTimeout(1250);
   console.log('BUTTON_DOWN',key,await p.evaluate(()=>({bits:Module._psx_web_get_pad_buttons?.(),active:document.body.classList.contains('running')})));
   await p.keyboard.up(key);await p.waitForTimeout(3100);
   await state(key);
 }
 console.log('ERRORS',errors);
 await b.close();
})().catch(e=>{console.log('TEST_FAILED',e.stack);process.exitCode=1});
