#!/bin/sh
# Menú con números para abrir Hermes en un perfil (lista en perfiles.txt).
# Uso (Terminal del contenedor): sh /opt/data/ADN/plataformas/hermes/perfil.sh
# Atajo: sh perfil.sh --instalar  → luego basta escribir: perfil
set -eu
AQUI="$(cd "$(dirname "$0")" && pwd)"
if [ "${1:-}" = "--instalar" ]; then
  ln -sf "$AQUI/perfil.sh" /usr/local/bin/perfil && chmod +x "$AQUI/perfil.sh"
  echo "Listo. Desde ahora escribe: perfil"; exit 0
fi
LISTA="${1:-$AQUI/perfiles.txt}"
NOMBRES=$(grep -v '^\s*#' "$LISTA" | grep -v '^\s*$' | awk '{print $1 "|" $2}')
i=0
echo "Perfiles de Hermes:"
for L in $NOMBRES; do
  i=$((i+1)); P=${L%%|*}; R=${L#*|}
  [ "$P" = default ] && P="default (bibliotecario)"
  echo "  $i) $P  ·  $R"
done
printf "Escribe el número y Enter: "
read -r N
case "$N" in ''|*[!0-9]*) echo "Número no válido"; exit 1;; esac
[ "$N" -ge 1 ] && [ "$N" -le "$i" ] || { echo "Número no válido"; exit 1; }
P=$(echo "$NOMBRES" | sed -n "${N}p"); P=${P%%|*}
echo "Abriendo Hermes en el perfil: $P  (para salir: /exit)"
if [ "$P" = default ]; then hermes || true; else hermes -p "$P" || true; fi
# La Terminal entra como root: devuelve los archivos al usuario de Hermes
[ "$(id -u)" = 0 ] && chown -R hermes:hermes /opt/data 2>/dev/null || true
echo "Listo, permisos en orden. Puedes cerrar la Terminal."
