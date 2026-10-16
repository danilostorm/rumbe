/* HostStorm NASCAR Rumble: optional native WebGL2 presentation fast path. */
(function(){
 'use strict';
 let installed=false;
 function install(){
   if(installed)return;
   var Module=window.Module;
   if(!Module || typeof Module._fish_web_set_direct_present!=='function')return;
   installed=true;
   var nativeCanvas=document.getElementById('canvas');
   if(!nativeCanvas)return;
   var overlay=document.createElement('canvas');overlay.id='nascarFastCanvas';
   overlay.setAttribute('aria-hidden','true');overlay.style.visibility='hidden';
   nativeCanvas.parentNode.appendChild(overlay);
   var log=function(msg){console.log('[Rumble]',msg)};
   var setStatus=function(msg){var status=document.getElementById('status');if(status)status.textContent=msg};
  function initFastRenderer() {
    var canvasFast=document.getElementById('nascarFastCanvas');
    if (!canvasFast) return false;
    var gl=canvasFast.getContext('webgl2',{alpha:false,antialias:false,depth:false,stencil:false,preserveDrawingBuffer:true,powerPreference:'high-performance'});
    if(!gl) {log('WebGL2 unavailable; using software renderer');return false;}
    function disableFastGraphics(reason) {
      if (Module.fishWebPresenter && Module.fishWebPresenter.failed) return;
      if (Module.fishWebPresenter) Module.fishWebPresenter.failed=true;
      log('Renderização WebGL2 interrompida: '+reason+'. Recarregue a página para tentar novamente.');
      setStatus('Falha na aceleração gráfica. Reinicie o jogo.');
      // In an exceptional GPU-device-loss case, release the emulation-side
      // direct-present path. No user-facing renderer picker is exposed.
      try { if (typeof Module._fish_web_set_direct_present === 'function') Module._fish_web_set_direct_present(0); } catch (_) {}
      canvasFast.style.visibility='hidden';
    }
    function shader(type,src) {
      var sh=gl.createShader(type);gl.shaderSource(sh,src);gl.compileShader(sh);
      if(!gl.getShaderParameter(sh,gl.COMPILE_STATUS)) throw Error(gl.getShaderInfoLog(sh));
      return sh;
    }
    try {
      var vs=shader(gl.VERTEX_SHADER,'#version 300 es\nout vec2 uv;\nvoid main(){\nvec2 p=vec2((gl_VertexID==1)?3.0:-1.0,(gl_VertexID==2)?3.0:-1.0);\ngl_Position=vec4(p,0.0,1.0);uv=(p+1.0)*0.5;\n}');
      var fs=shader(gl.FRAGMENT_SHADER,'#version 300 es\nprecision mediump float;\nin vec2 uv;\nuniform sampler2D tex;\nout vec4 color;\nvoid main(){\nvec4 c=texture(tex,vec2(uv.x,1.0-uv.y));\ncolor=vec4(c.b,c.g,c.r,1.0);\n}');
      var program=gl.createProgram();gl.attachShader(program,vs);gl.attachShader(program,fs);
      gl.linkProgram(program);
      if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(program));
      gl.useProgram(program);
      var tex=gl.createTexture();gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,tex);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
      gl.uniform1i(gl.getUniformLocation(program,'tex'),0);
      gl.pixelStorei(gl.UNPACK_ALIGNMENT,1);
      gl.bindVertexArray(gl.createVertexArray());
      var lastW=0,lastH=0;
      var state={draws:0,lastWidth:0,lastHeight:0,draw:function(buffer,w,h){
         if(!w||!h||buffer.length!==w*h*4)return;
         if(gl.isContextLost()){disableFastGraphics('contexto gráfico indisponível');return;}
         try {
         if(lastW!==w||lastH!==h){
           canvasFast.width=w;canvasFast.height=h;gl.viewport(0,0,w,h);
           lastW=w;lastH=h;
           gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,w,h,0,gl.RGBA,gl.UNSIGNED_BYTE,buffer);
         } else gl.texSubImage2D(gl.TEXTURE_2D,0,0,0,w,h,gl.RGBA,gl.UNSIGNED_BYTE,buffer);
         gl.drawArrays(gl.TRIANGLES,0,3);
         if(state.draws===0) canvasFast.style.visibility='visible';
         state.draws++;state.lastWidth=w;state.lastHeight=h;
         if ((state.draws % 120) === 0 && gl.getError() !== gl.NO_ERROR) throw Error('erro WebGL2');
         } catch(err) {disableFastGraphics(err.message);}
      }};
      canvasFast.addEventListener('webglcontextlost',function(e){
        e.preventDefault();disableFastGraphics('contexto WebGL2 perdido');
      });
      Module.fishWebPresenter=state;
      return true;
    } catch(err) {log('WebGL2 initialization failed: '+err.message);return false;}
  }

   if(initFastRenderer()){
     Module._fish_web_set_direct_present(1);
     console.info('[Rumble] WebGL2 accelerated video enabled');
   }else{
     console.warn('[Rumble] WebGL2 unavailable; keeping original software presenter');
   }
 }
 var id=setInterval(function(){
   install();if(installed)clearInterval(id);
 },120);
})();
