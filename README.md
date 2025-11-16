
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
