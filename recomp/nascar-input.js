/* Direct browser keyboard/gamepad -> compiled PS1 SIO pad bridge.
 * Based on the validated HostStorm Fish WebAssembly input path.
 * This does not depend on EmulatorJS, nor does it modify gameplay data.
 */
(function(){
  'use strict';
  const map={Enter:3,NumpadEnter:3,ArrowUp:4,ArrowRight:5,ArrowDown:6,ArrowLeft:7,KeyX:14,KeyS:13,KeyZ:15,KeyA:12,KeyQ:10,KeyW:11,KeyE:8,KeyR:9,ShiftRight:0};
  const gamepad={0:14,1:13,2:15,3:12,4:10,5:11,6:8,7:9,8:0,9:3,12:4,13:6,14:7,15:5};
  const keys=new Set();
  const canvas=document.querySelector('#canvas');
  function inputEnabled(){
    return document.body.classList.contains('running') &&
      !document.querySelector('dialog[open]') &&
      !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName||'');
  }
  window.addEventListener('keydown',e=>{
    if(!(e.code in map)||!inputEnabled())return;
    keys.add(e.code);
    if(canvas===document.activeElement && /^Arrow/.test(e.code))e.preventDefault();
  },true);
  window.addEventListener('keyup',e=>keys.delete(e.code),true);
  window.addEventListener('blur',()=>keys.clear());
  document.addEventListener('visibilitychange',()=>{if(document.hidden)keys.clear()});
  let wasReady=false;
  function run(){
    const module=window.Module;
    if(module&&typeof module._psx_web_set_pad_buttons==='function'){
      if(!wasReady){console.info('[NASCAR] Ponte direta de controles PS1 pronta');wasReady=true;}
      let bits=65535;
      if(inputEnabled()){
        keys.forEach(key=>{if(key in map)bits&=~(1<<map[key])});
        try{
          for(const pad of navigator.getGamepads?.()||[]){
            if(!pad?.connected)continue;
            for(const k of Object.keys(gamepad))if(pad.buttons[k]?.pressed)bits&=~(1<<gamepad[k]);
            if(pad.axes?.length>=2){
              if(pad.axes[0]<-.4)bits&=~(1<<7);
              if(pad.axes[0]>.4)bits&=~(1<<5);
              if(pad.axes[1]<-.4)bits&=~(1<<4);
              if(pad.axes[1]>.4)bits&=~(1<<6);
            }
          }
        }catch(_){}
      }
      module._psx_web_set_pad_buttons(bits);
    }
    requestAnimationFrame(run);
  }
  requestAnimationFrame(run);
})();
