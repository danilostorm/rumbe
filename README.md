# NASCAR Rumble — WebAssembly (HostStorm)

Port experimental do **NASCAR Rumble (PlayStation 1)** para navegador, utilizando [PSXRecomp](https://github.com/RetroPortingToolKit/psxrecomp) e Emscripten. Não utiliza EmulatorJS na versão recompilada.

**Status:** Alpha. Inicialização, tela de abertura da EA, controle PS1 e apresentação WebGL2 já foram verificados. **Menus e corridas ainda não estão jogáveis na recompilação.** Não confunda esta versão com o site antigo baseado em emulação.

- Prévia WebAssembly: https://rumble.hoststorm.cloud/recomp/
- Site anterior preservado: https://rumble.hoststorm.cloud/
- Arquivos locais: `/mnt/user/Games/nascar-rumble`
- Guia de diagnóstico: `docs/STATUS.md`

O repositório contém somente scripts, patches e infraestrutura próprios deste port. **Não inclui o jogo original (BIN/CUE), BIOS, executáveis extraídos, código de jogo recompilado nem assets proprietários.** Para recompilar, é necessário fornecer sua própria cópia legal do jogo e gerar os arquivos locais usando as ferramentas do PSXRecomp.

## Organização

- `recomp/patches/` — modificações incrementais no runtime PSXRecomp
- `recomp/nascar-input.js` — controle teclado/gamepad
- `recomp/nascar-renderer.js` — apresentação WebGL2
- `recomp/build_public_preview.py` — empacotamento da prévia
- `infra/nginx.conf` — servidor com isolamento COOP/COEP para WASM
- `tests/` — diagnósticos automatizados, sem ROM incluída

O site principal só deve ser substituído quando o menu, largada, corrida, controles e áudio forem comprovadamente funcionais.