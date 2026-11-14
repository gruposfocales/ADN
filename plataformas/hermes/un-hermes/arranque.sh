#!/bin/sh
# Arranque de un solo Hermes: trae de GitHub los repos y el SOUL.md (y config.yaml, si está en el repo).
# Corre solo en cada deploy/reinicio (ver docker-compose.yml) o desde el chat con "actualizar".
# Nunca detiene el arranque: si algo falla, avisa y sigue.
HOME_H="${HERMES_HOME:-/opt/data}"
ORG="${GITHUB_ORG:-gruposfocales}"
AQUI="$HOME_H/ADN/plataformas/hermes/un-hermes"
REPOS="${HERMES_REPOS:-ADN gf-bibliotecario inv-001-vejez inv-002-comunicacion age-001-en-efecto-noticias com-001-bartolinos disenador-de-agentes}"
[ -n "${GITHUB_TOKEN:-}" ] || { echo "⚠ arranque: falta GITHUB_TOKEN; sigo sin actualizar"; exit 0; }
AUTH="Authorization: Basic $(printf 'x-access-token:%s' "$GITHUB_TOKEN" | base64 | tr -d '\n')"
for R in $REPOS; do
  D="$HOME_H/$R"
  if [ -d "$D/.git" ]; then
    git -C "$D" -c safe.directory='*' -c http.extraHeader="$AUTH" pull -q --ff-only && echo "✓ $R" || echo "⚠ $R: no se pudo actualizar"
  else
    git -c http.extraHeader="$AUTH" clone -q "https://github.com/$ORG/$R.git" "$D" && echo "✓ $R (clonado)" || echo "⚠ $R: no se pudo clonar"
  fi
done
# SOUL.md del Hermes = enlace al de GitHub (si existía uno propio, se guarda una copia una sola vez)
if [ -f "$AQUI/SOUL.md" ]; then
  [ -f "$HOME_H/SOUL.md" ] && [ ! -L "$HOME_H/SOUL.md" ] && cp "$HOME_H/SOUL.md" "$HOME_H/SOUL.md.antes"
  ln -sfn "$AQUI/SOUL.md" "$HOME_H/SOUL.md" && echo "✓ SOUL.md desde GitHub"
fi
# config.yaml: solo si está en el repo (sin claves: usa ${VARIABLES}); copia de respaldo antes de reemplazar
if [ -f "$AQUI/config.yaml" ]; then
  [ -f "$HOME_H/config.yaml" ] && ! cmp -s "$AQUI/config.yaml" "$HOME_H/config.yaml" && cp "$HOME_H/config.yaml" "$HOME_H/config.yaml.antes"
  cp "$AQUI/config.yaml" "$HOME_H/config.yaml" && echo "✓ config.yaml desde GitHub"
fi
chown -R "$(stat -c %u:%g "$HOME_H")" "$HOME_H" 2>/dev/null || true
exit 0
