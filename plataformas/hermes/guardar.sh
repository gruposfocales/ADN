#!/bin/sh
# Guarda lo que Hermes cambió en un repo como RAMA + PULL REQUEST (nunca en main).
# Uso: sh guardar.sh <carpeta-del-repo> "Fase N · lote X · resumen"
set -eu
DIR="${1:?Falta la carpeta del repo}"; MSG="${2:?Falta el mensaje}"
: "${GITHUB_TOKEN:?Falta GITHUB_TOKEN}"
ORG="${GITHUB_ORG:-gruposfocales}"
REPO="$(basename "$DIR")"
AUTH="Authorization: Basic $(printf 'x-access-token:%s' "$GITHUB_TOKEN" | base64 | tr -d '\n')"
cd "$DIR"
[ -n "$(git status --porcelain)" ] || { echo "Nada que guardar en $REPO"; exit 0; }
RAMA="hermes/$(date +%Y-%m-%d-%H%M)"
git checkout -q -b "$RAMA"
git add -A
git -c user.name="Hermes" -c user.email="hermes@users.noreply.github.com" commit -q -m "$MSG"
git -c http.extraHeader="$AUTH" push -q origin "$RAMA"
BODY=$(printf '{"title":"%s","head":"%s","base":"main","body":"Guardado por Hermes. Revisa y fusiona."}' "$(printf '%s' "$MSG" | sed 's/"/\\"/g')" "$RAMA")
URL=$(curl -s -X POST -H "Authorization: Bearer $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$ORG/$REPO/pulls" -d "$BODY" | sed -n 's/.*"html_url": *"\([^"]*\/pull\/[0-9]*\)".*/\1/p' | head -1)
git checkout -q main && git -c http.extraHeader="$AUTH" pull -q --ff-only || true
echo "✓ PR: ${URL:-no se pudo crear (revisa permisos del token)}"
