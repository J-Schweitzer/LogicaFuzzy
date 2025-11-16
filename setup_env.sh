#!/usr/bin/env bash
set -euo pipefail

# setup_env.sh
# Instala Miniconda se necessário, cria o ambiente conda "Fuzzy",
# instala dependências e cria um lançador executável e um arquivo .desktop.

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_NAME="Fuzzy"
CONDA_DIR="$HOME/miniconda3"
MINICONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
TMP_INSTALLER="/tmp/${MINICONDA_INSTALLER}"

echo "Projeto: $PROJECT_DIR"

# helper
command_exists() { command -v "$1" >/dev/null 2>&1; }

# 1) Garantir conda disponível
if ! command_exists conda; then
  if [ -x "$CONDA_DIR/bin/conda" ]; then
    echo "Conda encontrado em $CONDA_DIR"
    export PATH="$CONDA_DIR/bin:$PATH"
  else
    echo "Conda não encontrado. Instalando Miniconda em $CONDA_DIR..."
    # baixar instalador
    if command_exists curl; then
      curl -fsSL -o "$TMP_INSTALLER" "https://repo.anaconda.com/miniconda/$MINICONDA_INSTALLER"
    elif command_exists wget; then
      wget -qO "$TMP_INSTALLER" "https://repo.anaconda.com/miniconda/$MINICONDA_INSTALLER"
    else
      echo "Erro: nem curl nem wget disponíveis para baixar Miniconda." >&2
      exit 1
    fi

    echo "Executando instalador Miniconda (modo silencioso)..."
    bash "$TMP_INSTALLER" -b -p "$CONDA_DIR"
    rm -f "$TMP_INSTALLER"
    export PATH="$CONDA_DIR/bin:$PATH"
    echo "Miniconda instalada em $CONDA_DIR"
  fi
else
  echo "Conda já disponível no PATH"
fi

# Inicializar conda para este shell
# preferir usar hook
if command_exists conda; then
  # load conda functions
  eval "$(conda shell.bash hook)"
else
  echo "Erro: conda não está disponível após instalação." >&2
  exit 1
fi

# 2) Criar ambiente se não existir
if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  echo "Ambiente conda '$ENV_NAME' já existe. Pulando criação."
else
  echo "Criando ambiente conda '$ENV_NAME' com Python 3.11..."
  conda create -y -n "$ENV_NAME" python=3.11
fi

# 3) Instalar dependências principais via conda (conda-forge)
echo "Instalando pacotes via conda (canal conda-forge): pyqt matplotlib numpy scipy pip"
conda install -y -n "$ENV_NAME" -c conda-forge pyqt matplotlib numpy scipy pip

# 4) Instalar pacotes pip no ambiente (scikit-fuzzy, fpdf)
echo "Instalando pacotes pip no ambiente: scikit-fuzzy, fpdf"
conda run -n "$ENV_NAME" pip install --upgrade pip
conda run -n "$ENV_NAME" pip install scikit-fuzzy fpdf

# 5) Criar script executável para rodar a aplicação sem ativar manualmente o env
RUN_SH="$PROJECT_DIR/run_fuzzy.sh"
cat > "$RUN_SH" <<'EOF'
#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
"
# usa conda run para executar dentro do ambiente sem ativar
conda run -n Fuzzy python3 "$SCRIPT_DIR/app/main.py"
EOF
chmod +x "$RUN_SH"

# 6) Criar arquivo .desktop para iniciar via GUI (usuário atual)
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"
DESKTOP_FILE="$DESKTOP_DIR/fuzzy-diagnostico.desktop"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=Fuzzy Diagnóstico
Comment=Diagnóstico Médico - Fuzzy
Exec=$RUN_SH
Icon=
Terminal=false
Type=Application
Categories=Utility;
EOF

echo "\nInstalação concluída."
echo "- Ambiente conda: $ENV_NAME"
echo "- Executavel de lançamento: $RUN_SH"
echo "- Atalho desktop criado em: $DESKTOP_FILE"

echo "Para testar agora, execute:\n  $RUN_SH"

echo "Se o ícone não aparecer no menu imediatamente, execute:\n  update-desktop-database ~/.local/share/applications || true"

exit 0
