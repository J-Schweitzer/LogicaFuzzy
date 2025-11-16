
# Diagnóstico Médico com Lógica Fuzzy

Este é um projeto de aplicação desktop desenvolvida em Python e PyQt5 que utiliza Lógica Fuzzy (Fuzzy Logic) para calcular o risco de diagnóstico médico com base em sintomas. A aplicação permite que o usuário insira valores para febre, tosse e saturação de oxigênio para estimar um percentual de risco.

# 🌟 Funcionalidades

A aplicação é organizada em abas e oferece as seguintes funcionalidades:

Cálculo de Risco: Na aba "Diagnóstico", o usuário pode selecionar uma doença (conjunto de regras), inserir a temperatura (febre), um nível de tosse (0-10) e a saturação de oxigênio (%).

Feedback Visual Imediato: Ao calcular, uma janela pop-up exibe os gráficos de pertinência para cada variável de entrada (Febre, Tosse, Saturação) e saída (Risco), destacando os valores inseridos.

Regras Acionadas: Uma mensagem informa as 5 principais regras fuzzy que foram acionadas pelo cálculo, juntamente com seu grau de ativação.

Visualização de Gráficos Fuzzy: A aba "Gráficos Fuzzy" exibe os gráficos estáticos das funções de pertinência (conjuntos fuzzy) para todas as variáveis do sistema (ex: Febre Baixa, Média, Alta).

Visualização de Regras: A aba "Regras Fuzzy" mostra um texto com todas as regras cadastradas no motor fuzzy para os diferentes conjuntos de doenças.

Histórico de Cálculos: A aba "Histórico" salva automaticamente cada cálculo realizado, permitindo ao usuário revisar diagnósticos anteriores, atualizar a lista ou limpar o histórico.

Exportação para PDF: Na aba principal, o botão "Exportar Relatório (PDF)" gera um documento PDF com os dados de entrada, o resultado do risco e os gráficos de pertinência, permitindo salvar um registro formal do diagnóstico.

# ⚙️ Como Funciona
O núcleo do projeto é o DiagnosticoFuzzy, que (presumivelmente) utiliza uma biblioteca como scikit-fuzzy ou similar para:

Fuzzificação: Converter os valores numéricos de entrada (ex: febre de 38.7°C) em graus de pertinência em conjuntos fuzzy (ex: 70% "Febre Média" e 30% "Febre Alta").

Inferência (Regras): Aplicar um conjunto de regras (ex: "SE febre é Alta E tosse é Forte, ENTÃO risco é Alto") para determinar a ativação de cada regra.

Agregação e Defuzzificação: Combinar os resultados das regras e convertê-los de volta em um valor numérico único (ex: "Risco de 85.2%").

A interface gráfica (main.py) captura esses dados, chama o motor e exibe os resultados de forma amigável, usando matplotlib para incorporar os gráficos diretamente na UI com PyQt5.
=======
# Diagnóstico Médico — Fuzzy

Descrição
----------
Esta aplicação é uma interface gráfica (PyQt5) para um motor de lógica fuzzy que realiza um diagnóstico de risco médico com base em três entradas principais: febre (°C), intensidade da tosse (0–10) e saturação de oxigênio (%).

O problema que resolve
----------------------
- Fornece uma avaliação de risco quantitativa (0–100%) a partir de variáveis clínicas que são imprecisas por natureza.
- Usa regras fuzzy para combinar pertences linguísticas (por exemplo: febre alta, tosse forte, saturação baixa) e produzir um resultado interpretável.
- Facilita visualização das funções de pertinência e permite exportar relatórios em PDF.

Principais funcionalidades
-------------------------
- Interface moderna em PyQt5 com abas para diagnóstico, gráficos de pertinência, regras e histórico.
- Validação e normalização das entradas (aceita `,` ou `.` como separador decimal).
- Visualização das funções de pertinência (matplotlib embutido).
- Histórico local de consultas e exportação de relatório em PDF com figuras.

Pré-requisitos
--------------
- Sistema Linux (testado no Ubuntu). O projeto instala Miniconda automaticamente se necessário.
- Conexão com a internet (para baixar dependências na primeira execução).

Instalação e execução (modo simples)
-----------------------------------
1. Tornar o script de setup executável:

```bash
chmod +x setup_env.sh
```

2. Executar o setup (cria/atualiza ambiente Conda `Fuzzy`, instala dependências e cria um atalho no menu):

```bash
./setup_env.sh
```

3. Ao final do script, a aplicação será iniciada automaticamente. Depois você pode abrir a aplicação a partir do atalho no menu ("Fuzzy Diagnóstico") ou executando manualmente:

```bash
./run_fuzzy.sh
```

Observações importantes
----------------------
- O instalador cria um ambiente Conda chamado `Fuzzy` e instala as dependências necessárias (PyQt5, matplotlib, numpy, scipy, scikit-fuzzy, networkx, fpdf, entre outras).
- Se já existir uma instalação do Conda (Anaconda/Miniconda) o script irá reutilizá-la.
- O atalho do menu é criado como `~/.local/share/applications/fuzzy-diagnostico.desktop`.
- Se o atalho não abrir a aplicação, execute `./run_fuzzy.sh` no terminal para ver mensagens de erro e verifique o arquivo de log `~/.fuzzy_launcher.log`.

Remoção / Reset (modo testador)
------------------------------
Para limpar todos os artefatos criados pelo setup (atalho, launcher e ambiente):

```bash
# parar processos (se necessário)
pkill -f "app/main.py" || true

# remover atalho do menu
rm -f ~/.local/share/applications/fuzzy-diagnostico.desktop

# remover run script
rm -f run_fuzzy.sh

# remover histórico local
rm -f ~/.fuzzy_history.json

# remover ambiente conda (opcional)
conda env remove -n Fuzzy -y || true

# remover Miniconda (APENAS se instalado pelo setup e você quiser removê-lo)
rm -rf ~/miniconda3
```

Estrutura do projeto
--------------------
- `app/` — aplicação PyQt5 e recursos (UI, assets, fuzzy_engine, utils)
- `fuzzy_engine/` — motor fuzzy (definição de universos, pertinências e regras)
- `utils/` — helpers (histórico, exportação PDF)
- `setup_env.sh` — script de instalação e criação do atalho
- `run_fuzzy.sh` — lançador para executar a aplicação com o ambiente Conda ativado

Contribuindo
------------
Contribuições são bem-vindas. Para alterações grandes, prefira abrir uma issue descrevendo a mudança e depois um pull request com testes quando aplicável.

Suporte e Debug
---------------
- Logs do launcher: `~/.fuzzy_launcher.log` (útil quando o atalho do menu não inicia a app)
- Mensagens de erro: execute `./run_fuzzy.sh` no terminal para receber saída direta

Licença
-------
Projeto para uso acadêmico / educativo (sem licença explícita fornecida). Pergunte se você precisa de uma licença específica.
# LogicaFuzzy
>>>>>>> ba6b9a2 (Atualizações realizadas no projeto)
