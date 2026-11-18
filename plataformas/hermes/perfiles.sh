#!/bin/sh
# Crea o actualiza un perfil de Hermes por repo (lista única: ADN/agentes.txt, columna perfil).
# - Clona o actualiza cada repo en $REPOS_DIR/<repo> (por defecto $HERMES_HOME) (solo lectura: pull --ff-only).
# - El SOUL.md de cada perfil es una línea neutra; las instrucciones son solo el AGENTS.md del repo
#   (Hermes lo carga como contexto al abrir con --in). GitHub es la única fuente.
# - El token nunca se guarda en disco: se pasa en cada git por cabecera.
# - Crea un atajo de una palabra por perfil (ej. `vejez`) que abre Hermes en la carpeta del repo
#   con una sesión nueva. El default se llama `inicio`. Se guardan en $HERMES_HOME/bin (volumen).
# Uso (dentro del contenedor): sh perfiles.sh [agentes.txt]
set -eu
HOME_H="${HERMES_HOME:-/opt/data}"
LISTA="${1:-$(dirname "$0")/../../agentes.txt}"
# filas "REPO CLASE PERFIL" sin comentarios. Un repo con perfil "-" (ej. el de datos) se trae, pero no lleva perfil ni atajo.
filas() { sed 's/#.*//' "$LISTA" | awk 'NF >= 3 {print $1, $2, $3}'; }
ORG="${GITHUB_ORG:-gruposfocales}"
: "${GITHUB_TOKEN:?Falta GITHUB_TOKEN}"
AUTH="Authorization: Basic $(printf 'x-access-token:%s' "$GITHUB_TOKEN" | base64 | tr -d '\n')"
# El ADN (este script y agentes.txt) se trae primero. Si cambió, el script se vuelve a correr con la versión
# nueva: así nunca corre con reglas viejas (antes el ADN se actualizaba al final, ya tarde).
NUCLEO_DIR=$(cd "$(dirname "$0")/../.." && pwd)
if [ -z "${PERFILES_RELANZADO:-}" ] && [ -d "$NUCLEO_DIR/.git" ]; then
  ANTES=$(git -C "$NUCLEO_DIR" -c safe.directory="$NUCLEO_DIR" rev-parse HEAD)
  git -C "$NUCLEO_DIR" -c safe.directory="$NUCLEO_DIR" -c http.extraHeader="$AUTH" pull -q --ff-only </dev/null \
    || echo "⚠ ADN: no se pudo actualizar (sigo con la versión que hay)"
  if [ "$(git -C "$NUCLEO_DIR" -c safe.directory="$NUCLEO_DIR" rev-parse HEAD)" != "$ANTES" ]; then
    echo "↻ ADN actualizado: vuelvo a correr con la versión nueva"
    PERFILES_RELANZADO=1 exec sh "$0" "$@"
  fi
fi
# Telegram: el IPv6 del contenedor no sirve y el bot quedaba mudo ("connect timed out").
# Esta línea hace que prefiera IPv4. Vive fuera del volumen, así que un Redeploy la borra:
# por eso se vuelve a poner aquí en cada corrida (y luego Restart del servicio).
if grep -qs '^precedence ::ffff:0:0/96' /etc/gai.conf; then :
elif echo 'precedence ::ffff:0:0/96 100' >> /etc/gai.conf 2>/dev/null; then
  echo "✓ Telegram: IPv4 preferido (/etc/gai.conf). Haz Restart del servicio para que el bot lo tome."
else
  echo "⚠ Telegram: no pude escribir /etc/gai.conf (corre este script como root)"
fi
REPOS_DIR="${REPOS_DIR:-$HOME_H}"   # en hermes2 los repos ya están en /opt/data
mkdir -p "$REPOS_DIR"
BIN="$HOME_H/bin"                   # atajos en el volumen: sobreviven a un redeploy
mkdir -p "$BIN"

# atajo NOMBRE PERFIL DIR: script de una línea; sin -c ni --resume, así que cada vez es una sesión nueva
atajo() {
  if [ "$2" = default ]; then P=""; else P="-p $2 "; fi
  printf '#!/bin/sh\n# Atajo de perfiles.sh: Hermes en %s, sesión nueva.\nexec hermes %s--in %s "$@"\n' "$3" "$P" "$3" > "$BIN/$1"
  chmod 755 "$BIN/$1"
  # al PATH: /usr/local/bin y ~/.local/bin (este último reemplaza el alias que crea `hermes profile create`)
  for D in /usr/local/bin "$HOME/.local/bin"; do
    mkdir -p "$D" 2>/dev/null && ln -sfn "$BIN/$1" "$D/$1" 2>/dev/null || true
  done
}

# SOUL.md neutro: el espacio de identidad de Hermes no lleva nada del proyecto.
# Las instrucciones son SOLO el AGENTS.md (o CLAUDE.md) del repo, que Hermes carga como contexto
# del proyecto al abrir en su carpeta (los atajos usan --in). Así se lee una sola vez y no se mezcla.
# Si el SOUL.md quedara vacío, Hermes pondría su identidad por defecto (en inglés): por eso va una línea.
SOUL_NEUTRO='Tus instrucciones son el AGENTS.md (o CLAUDE.md) del proyecto: el de la carpeta donde trabajas o el que cargues con un comando. Síguelo: no tienes otra identidad ni otras reglas. Si todavía no hay ninguno cargado, no inventes reglas: ofrece /menu, /pulso, /inicio o el comando de un proyecto (ej. /vejez). Para empezar limpio: /new.'

# Skills del bot de Telegram (perfil default): el bot arranca limpio (sin AGENTS.md) y el usuario
# carga lo que necesita con un comando: /inicio, /menu, /pulso o /<proyecto>. Cada skill solo dice
# "lee este AGENTS.md": la única fuente sigue siendo el repo. Se regeneran en cada corrida.
SKILLS="$HOME_H/skills/gruposfocales"
rm -rf "$SKILLS" && mkdir -p "$SKILLS"

# skill_repo NOMBRE DIR ARCHIVO: /NOMBRE carga el agente del repo DIR (su ARCHIVO de instrucciones).
skill_repo() {
  mkdir -p "$SKILLS/$1"
  cat > "$SKILLS/$1/SKILL.md" <<FIN
---
name: $1
description: Carga en esta sesión el agente del repo $(basename "$2") (sus instrucciones están en $3).
---
# Agente $1 · repo $(basename "$2")

1. Si en esta sesión ya cargaste otro agente de GruposFocales (otro de estos comandos), no sigas:
   pide al usuario que escriba /new y después /$1. Así el contexto no se mezcla.
2. Lee completo $2/$3 con tu herramienta para leer archivos. Desde ahora ese archivo es tu
   guía de trabajo en esta sesión: síguelo en todo, como si fuera tu identidad.
3. Trabajas en la carpeta $2: antes de cada comando de terminal haz cd $2.
   Las rutas relativas de $3 son relativas a esa carpeta.
4. Si la conversación se resume o ya no tienes el texto de $3 a la vista, vuelve a leerlo antes de seguir.
5. Empieza como dice $3 que se empieza una sesión.
FIN
}

# limpia_hermes_md DIR: quita el .hermes.md que dejaba una versión anterior de este script (ya no hace falta).
limpia_hermes_md() {
  H="$1/.hermes.md"
  [ -f "$H" ] && grep -qF '<!-- generado por perfiles.sh -->' "$H" && rm -f "$H"
  EX="$1/.git/info/exclude"
  [ -f "$EX" ] && grep -qx '/.hermes.md' "$EX" && { grep -vx '/.hermes.md' "$EX" > "$EX.tmp"; mv "$EX.tmp" "$EX"; }
  return 0
}

filas | while read -r REPO CLASE PERFIL; do
  DIR="$REPOS_DIR/$REPO"
  if [ -d "$DIR/.git" ]; then
    # remoto limpio: clones viejos tenían el token pegado en la URL (quedaba guardado en .git/config)
    git -C "$DIR" -c safe.directory="$DIR" remote set-url origin "https://github.com/$ORG/$REPO.git"
    if ! git -C "$DIR" -c safe.directory="$DIR" -c http.extraHeader="$AUTH" pull -q --ff-only </dev/null; then
      echo "⚠ $REPO: no se pudo actualizar"
      SUCIOS=$(git -C "$DIR" -c safe.directory="$DIR" status --porcelain | awk '$1=="M"{print $2}' | tr '\n' ' ')
      [ -n "$SUCIOS" ] && echo "  Tiene cambios locales: $SUCIOS. Si son archivos generados, descártalos (una línea): git -C $DIR -c safe.directory=$DIR checkout -- $SUCIOS"
    fi
  else
    git -c http.extraHeader="$AUTH" clone -q "https://github.com/$ORG/$REPO.git" "$DIR" </dev/null \
      || { echo "⚠ $REPO: no se pudo clonar (¿el token tiene acceso a este repo?)"; continue; }
  fi
  # Hermes corre como el dueño de /opt/data; este script suele correr como root. Se devuelve el repo a ese
  # dueño para que Hermes pueda leerlo y escribirlo, y safe.directory evita el "dubious ownership" de git.
  chown -R "$(stat -c %u:%g "$HOME_H")" "$DIR" 2>/dev/null || true
  [ "$PERFIL" = "-" ] && { echo "✓ $REPO (sin perfil: solo datos)"; continue; }
  if [ "$PERFIL" = default ]; then
    PH="$HOME_H"
  else
    PH="$HOME_H/profiles/$PERFIL"
    [ -d "$PH" ] || hermes profile create "$PERFIL" --clone </dev/null >/dev/null || { echo "⚠ $PERFIL: no se pudo crear el perfil"; continue; }
  fi
  ALMA=""
  for F in AGENTS.md CLAUDE.md README.md; do [ -f "$DIR/$F" ] && { ALMA="$F"; break; }; done
  [ -n "$ALMA" ] || { echo "⚠ $REPO no tiene AGENTS.md, CLAUDE.md ni README.md"; continue; }
  # el modelo (DeepSeek) y demás ajustes salen del perfil default
  [ "$PERFIL" = default ] || cp "$HOME_H/config.yaml" "$PH/config.yaml" 2>/dev/null || true
  # los perfiles solo leen claves de su propio .env: se escribe ahí desde el entorno del contenedor
  if [ "$PERFIL" != default ] && [ -n "${DEEPSEEK_API_KEY:-}" ]; then
    touch "$PH/.env" && chmod 600 "$PH/.env"
    grep -v '^DEEPSEEK_API_KEY=' "$PH/.env" > "$PH/.env.tmp" || true
    echo "DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY" >> "$PH/.env.tmp" && mv "$PH/.env.tmp" "$PH/.env" && chmod 600 "$PH/.env"
    chown "$(stat -c %u:%g "$HOME_H")" "$PH/.env" 2>/dev/null || true   # Hermes corre con el usuario dueño de /opt/data
  fi
  rm -f "$PH/SOUL.md"   # borra el enlace viejo antes de escribir (si no, se escribiría DENTRO del AGENTS.md del repo)
  if [ "$ALMA" = README.md ]; then
    ln -s "$DIR/README.md" "$PH/SOUL.md"   # sin AGENTS.md ni CLAUDE.md, Hermes no carga el README como contexto
  else
    printf '%s\n' "$SOUL_NEUTRO" > "$PH/SOUL.md"
    chown "$(stat -c %u:%g "$HOME_H")" "$PH/SOUL.md" 2>/dev/null || true
  fi
  limpia_hermes_md "$DIR"
  if [ "$PERFIL" = default ]; then NOMBRE=inicio; else NOMBRE="$PERFIL"; fi
  atajo "$NOMBRE" "$PERFIL" "$DIR"
  [ "$ALMA" = README.md ] || skill_repo "$NOMBRE" "$DIR" "$ALMA"
  echo "✓ $PERFIL → $REPO/$ALMA · atajo: $NOMBRE"
done

# Atajos que NO abren Hermes (no gastan contexto ni tokens):
#   pulso  → el Pulso del Día de gf-inicio, directo en la terminal
#   atajos → la lista de todos los atajos
INICIO=$(filas | awk '$3=="default"{print $1}')
if [ -n "$INICIO" ] && [ -d "$REPOS_DIR/$INICIO" ]; then
  D="$REPOS_DIR/$INICIO"
  mkdir -p "$SKILLS/pulso"
  # skill_atajo NOMBRE ATAJO: /NOMBRE carga el agente de inicio y hace su atajo ATAJO (así cada línea
  # de la lista de atajos es un enlace que funciona en Telegram).
  skill_atajo() {
    mkdir -p "$SKILLS/$1"
    cat > "$SKILLS/$1/SKILL.md" <<FIN2
---
name: $1
description: Carga el agente de inicio ($INICIO) y hace su atajo $2.
---
# Atajo $2 de GruposFocales

1. Si en esta sesión ya cargaste un agente de proyecto (no el de inicio), pide al usuario /new y después /$1.
2. Si aún no lo leíste en esta sesión, lee completo $D/AGENTS.md: es tu guía de trabajo. Trabajas en $D (cd antes de cada comando).
3. Haz el atajo \`$2\` tal como lo define ese archivo y responde solo con eso.
FIN2
  }
  skill_atajo menu menu
  for A in bloqueos nuevo cerrar fabrica repos prs guardar actualizar; do skill_atajo "$A" "$A"; done
  skill_atajo herramientas skills   # /skills es un comando propio de Hermes: por eso /herramientas
  cat > "$SKILLS/pulso/SKILL.md" <<FIN
---
name: pulso
description: Muestra el Pulso del Día (proyectos y git) sin cargar ningún agente.
---
# Pulso del Día

1. Corre: cd $D && python3 herramientas/pulso.py
2. Muestra la salida tal cual, sin agregar análisis. No cargues ningún AGENTS.md.
3. Cierra con una línea: "Escribe /menu, /inicio o el comando de un proyecto (ej. /vejez). Para empezar limpio: /new".
FIN
fi
chown -R "$(stat -c %u:%g "$HOME_H")" "$SKILLS" 2>/dev/null || true
if [ -n "$INICIO" ] && [ -f "$REPOS_DIR/$INICIO/herramientas/pulso.py" ]; then
  printf '#!/bin/sh\n# Atajo de perfiles.sh: Pulso del Día sin abrir Hermes.\nexec python3 %s "$@"\n' "$REPOS_DIR/$INICIO/herramientas/pulso.py" > "$BIN/pulso"
  chmod 755 "$BIN/pulso"
  rm -f "$BIN/pulzo"
  for D in /usr/local/bin "$HOME/.local/bin"; do
    rm -f "$D/pulzo" 2>/dev/null || true
    ln -sfn "$BIN/pulso" "$D/pulso" 2>/dev/null || true
  done
fi
{
  echo '#!/bin/sh'
  echo '# Atajo de perfiles.sh: lista de atajos (no abre Hermes).'
  echo "cat <<'FIN'"
  echo 'Atajos de GruposFocales (escribe la palabra y Enter):'
  echo '  pulso          Pulso del Día, sin abrir Hermes (no gasta contexto)'
  echo '  atajos         esta lista'
  filas | while read -r REPO CLASE PERFIL; do
    [ "$PERFIL" = "-" ] && continue
    [ "$PERFIL" = default ] && PERFIL=inicio
    printf '  %-14s Hermes en %s, sesión nueva\n' "$PERFIL" "$REPO"
  done
  echo 'Agrega -c para retomar la última sesión (ej. vejez -c). Para salir de Hermes: /exit'
  echo 'FIN'
} > "$BIN/atajos"
chmod 755 "$BIN/atajos"
# Atajos viejos: si un repo ya no tiene perfil en agentes.txt (ej. bibliotecario), se quita su atajo.
VIGENTES=" $(filas | awk '$3 != "-" {print ($3 == "default" ? "inicio" : $3)}' | tr '\n' ' ') "
for F in "$BIN"/*; do
  N=$(basename "$F")
  grep -q '^# Atajo de perfiles.sh: Hermes en' "$F" 2>/dev/null || continue
  case "$VIGENTES" in *" $N "*) continue ;; esac
  rm -f "$F"
  for D in /usr/local/bin "$HOME/.local/bin"; do [ -L "$D/$N" ] && rm -f "$D/$N"; done
  echo "🗑 atajo viejo quitado: $N (su perfil de Hermes queda sin uso)"
done
for D in /usr/local/bin "$HOME/.local/bin"; do ln -sfn "$BIN/atajos" "$D/atajos" 2>/dev/null || true; done
echo
sh "$BIN/atajos"
