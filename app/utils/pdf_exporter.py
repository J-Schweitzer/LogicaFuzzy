# utils/pdf_exporter.py
from fpdf import FPDF
from pathlib import Path
from datetime import datetime
import tempfile
import os

class PDFExporter:
    """
    Exporta relatório simples contendo os inputs, resultado e imagens (png) dos gráficos.
    """

    def __init__(self, target_folder: Path = Path.cwd()):
        self.target_folder = Path(target_folder)

    def export(self, filename: str, patient_info: dict, risco: float, figs: list):
        """
        figs: lista de matplotlib.figure.Figure
        """
        # salvar figuras temporárias
        tmpdir = tempfile.mkdtemp(prefix="fuz_")
        img_paths = []
        try:
            for i, fig in enumerate(figs):
                path = Path(tmpdir) / f"fig_{i}.png"
                fig.savefig(path, dpi=150)
                img_paths.append(path)

            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 8, "Relatório de Diagnóstico Fuzzy", ln=True, align='C')
            pdf.ln(4)
            pdf.set_font("Arial", size=11)
            pdf.cell(0, 6, f"Data: {datetime.now().isoformat()}", ln=True)
            pdf.cell(0, 6, f"Resultado (risco): {risco:.2f} %", ln=True)
            pdf.ln(4)
            pdf.cell(0, 6, "Entradas:", ln=True)
            for k, v in patient_info.items():
                pdf.cell(0, 6, f" - {k}: {v}", ln=True)
            pdf.ln(6)

            for img in img_paths:
                pdf.add_page()
                pdf.image(str(img), x=15, w=180)
            out_path = self.target_folder / f"{filename}.pdf"
            pdf.output(str(out_path))
        finally:
            # cleanup
            for p in img_paths:
                try:
                    os.remove(p)
                except:
                    pass
            try:
                os.rmdir(tmpdir)
            except:
                pass
        return out_path
