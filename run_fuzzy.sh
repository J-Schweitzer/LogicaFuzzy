#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Garantir que o display está definido (necessário para GUI)
if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
  export DISPLAY=:0
fi

# Inicializar conda no shell
eval "$(conda shell.bash hook)"

# Ativar o ambiente Fuzzy
conda activate Fuzzy

# Executar a aplicação dentro do ambiente ativado
# QT_QPA_PLATFORM garante que o backend correto seja usado
export QT_QPA_PLATFORM=xcb
exec python3 "$SCRIPT_DIR/app/main.py"
