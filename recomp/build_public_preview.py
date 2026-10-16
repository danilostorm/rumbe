from pathlib import Path
import re,shutil
root=Path('/mnt/user/Games/nascar-rumble')
dist=root/'site/recomp'
dist.mkdir(parents=True,exist_ok=True)
compiled=root/'recomp/web-port/build-web'
h=(compiled/'NASCAR_Rumble_Recompiled.html').read_text()
# Do not misrepresent the recomp project as Pepsiman/RepsiMan or as validated racing gameplay.
h=h.replace('https://nascar-rumble.ol.mr/','https://rumble.hoststorm.cloud/recomp/')
h=h.replace('https://nascar-rumble.ol.mr/og.png?v=logo-1','')
h=h.replace('https://github.com/kem0x/RepsiMan','https://github.com/RetroPortingToolKit/psxrecomp')
h=h.replace('>Pepsiman · PlayStation<','>NASCAR RUMBLE · PS1<')
h=h.replace('>RECOMPILED BY OL.MR<','>PORT EXPERIMENTAL<')
h=h.replace('>Pronto para acelerar?<','>Prévia WebAssembly<')
h=h.replace('>Start game<','>Iniciar versão recompilada<')
h=h.replace('>Carros velozes, pistas imprevisíveis e muita adrenalina. Reviva NASCAR Rumble diretamente no navegador com uma versão experimental recompilada para WebAssembly.<',
''' >Port experimental de NASCAR Rumble para o navegador. O motor recompilado já executa a introdução, mas menus e corridas ainda não foram validados.<''')
h=h.replace('>Jogue do seu jeito no computador.<','>Entrada por teclado e controle em validação.<')
h=h.replace('>Salve e carregue suas corridas.<','>Memory Card implementado, aguardando testes completos.<')
h=h.replace('>NASCAR Rumble iniciado — use o teclado ou controle.<','>Motor iniciado — verificando o boot do jogo.<')
h=h.replace('NASCAR Rumble iniciado — use o teclado ou controle.','Motor WebAssembly ativo — menu e corrida ainda em validação.')
h=h.replace('>Seus saves<','>Memory Card<')
h=h.replace('>Corrida arcade<','>Corrida arcade<')
h=h.replace('>Explore every enhancement →<','>Ver recursos experimentais<')
# Wrong game-branded asset is not part of NASCAR.
h=h.replace('/assets/title-logo-recompiled.png','/recomp/assets/nascar-rumble-logo.svg')
h=h.replace('https://github.com/mstan/psxrecomp','https://github.com/RetroPortingToolKit/psxrecomp')
h=h.replace('href="/hoststorm-rumble.css?v=1"','href="/recomp/hoststorm-rumble.css?v=2"')
# Remove imported/irrelevant SEO JSON-LD (inaccurately marked as "runner")
h, n = re.subn(r'<script\s+type=["\']?application/ld\+json["\']?>.*?</script>', '', h, flags=re.S)
print('schema blocks removed:',n)
h=h.replace('<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">',
            '<meta name="robots" content="noindex,nofollow">')
h=h.replace('content="NASCAR Rumble recompilado em WebAssembly in your browser through a WebAssembly static recompilation of the PS1 game, with widescreen, controllers, saves, and optional QoL features."',
    'content="NASCAR Rumble em WebAssembly — prévia experimental de recompilação estática do executável de PlayStation, em desenvolvimento."')
h=h.replace('<link rel="manifest" href="/manifest.webmanifest">','')
h=h.replace('https://nascar-rumble.ol.mr','https://rumble.hoststorm.cloud/recomp')
h=h.replace('>Loading WebAssembly…<','>Preparando WebAssembly…<')
# Legacy service worker is not supplied by this project; avoid HTTP 404 on the preview.
h=h.replace('navigator.serviceWorker.register("/sw.js")', 'Promise.resolve()')
# Input bridge loads after the generated UI Module is initialized but before WASM.
assert '<script async src=NASCAR_Rumble_Recompiled.js>' in h
h=h.replace('<script async src=NASCAR_Rumble_Recompiled.js>', '<script src=/recomp/nascar-input.js></script><script src=/recomp/nascar-renderer.js></script><script async src=NASCAR_Rumble_Recompiled.js>')
# Prior build exposes runtime via "script async"; leave intact and unchanged.
assert 'NASCAR_Rumble_Recompiled.js' in h and 'id=start' in h and 'id=canvas' in h
(dist/'index.html').write_text(h)
# Do not copy PS1 game content or copyrighted third-party logo. Original remains server-mounted privately.
for f in ['NASCAR_Rumble_Recompiled.js','NASCAR_Rumble_Recompiled.wasm','openbios.bin','openbios-fastboot.bin']:
  shutil.copy2(compiled/f,dist/f)
shutil.copy2(root/'recomp/nascar-input.js',dist/'nascar-input.js')
shutil.copy2(root/'recomp/nascar-renderer.js',dist/'nascar-renderer.js')
for f in ['hoststorm-rumble.css']:
  shutil.copy2(compiled/f,dist/f)
(dist/'assets').mkdir(exist_ok=True)
# SVG is our own decorative lettering, not an original game asset.
(dist/'assets/nascar-rumble-logo.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="700" height="260" viewBox="0 0 700 260"><rect width="700" height="260" fill="#08111f"/><path d="M0 0h700v14H0zm0 246h700v14H0z" fill="#f37c26"/><g fill="#f8f7ee" font-family="Arial,Helvetica,sans-serif" font-weight="900" text-anchor="middle"><text x="350" y="107" font-size="62" font-style="italic">NASCAR</text><text x="350" y="196" font-size="90" font-style="italic">RUMBLE</text></g><path d="M30 215h640" stroke="#f37c26" stroke-width="5"/></svg>''')
# Update experimental shell from old theme with a sharp orange/track-inspired visual.
p=dist/'hoststorm-rumble.css'
css=p.read_text()+r'''
/* NASCAR Rumble — dedicated HostStorm racing identity.
   Runtime is preserved: only presentation is changed. */
:root,:root[data-theme="dark"] {--background:#090b0f!important;--surface:#111724!important;--surface-soft:#171e2d!important;
--foreground:#fef9f3!important;--muted:#d2cbd0!important;--subtle:#ab9da8!important;--border:#50434a!important;
--border-hover:#ffac4d!important;--button:#ff861f!important;--button-text:#190d05!important}
html,body{background:#0a0e16!important}
body{background:
radial-gradient(ellipse at 80% 10%,rgba(233,77,19,.24),transparent 41%),
linear-gradient(115deg,rgba(2,8,16,.96) 30%,rgba(10,20,36,.89) 65%,rgba(10,9,18,.96)),
repeating-conic-gradient(#ddd 0% 25%,#151c2a 0% 50%) 50% 2%/58px 58px!important}
.site-shell{width:min(1460px,100%);padding-top:22px}
.site-header{border-bottom:1px solid rgba(255,151,69,.3);padding-bottom:20px;margin-bottom:35px}
.site-header>a:before{content:"🏁";background:linear-gradient(130deg,#fca54d,#d64626);font-size:20px;box-shadow:0 0 40px rgba(239,112,34,.35)}
.site-header>a{font-weight:900;font-size:15px}
.release-line{letter-spacing:.28em;color:#f7ac6d}
.intro h1{font-size:clamp(52px,7vw,112px);text-transform:uppercase;font-weight:1000;line-height:.86}
.intro h1 strong{display:block;color:#ff752c;font-style:italic;filter:drop-shadow(1px 4px 22px #fa612b45)}
.intro .lede{color:#d3dce5}
.rumble-art{margin-top:26px}
.rumble-art>span:first-child{background:#fd742b29;border-color:#ffb45677}
.rumble-art>span:last-child{color:#fbb969}
.feature-preview-list{gap:16px}
.feature-preview-item:before{content:'◆';border-color:#fb8c4480;background:#ff81221f;color:#fb8f41}
.game-card{border-color:#fc89379e;box-shadow:0 0 0 1px #ff812b32,0 25px 110px #000b,0 0 85px #f96c2424}
.panel-heading h2{font-weight:900;color:#fff}
.actions #start{background:linear-gradient(120deg,#ffe18c,#f68b25 40%,#ec4d17 100%);box-shadow:0 0 35px #fa713355}
.actions #start:hover{filter:brightness(1.1)}
#status{font-size:12px}
body:not(.running) #status{background:#301a1499;border:1px solid #fc9e5f44;padding:8px 12px;border-radius:9px}
body:not(.running) .game-card:after{content:'RECOMPILAÇÃO EXPERIMENTAL • CORRIDAS AINDA EM VALIDAÇÃO';display:block;padding:16px 24px;
background:#ff7a2120;border-top:1px solid #ff95463c;color:#f5b778;font-size:11px;font-weight:850;letter-spacing:.12em;text-align:center}
body.running .game-card:after{display:none}
#title-logo-frame{display:none!important} /* never overlay an unrelated game's key art */
#recompiled-mark{display:none!important}
#leaderboard-browser,#levels,#pause{display:none!important}
body.running .panel{background:rgba(10,19,29,.98)}
body.running .screen{border:1px solid #fa8a448f;border-radius:12px;overflow:hidden}
@media(max-width:940px){.site-shell{padding:18px}.site-header{margin-bottom:20px}.app-layout{gap:26px}.intro h1{font-size:clamp(46px,11vw,84px)}}
'''
css += '''
#nascarFastCanvas{position:absolute;inset:0;width:100%;height:100%;max-width:100%;max-height:100%;z-index:2;pointer-events:none;image-rendering:pixelated}
'''
p.write_text(css)
print('Prepared isolated /recomp preview with complete browser runtime, page',len(h),'bytes, game image not copied')
