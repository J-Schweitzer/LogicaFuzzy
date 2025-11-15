# fuzzy_engine/fuzzy_plotter.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from fuzzy_engine.diagnostico_fuzzy import DiagnosticoFuzzy

class FuzzyPlotter:
    """
    Cria figuras matplotlib com as funções de pertinência e pode retorná-las
    embutidas em um canvas para exibir no PyQt5.
    """

    def __init__(self, diagnostico: 'DiagnosticoFuzzy'):
        self.d = diagnostico

    def plot_febre(self, highlight_value=None):
        fig, ax = plt.subplots(figsize=(4.5,2.8), dpi=100)
        x = self.d.febre.universe
        for name in self.d.febre.terms.keys():
            mf = self.d.febre[name]
            ax.plot(x, mf.mf if hasattr(mf, 'mf') else x, label=name)
        ax.set_title("Febre (°C)")
        ax.legend()
        if highlight_value is not None:
            ax.axvline(highlight_value, color='k', linestyle='--')
        fig.tight_layout()
        return fig

    def plot_tosse(self, highlight_value=None):
        fig, ax = plt.subplots(figsize=(4.5,2.8), dpi=100)
        x = self.d.tosse.universe
        for name in self.d.tosse.terms.keys():
            mf = self.d.tosse[name]
            ax.plot(x, mf.mf if hasattr(mf, 'mf') else x, label=name)
        ax.set_title("Tosse (0-10)")
        ax.legend()
        if highlight_value is not None:
            ax.axvline(highlight_value, color='k', linestyle='--')
        fig.tight_layout()
        return fig

    def plot_saturacao(self, highlight_value=None):
        fig, ax = plt.subplots(figsize=(4.5,2.8), dpi=100)
        x = self.d.saturacao.universe
        for name in self.d.saturacao.terms.keys():
            mf = self.d.saturacao[name]
            ax.plot(x, mf.mf if hasattr(mf, 'mf') else x, label=name)
        ax.set_title("Saturação (%)")
        ax.legend()
        if highlight_value is not None:
            ax.axvline(highlight_value, color='k', linestyle='--')
        fig.tight_layout()
        return fig

    def plot_risco(self, highlight_value=None):
        fig, ax = plt.subplots(figsize=(4.5,2.8), dpi=100)
        x = self.d.risco.universe
        for name in self.d.risco.terms.keys():
            mf = self.d.risco[name]
            ax.plot(x, mf.mf if hasattr(mf, 'mf') else x, label=name)
        ax.set_title("Risco (%)")
        ax.legend()
        if highlight_value is not None:
            ax.axvline(highlight_value, color='k', linestyle='--')
        fig.tight_layout()
        return fig

    def to_canvas(self, fig):
        canvas = FigureCanvas(fig)
        return canvas
