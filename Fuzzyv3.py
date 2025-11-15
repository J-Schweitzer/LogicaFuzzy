import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QSlider, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt


# ------------------------
# Função de pertinência triangular
# ------------------------
def triangular(x, a, b, c):
    """Função triangular clássica."""
    return np.maximum(0, np.minimum((x - a) / (b - a + 1e-9), (c - x) / (c - b + 1e-9)))


# ------------------------
# Sistema Fuzzy corrigido
# ------------------------
def diagnostico_fuzzy(sintomas):
    """
    Calcula o grau de pertinência (0–1) para Gripe, Sinusite, Dengue e Covid.
    As porcentagens finais (0–100) são derivadas desses graus.
    """
    temp, tosse, dor_cabeca, dor_musc, congestao, olfato, fadiga, nausea = sintomas

    # Normaliza todos os sintomas para o intervalo [0, 1]
    sintomas_norm = np.array(sintomas) / 10

    # Regras simples baseadas em sintomas relevantes (exemplo educativo)
    gripe_in = (0.4*sintomas_norm[0] + 0.4*sintomas_norm[1] + 0.2*sintomas_norm[3])  # temp, tosse, dor_musc
    sinusite_in = (0.5*sintomas_norm[2] + 0.5*sintomas_norm[4])                      # dor_cabeca, congestao
    dengue_in = (0.5*sintomas_norm[0] + 0.4*sintomas_norm[3] + 0.4*sintomas_norm[6] + 0.3*sintomas_norm[7])
    covid_in = (0.5*sintomas_norm[0] + 0.4*sintomas_norm[1] + 0.4*sintomas_norm[3] + 0.4*sintomas_norm[5])

    entradas = np.array([gripe_in, sinusite_in, dengue_in, covid_in]) * 10  # escala 0–10

    # Funções de pertinência (triangulares) definidas no universo 0–10
    params = {
        "Gripe": (2, 4, 7),
        "Sinusite": (1, 5, 8),
        "Dengue": (3, 6, 9),
        "Covid-19": (4, 7, 10)
    }

    nomes = ["Gripe", "Sinusite", "Dengue", "Covid-19"]
    graus = []

    for i, nome in enumerate(nomes):
        a, b, c = params[nome]
        grau = triangular(entradas[i], a, b, c)
        graus.append(grau)

    # Normaliza para que o máximo seja 1.0 (apenas precaução)
    graus = np.clip(graus, 0, 1)
    resultados = np.array(graus) * 100  # transforma em porcentagem

    return resultados, entradas


# ------------------------
# Interface PyQt5
# ------------------------
class DiagnosticoFuzzyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagnóstico Fuzzy de Doenças Comuns")
        self.setGeometry(100, 100, 780, 820)
        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        conteudo = QWidget()
        layout_conteudo = QVBoxLayout(conteudo)

        titulo = QLabel("🩺 Sistema de Diagnóstico Fuzzy")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout_conteudo.addWidget(titulo)

        subtitulo = QLabel("Ajuste os sintomas conforme necessário (0–10).")
        subtitulo.setStyleSheet("font-size: 13px;")
        layout_conteudo.addWidget(subtitulo)

        # Sliders de sintomas
        self.sintomas_labels = [
            "Temperatura (°C)", "Tosse", "Dor de cabeça", "Dor muscular",
            "Congestão nasal", "Perda de olfato", "Fadiga", "Náusea"
        ]
        self.sintomas_sliders = []
        for label in self.sintomas_labels:
            hbox = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setMinimumWidth(240)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 10)
            slider.setSingleStep(1)
            slider.setValue(0)
            hbox.addWidget(lbl)
            hbox.addWidget(slider)
            layout_conteudo.addLayout(hbox)
            self.sintomas_sliders.append(slider)

        # Botão
        btn_calcular = QPushButton("Calcular Diagnóstico")
        btn_calcular.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px; padding:8px;"
        )
        btn_calcular.clicked.connect(self.calcular_diagnostico)
        layout_conteudo.addWidget(btn_calcular)

        aviso = QLabel("* Este sistema é apenas educativo e não substitui diagnóstico médico real.")
        aviso.setStyleSheet("font-style: italic; color: gray; font-size: 10px;")
        layout_conteudo.addWidget(aviso)

        scroll_area.setWidget(conteudo)
        layout_principal.addWidget(scroll_area)
        self.setLayout(layout_principal)

    def calcular_diagnostico(self):
        sintomas = [s.value() for s in self.sintomas_sliders]
        resultados, entradas = diagnostico_fuzzy(sintomas)
        nomes = ["Gripe", "Sinusite", "Dengue", "Covid-19"]
        cores = ["#2196F3", "#FF9800", "#4CAF50", "#F44336"]

        # Mensagem textual
        texto = "\n".join([f"{doenca}: {valor:.1f}%" for doenca, valor in zip(nomes, resultados)])
        QMessageBox.information(self, "Resultado do Diagnóstico", texto)

        # Plotagem fuzzy
        x = np.linspace(0, 10, 200)
        params = {
            "Gripe": (2, 4, 7),
            "Sinusite": (1, 5, 8),
            "Dengue": (3, 6, 9),
            "Covid-19": (4, 7, 10)
        }

        plt.figure(figsize=(10, 6))
        for i, nome in enumerate(nomes):
            a, b, c = params[nome]
            curva = triangular(x, a, b, c)
            plt.plot(x, curva, color=cores[i], label=nome, linewidth=2)
            plt.fill_between(x, curva, alpha=0.15, color=cores[i])

            # Ponto do usuário
            entrada = entradas[i]
            grau = resultados[i] / 100
            plt.scatter([entrada], [grau], color=cores[i], s=80, edgecolors='k', zorder=5)
            plt.plot([entrada, entrada], [0, grau], color=cores[i], linestyle='--', alpha=0.6)
            plt.text(entrada, grau + 0.05, f"{resultados[i]:.1f}%", color=cores[i],
                     fontsize=10, fontweight='bold', ha='center')

        plt.title("Funções de Pertinência e Grau Fuzzy Calculado")
        plt.xlabel("Valor de entrada normalizado (0–10)")
        plt.ylabel("Grau de pertinência (0–1)")
        plt.ylim(-0.05, 1.1)
        plt.xlim(0, 10)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()


# ------------------------
# Execução
# ------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = DiagnosticoFuzzyApp()
    janela.show()
    sys.exit(app.exec_())
