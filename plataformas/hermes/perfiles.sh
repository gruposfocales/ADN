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
  fi
  ln -sfn "$DIR/$ALMA" "$PH/SOUL.md"
  echo "✓ $PERFIL → $REPO/$ALMA"
done
