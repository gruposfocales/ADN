#!/bin/sh
# Crea o actualiza un perfil de Hermes por repo (lista en perfiles.txt).
# - Clona o actualiza cada repo en $REPOS_DIR/<repo> (por defecto $HERMES_HOME) (solo lectura: pull --ff-only).
# - El SOUL.md de cada perfil es un ENLACE al AGENTS.md de su repo: GitHub es la única fuente.
# - El token nunca se guarda en disco: se pasa en cada git por cabecera.
# Uso (dentro del contenedor): sh perfiles.sh [perfiles.txt]
set -eu
HOME_H="${HERMES_HOME:-/opt/data}"
LISTA="${1:-$(dirname "$0")/perfiles.txt}"
ORG="${GITHUB_ORG:-gruposfocales}"
: "${GITHUB_TOKEN:?Falta GITHUB_TOKEN}"
AUTH="Authorization: Basic $(printf 'x-access-token:%s' "$GITHUB_TOKEN" | base64 | tr -d '\n')"
REPOS_DIR="${REPOS_DIR:-$HOME_H}"   # en hermes2 los repos ya están en /opt/data
mkdir -p "$REPOS_DIR"

grep -v '^\s*#' "$LISTA" | grep -v '^\s*$' | while read -r PERFIL REPO; do
  DIR="$REPOS_DIR/$REPO"
  if [ -d "$DIR/.git" ]; then
    git -C "$DIR" -c http.extraHeader="$AUTH" pull -q --ff-only || echo "⚠ $REPO: no se pudo actualizar"
  else
    git -c http.extraHeader="$AUTH" clone -q "https://github.com/$ORG/$REPO.git" "$DIR"
  fi
  if [ "$PERFIL" = default ]; then
    PH="$HOME_H"
  else
    PH="$HOME_H/profiles/$PERFIL"
    [ -d "$PH" ] || hermes profile create "$PERFIL" </dev/null >/dev/null || { echo "⚠ $PERFIL: no se pudo crear el perfil"; continue; }
  fi
  [ -f "$DIR/AGENTS.md" ] || { echo "⚠ $REPO no tiene AGENTS.md"; continue; }
  ln -sfn "$DIR/AGENTS.md" "$PH/SOUL.md"
  echo "✓ $PERFIL → $REPO"
done
