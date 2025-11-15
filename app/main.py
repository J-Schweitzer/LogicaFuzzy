# app/main.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QMessageBox, QComboBox, QTabWidget,
    QTextEdit, QListWidget, QFileDialog, QSplitter, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from fuzzy_engine.diagnostico_fuzzy import DiagnosticoFuzzy
from fuzzy_engine.fuzzy_plotter import FuzzyPlotter
from utils.history_manager import HistoryManager
from utils.pdf_exporter import PDFExporter
from app.ui_main import QSS

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagnóstico Médico - Fuzzy (Estilo Moderno)")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(QSS)

        # motores e utilitários
        self.engine = DiagnosticoFuzzy()
        self.plotter = FuzzyPlotter(self.engine)
        self.history = HistoryManager()
        self.pdf = PDFExporter()

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        header = QLabel("Diagnóstico Médico - Fuzzy")
        header.setObjectName("title")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Segoe UI", 16))
        layout.addWidget(header)

        tabs = QTabWidget()
        tabs.addTab(self._tab_diagnostico(), "Diagnóstico")
        tabs.addTab(self._tab_graficos(), "Gráficos Fuzzy")
        tabs.addTab(self._tab_regras(), "Regras Fuzzy")
        tabs.addTab(self._tab_historico(), "Histórico / Exportar")
        layout.addWidget(tabs)

        self.setLayout(layout)

    # --- Tab Diagnóstico ---
    def _tab_diagnostico(self):
        w = QWidget()
        v = QVBoxLayout()

        # inputs
        form = QHBoxLayout()

        self.combo_disease = QComboBox()
        self.combo_disease.addItems(list(self.engine.rulesets.keys()))
        self.input_febre = QLineEdit()
        self.input_febre.setPlaceholderText("Temperatura (°C) — ex: 38.7")
        self.input_tosse = QLineEdit()
        self.input_tosse.setPlaceholderText("Tosse (0-10) — ex: 7")
        self.input_sat = QLineEdit()
        self.input_sat.setPlaceholderText("Saturação (%) — ex: 89")

        form.addWidget(self.combo_disease)
        form.addWidget(self.input_febre)
        form.addWidget(self.input_tosse)
        form.addWidget(self.input_sat)

        v.addLayout(form)

        btn_layout = QHBoxLayout()
        self.btn_calcular = QPushButton("Calcular Risco")
        self.btn_calcular.clicked.connect(self.on_calcular)
        self.btn_export = QPushButton("Exportar Relatório (PDF)")
        self.btn_export.clicked.connect(self.on_exportar)
        btn_layout.addWidget(self.btn_calcular)
        btn_layout.addWidget(self.btn_export)
        v.addLayout(btn_layout)

        # resultado e canvas
        self.lbl_result = QLabel("Resultado: -")
        self.lbl_result.setFont(QFont("Segoe UI", 14))
        v.addWidget(self.lbl_result)

        # area para mostrar gráficos de pertinência em miniatura
        mini_split = QHBoxLayout()
        self.canvas_febre = None
        self.canvas_tosse = None
        self.canvas_sat = None

        self.fig_feb = None
        self.fig_tos = None
        self.fig_sat = None
        self.fig_risk = None

        mini_split_widget = QWidget()
        mini_split_widget.setLayout(mini_split)
        v.addWidget(mini_split_widget)

        w.setLayout(v)
        return w

    # --- Tab Gráficos ---
    def _tab_graficos(self):
        w = QWidget()
        v = QVBoxLayout()

        tabs = QTabWidget()

        # febre
        tab_f = QWidget()
        l_f = QVBoxLayout()
        fig = self.plotter.plot_febre()
        canvas = FigureCanvas(fig)
        l_f.addWidget(canvas)
        tab_f.setLayout(l_f)
        tabs.addTab(tab_f, "Febre")

        # tosse
        tab_t = QWidget()
        l_t = QVBoxLayout()
        fig2 = self.plotter.plot_tosse()
        canvas2 = FigureCanvas(fig2)
        l_t.addWidget(canvas2)
        tab_t.setLayout(l_t)
        tabs.addTab(tab_t, "Tosse")

        # saturacao
        tab_s = QWidget()
        l_s = QVBoxLayout()
        fig3 = self.plotter.plot_saturacao()
        canvas3 = FigureCanvas(fig3)
        l_s.addWidget(canvas3)
        tab_s.setLayout(l_s)
        tabs.addTab(tab_s, "Saturação")

        # risco
        tab_r = QWidget()
        l_r = QVBoxLayout()
        fig4 = self.plotter.plot_risco()
        canvas4 = FigureCanvas(fig4)
        l_r.addWidget(canvas4)
        tab_r.setLayout(l_r)
        tabs.addTab(tab_r, "Risco")

        v.addWidget(tabs)
        w.setLayout(v)
        return w

    # --- Tab Regras ---
    def _tab_regras(self):
        w = QWidget()
        v = QVBoxLayout()
        self.txt_regras = QTextEdit()
        self.txt_regras.setReadOnly(True)
        self._refresh_rules_text()
        v.addWidget(self.txt_regras)
        w.setLayout(v)
        return w

    def _refresh_rules_text(self):
        s = ""
        for disease, rules in self.engine.rulesets.items():
            s += f"--- {disease} ---\n"
            for i, r in enumerate(rules):
                s += f"R{i+1}: {r}\n"
            s += "\n"
        self.txt_regras.setPlainText(s)

    # --- Tab Histórico ---
    def _tab_historico(self):
        w = QWidget()
        v = QVBoxLayout()

        top = QHBoxLayout()
        self.lst_history = QListWidget()
        self._refresh_history()
        top.addWidget(self.lst_history)

        side = QVBoxLayout()
        self.btn_refresh = QPushButton("Atualizar")
        self.btn_refresh.clicked.connect(self._refresh_history)
        self.btn_clear = QPushButton("Limpar Histórico")
        self.btn_clear.clicked.connect(self._clear_history)
        side.addWidget(self.btn_refresh)
        side.addWidget(self.btn_clear)
        side.addStretch()
        top.addLayout(side)

        v.addLayout(top)
        w.setLayout(v)
        return w

    def _refresh_history(self):
        self.lst_history.clear()
        rows = self.history.list(50)
        for e in rows:
            ts = e.get("timestamp")
            disease = e.get("disease")
            risco = e.get("risco")
            self.lst_history.addItem(f"{ts} — {disease} — risco {risco:.2f}%")

    def _clear_history(self):
        self.history.clear()
        self._refresh_history()
        QMessageBox.information(self, "Histórico", "Histórico limpo.")

    # --- Events ---
    def on_calcular(self):
        try:
            feb = float(self.input_febre.text())
            tos = float(self.input_tosse.text())
            sat = float(self.input_sat.text())
        except:
            QMessageBox.warning(self, "Erro", "Preencha os valores corretamente.")
            return

        disease = self.combo_disease.currentText()
        risco, fired, sim = self.engine.calcular_risco(disease, feb, tos, sat)
        self.lbl_result.setText(f"Resultado: {risco:.2f} %")
        # salvar no histórico
        self.history.add(disease, {"febre": feb, "tosse": tos, "saturacao": sat}, risco)
        self._refresh_history()
        # atualizar mini-gráficos com destaque
        self._update_minigraphs(feb, tos, sat, risco)
        # mostrar regras ativadas
        if fired:
            top = sorted(fired, key=lambda x: -x[1])[:5]
            msg = "Regras acionadas (top):\n"
            for idx, deg in top:
                msg += f"R{idx+1} — grau {deg:.3f}\n"
            QMessageBox.information(self, "Regras acionadas", msg)

    def _update_minigraphs(self, feb, tos, sat, risco):
        # gerar figuras
        self.fig_feb = self.plotter.plot_febre(highlight_value=feb)
        self.fig_tos = self.plotter.plot_tosse(highlight_value=tos)
        self.fig_sat = self.plotter.plot_saturacao(highlight_value=sat)
        self.fig_risk = self.plotter.plot_risco(highlight_value=risco)
        # remover widgets antigos se existirem
        # inserir canvases numa nova janela (pop-up) para evitar reorganização complexa
        # Vamos abrir uma janela de visualização rápida
        self._show_preview_window()

    def _show_preview_window(self):
        # janela de preview
        preview = QWidget()
        preview.setWindowTitle("Preview das Pertinências")
        layout = QHBoxLayout()
        c1 = FigureCanvas(self.fig_feb)
        c2 = FigureCanvas(self.fig_tos)
        c3 = FigureCanvas(self.fig_sat)
        c4 = FigureCanvas(self.fig_risk)
        layout.addWidget(c1)
        layout.addWidget(c2)
        layout.addWidget(c3)
        layout.addWidget(c4)
        preview.setLayout(layout)
        preview.setMinimumSize(1000, 300)
        preview.show()
        # manter referência para evitar GC
        self.preview_window = preview

    def on_exportar(self):
        # pega último valores do formulário
        try:
            feb = float(self.input_febre.text())
            tos = float(self.input_tosse.text())
            sat = float(self.input_sat.text())
        except:
            QMessageBox.warning(self, "Erro", "Preencha os valores corretamente para exportar.")
            return
        disease = self.combo_disease.currentText()
        risco, fired, sim = self.engine.calcular_risco(disease, feb, tos, sat)
        # criar figuras atuais (caso não existam)
        figs = []
        figs.append(self.plotter.plot_febre(highlight_value=feb))
        figs.append(self.plotter.plot_tosse(highlight_value=tos))
        figs.append(self.plotter.plot_saturacao(highlight_value=sat))
        figs.append(self.plotter.plot_risco(highlight_value=risco))

        # escolher arquivo
        path, _ = QFileDialog.getSaveFileName(self, "Salvar PDF", f"relatorio_{disease}.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        filename = Path(path).stem
        # exportar
        out = self.pdf.export(filename, {"febre": feb, "tosse": tos, "saturacao": sat, "doenca": disease}, risco, figs)
        QMessageBox.information(self, "Exportado", f"Relatório salvo: {out}")

if __name__ == "__main__":
    from pathlib import Path
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
