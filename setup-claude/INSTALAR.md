# Instalación, primera vez

Claude: hacé esto vos, no se lo pidas a Juan. Él no quiere escribir comandos.

## 1. Instalar los atajos

Mové el contenido de esta carpeta a `.claude/` en la raíz del repo:

```
setup-claude/settings.json      →  .claude/settings.json
setup-claude/commands/*.md      →  .claude/commands/
```

Después borrá `setup-claude/`. Quedan tres atajos: `/arrancar`, `/publicar`, `/estado`.

`settings.json` preaprueba los comandos de este proyecto (build, tests, git local) para no
preguntar en cada paso. **`git push` NO está preaprobado a propósito**: publica en un sitio
público que Thais también mira, y esa confirmación vale la pena. Si Juan prefiere que también
sea automático, agregá `"Bash(git push:*)"` a la lista.

Avisale que tiene que reiniciar la ventana para que aparezcan los atajos:
Command Palette (`Cmd+Shift+P`) → *Developer: Reload Window*.

## 2. Arrancar

Seguí lo que dice `.claude/commands/arrancar.md` — o sea: `git pull`, dependencias, build con
tests, primer commit del fuente, y los tags de las versiones ya publicadas.

## 3. Limpiar

En `CLAUDE.md` hay un bloque **PRIMERA VEZ** al principio. Una vez que terminaste, borralo:
ya no sirve y ocupa contexto en cada sesión.
