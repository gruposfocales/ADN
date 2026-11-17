#!/bin/sh
# Crea o actualiza un perfil de Hermes por repo (lista en perfiles.txt).
# - Clona o actualiza cada repo en $REPOS_DIR/<repo> (por defecto $HERMES_HOME) (solo lectura: pull --ff-only).
# - El SOUL.md de cada perfil es una línea neutra; las instrucciones son solo el AGENTS.md del repo
#   (Hermes lo carga como contexto al abrir con --in). GitHub es la única fuente.
# - El token nunca se guarda en disco: se pasa en cada git por cabecera.
# - Crea un atajo de una palabra por perfil (ej. `vejez`) que abre Hermes en la carpeta del repo
#   con una sesión nueva. El default se llama `inicio`. Se guardan en $HERMES_HOME/bin (volumen).
# Uso (dentro del contenedor): sh perfiles.sh [perfiles.txt]
set -eu
HOME_H="${HERMES_HOME:-/opt/data}"
LISTA="${1:-$(dirname "$0")/perfiles.txt}"
ORG="${GITHUB_ORG:-gruposfocales}"
: "${GITHUB_TOKEN:?Falta GITHUB_TOKEN}"
AUTH="Authorization: Basic $(printf 'x-access-token:%s' "$GITHUB_TOKEN" | base64 | tr -d '\n')"
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
SOUL_NEUTRO='Tus instrucciones están en el AGENTS.md (o CLAUDE.md) de la carpeta del proyecto, cargado como contexto del proyecto. Síguelo: no tienes otra identidad ni otras reglas. Si no aparece, avísalo y pide abrir Hermes en la carpeta del repo.'

# limpia_hermes_md DIR: quita el .hermes.md que dejaba una versión anterior de este script (ya no hace falta).
limpia_hermes_md() {
  H="$1/.hermes.md"
  [ -f "$H" ] && grep -qF '<!-- generado por perfiles.sh -->' "$H" && rm -f "$H"
  EX="$1/.git/info/exclude"
  [ -f "$EX" ] && grep -qx '/.hermes.md' "$EX" && { grep -vx '/.hermes.md' "$EX" > "$EX.tmp"; mv "$EX.tmp" "$EX"; }
  return 0
}

grep -v '^\s*#' "$LISTA" | grep -v '^\s*$' | while read -r PERFIL REPO; do
  DIR="$REPOS_DIR/$REPO"
  if [ -d "$DIR/.git" ]; then
    git -C "$DIR" -c http.extraHeader="$AUTH" pull -q --ff-only </dev/null || echo "⚠ $REPO: no se pudo actualizar"
  else
    git -c http.extraHeader="$AUTH" clone -q "https://github.com/$ORG/$REPO.git" "$DIR" </dev/null \
      || { echo "⚠ $REPO: no se pudo clonar (¿el token tiene acceso a este repo?)"; continue; }
  fi
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
  echo "✓ $PERFIL → $REPO/$ALMA · atajo: $NOMBRE"
done

# Atajos que NO abren Hermes (no gastan contexto ni tokens):
#   pulso  → el Pulso del Día de gf-inicio, directo en la terminal
#   atajos → la lista de todos los atajos
INICIO=$(grep -v '^\s*#' "$LISTA" | awk '$1=="default"{print $2}')
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
  grep -v '^\s*#' "$LISTA" | grep -v '^\s*$' | while read -r PERFIL REPO; do
    [ "$PERFIL" = default ] && PERFIL=inicio
    printf '  %-14s Hermes en %s, sesión nueva\n' "$PERFIL" "$REPO"
  done
  echo 'Agrega -c para retomar la última sesión (ej. vejez -c). Para salir de Hermes: /exit'
  echo 'FIN'
} > "$BIN/atajos"
chmod 755 "$BIN/atajos"
for D in /usr/local/bin "$HOME/.local/bin"; do ln -sfn "$BIN/atajos" "$D/atajos" 2>/dev/null || true; done
echo
sh "$BIN/atajos"
