import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QSlider, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt


# =============================
# SISTEMA DE DIAGNÓSTICO FUZZY
# =============================
def diagnostico_fuzzy(sintomas):
    """
    Inferência fuzzy simplificada com curvas de pertinência.
    Retorna probabilidades (0–100%) para Gripe, Sinusite, Dengue e Covid-19.
    """
    temp, tosse, dor_cabeca, dor_musc, congestao, olfato, fadiga, nausea = sintomas

    # Pesos fixos definidos no código (0–1)
    w_temp, w_tosse, w_dor, w_musc, w_cong, w_olf, w_fad, w_nau = [1, 1, 1, 1, 1, 1, 1, 1]

    # Cálculos básicos
    gripe = (0.4*temp + 0.4*tosse + 0.6*dor_musc + 0.2*dor_cabeca + 0.1*congestao) * 10
    sinusite = (0.5*dor_cabeca + 0.5*congestao + 0.2*temp) * 10
    dengue = (0.6*temp + 0.4*dor_musc + 0.5*dor_cabeca + 0.4*fadiga + 0.3*nausea) * 10
    covid = (0.5*temp + 0.4*tosse + 0.4*dor_musc + 0.6*olfato + 0.4*fadiga + 0.2*nausea) * 10

    # Aplicar pesos fixos
    gripe *= (w_temp + w_tosse + w_musc + w_dor + w_cong) / 5
    sinusite *= (w_dor + w_cong + w_temp) / 3
    dengue *= (w_temp + w_musc + w_dor + w_fad + w_nau) / 5
    covid *= (w_temp + w_tosse + w_musc + w_olf + w_fad + w_nau) / 6

    resultados = np.clip([gripe, sinusite, dengue, covid], 0, 100)
    return resultados


# =============================
# INTERFACE PYQT5
# =============================
class DiagnosticoFuzzyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagnóstico Fuzzy de Doenças Comuns")
        self.setGeometry(100, 100, 700, 750)
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

        self.sintomas_labels = [
            "Temperatura (°C)", "Tosse", "Dor de cabeça", "Dor muscular",
            "Congestão nasal", "Perda de olfato", "Fadiga", "Náusea"
        ]
        self.sintomas_sliders = []

        for label in self.sintomas_labels:
            hbox = QHBoxLayout()
            lbl = QLabel(label)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 10)
            slider.setSingleStep(1)
            slider.setValue(0)
            hbox.addWidget(lbl)
            hbox.addWidget(slider)
            layout_conteudo.addLayout(hbox)
            self.sintomas_sliders.append(slider)

        btn_calcular = QPushButton("Calcular Diagnóstico")
        btn_calcular.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px;")
        btn_calcular.clicked.connect(self.calcular_diagnostico)
        layout_conteudo.addWidget(btn_calcular)

        scroll_area.setWidget(conteudo)
        layout_principal.addWidget(scroll_area)
        self.setLayout(layout_principal)

    def calcular_diagnostico(self):
        sintomas = [s.value() for s in self.sintomas_sliders]
        resultados = diagnostico_fuzzy(sintomas)
        nomes = ["Gripe", "Sinusite", "Dengue", "Covid-19"]

        texto = "\n".join([f"{doenca}: {valor:.1f}%" for doenca, valor in zip(nomes, resultados)])
        QMessageBox.information(self, "Resultado do Diagnóstico", texto)

        # Geração de gráfico fuzzy (curvas de pertinência)
        x = np.linspace(0, 10, 100)
        gripe_curve = np.maximum(0, np.minimum((x - 0)/5, (10 - x)/5))
        sinusite_curve = np.maximum(0, np.minimum((x - 2)/4, (8 - x)/4))
        dengue_curve = np.maximum(0, np.minimum((x - 4)/3, (10 - x)/6))
        covid_curve = np.maximum(0, np.minimum((x - 3)/3, (10 - x)/5))

        plt.figure(figsize=(7, 4))
        plt.plot(x, gripe_curve, label='Gripe')
        plt.plot(x, sinusite_curve, label='Sinusite')
        plt.plot(x, dengue_curve, label='Dengue')
        plt.plot(x, covid_curve, label='Covid-19')

        plt.title("Funções de Pertinência (Lógica Fuzzy)")
        plt.xlabel("Intensidade dos sintomas")
        plt.ylabel("Grau de pertinência")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()


# =============================
# EXECUÇÃO DO APP
# =============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = DiagnosticoFuzzyApp()
    janela.show()
    sys.exit(app.exec_())
