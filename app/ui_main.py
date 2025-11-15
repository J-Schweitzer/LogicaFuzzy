# app/ui_main.py
# Contém QSS (estilização) e funções utilitárias para a UI moderna.
QSS = """
QWidget {
    background-color: #f6f7fb;
    font-family: "Segoe UI", Roboto, Arial;
    color: #222;
}
QTabWidget::pane { border: none; }
QTabBar::tab {
    background: #e6e9f2;
    border-radius: 8px;
    padding: 8px 16px;
    margin: 4px;
}
QTabBar::tab:selected {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #6a7bd5, stop:1 #8f67f0);
    color: white;
    font-weight: bold;
}
QPushButton {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #7b61ff, stop:1 #4b3ad6);
    color: white;
    padding: 8px 14px;
    border-radius: 8px;
    border: none;
}
QPushButton:hover { opacity: 0.92; }
QLineEdit {
    background: white;
    padding: 8px;
    border-radius: 6px;
    border: 1px solid #d6d9f0;
}
QLabel#title {
    font-size: 18px;
    font-weight: 700;
}
"""
