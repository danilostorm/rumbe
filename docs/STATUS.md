# NASCAR Rumble — HostStorm WebAssembly Alpha (2026-10-16)

## Endereços e arquivos
Prévia recompilada: https://rumble.hoststorm.cloud/recomp/
Site original funcionando: https://rumble.hoststorm.cloud/
Arquivos no AEROCOOL: /mnt/user/Games/nascar-rumble/
Disco privado: game/disc/NASCAR Rumble.bin e NASCAR Rumble.cue
Projeto: recomp/web-port/

## O que foi confirmado
A compilação usa PSXRecomp: código MIPS do SLUS-01068 recompilado em C, depois compilado para WebAssembly pelo Emscripten 4.0.23. Não utiliza EmulatorJS dentro da prévia, mas o runtime mantém os periféricos e BIOS necessários do PS1.

A prévia antiga falhava com DataCloneError e SharedArrayBuffer ao usar HTTP num IP LAN. O navegador exige contexto seguro e crossOriginIsolated para as threads WASM. O HTTPS do site agora inclui COOP/COEP somente na rota /recomp/, sem quebrar o CDN do EmulatorJS na página original.

O jogo carrega OpenBIOS, inicializa o executável, mostra a abertura EA/NASCAR e continua incrementando VBlanks. Porém a imagem permanece na introdução após cerca de dois minutos; nenhuma corrida foi comprovada.

Apliquei à cópia de PSXRecomp dedicada ao NASCAR duas alterações derivadas do port de pesca: ponte de teclado/gamepad ao SIO e otimização do scanout da VRAM com apresentação WebGL2. Enter, Cross e direcional foram recebidos com palavras PS1 ativas-baixas nos testes. O teste Chromium confirmou quadros no canvas WebGL2 e duração de apresentação da ordem de 0,14 ms, mas somente cerca de 17 VBlanks/s numa amostra. Isso NÃO comprova velocidade jogável.

A tentativa de pular FMVs não resolveu o bloqueio na abertura. Testes adicionais com escalonador LLE, CD 1x e saída nativa 4:3 devem ser avaliados separadamente.

## Arquivos
- recomp/patches/nascar-web-input.patch: ponte SIO.
- recomp/patches/nascar-webgl-performance.patch: renderização WebGL2 e métricas.
- recomp/nascar-input.js: publicação dos comandos no controle recompilado.
- recomp/nascar-renderer.js: canvas WebGL2 acelerado, com fallback interno.
- recomp/build_public_preview.py: empacotamento da prévia.
- site/recomp/: HTML e runtime prontos, sem incluir cópia do disco.
- site/index.html: atalho opcional à Alpha; site original preservado.
- nginx.conf: isolamento COOP/COEP restrito à prévia.
- recomp/test-client/: capturas e registros de diagnóstico.

## Reconstrução
Os dois patches já estão aplicados ao clone recomp/web-port/psxrecomp. Não reaplicá-los sobre esse clone.

cd /mnt/user/Games/nascar-rumble/recomp/web-port
docker run --rm -v "$PWD:/project" -w /project emscripten/emsdk:4.0.23 bash -lc 'cmake --build build-web -j 10'
cd /mnt/user/Games/nascar-rumble
python3 recomp/build_public_preview.py
docker exec nascar-rumble-web nginx -t
docker exec nascar-rumble-web nginx -s reload

Para checkout limpo compatível, aplique ambos os patches UMA VEZ antes de compilar. As fontes geradas SLUS_010.68_full.c e dispatch são necessárias.

## Pendências técnicas
Identificar por que os VBlanks avançam mas o jogo permanece no logotipo EA; investigar CD-ROM XA/MDEC, temporizadores e scheduler, e transições de código dinâmico/overlays. Validar menu, largada, inputs e áudio em uma corrida real. Não é possível afirmar ainda que NASCAR Rumble está 100% jogável na versão recompilada.

O site principal mantém a versão anterior que já funciona enquanto corrigimos o port nativo.

Atenção à distribuição: o endpoint /disc/nascar-rumble.bin existente no site principal expõe dados protegidos por direitos autorais. A prévia reutiliza essa rota, mas não contém o BIN em seus assets. Hospedagem pública exige autorização dos titulares.

## Diagnóstico adicional de 16/10 — ISO/MDEC

A tabela de diretórios ISO 9660 foi lida da imagem original, sem modificá-la. `CW/OPENING/INTRO.WVE` começa no setor lógico 93447 e termina imediatamente antes de 97407. `CW/OPENING/LEGAL.LSC` ocupa 97407–97424 e a área `DUMMY.DAT` começa em 97425.

No teste com interface de diagnóstico somente leitura, a máquina continuou solicitando setores acima do fim de `INTRO.WVE` (inclusive setores de `DUMMY.DAT`) enquanto a imagem da EA permaneceu estática. Houve aproximadamente 1417 VBlanks, mas somente 17 chamadas de decodificação MDEC e ~364 apresentações WebGL2 naquele ponto. O CD seguia em `ReadN (0x06)`, modo 0xA0, com buffer de setor disponível. O contador de leituras suspensas pelo ACK continuou zero.

**Interpretação:** a transição da introdução ainda está bloqueada e exige análise do fluxo de CD/MDEC/game. O padrão sugere leitura prolongada após o fim do vídeo, mas isso não demonstra, por si só, um erro no driver; o código do jogo, temporizadores, DMA ou decodificador podem ser responsáveis. Evitar correções artificiais em LBA/EOF até comparar com um comportamento de referência.

Adicionado patch opcional `nascar-readonly-debug.patch` com `nascar_web_diag(n)` para observar CD-ROM, registros MIPS e MDEC sem alterar a emulação. Esta instrumentação permanece no binário de teste local e **não** foi colocada no site público.
