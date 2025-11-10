import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

# =============================
# SISTEMA DE DIAGNÓSTICO FUZZY
# =============================

def diagnostico_fuzzy(sintomas, pesos):
    """
    Função simplificada de inferência fuzzy
    Retorna probabilidades (0–100%) para Gripe, Resfriado, Sinusite e Covid.
    """

    temp, tosse, dor_cabeca, dor_musc, congestao, olfato, fadiga, nausea = sintomas

    # Pesos adaptativos (0–1)
    w_temp, w_tosse, w_dor, w_musc, w_cong, w_olf, w_fad, w_nau = pesos

    # Cálculo simples ponderado com base em sintomas típicos
    gripe = (0.4*temp + 0.4*tosse + 0.6*dor_musc + 0.2*dor_cabeca + 0.1*congestao) * 10
    resfriado = (0.2*temp + 0.4*congestao + 0.3*tosse + 0.1*dor_cabeca) * 10
    sinusite = (0.5*dor_cabeca + 0.5*congestao + 0.2*temp) * 10
    covid = (0.5*temp + 0.4*tosse + 0.4*dor_musc + 0.6*olfato + 0.4*fadiga + 0.2*nausea) * 10

    # Aplicar pesos adaptativos
    gripe *= (w_temp + w_tosse + w_musc + w_dor + w_cong) / 5
    resfriado *= (w_temp + w_tosse + w_dor + w_cong) / 4
    sinusite *= (w_dor + w_cong + w_temp) / 3
    covid *= (w_temp + w_tosse + w_musc + w_olf + w_fad + w_nau) / 6

    # Normaliza os resultados entre 0 e 100
    resultados = np.clip([gripe, resfriado, sinusite, covid], 0, 100)
    return resultados


# =============================
# INTERFACE TKINTER COM SCROLL
# =============================

root = tk.Tk()
root.title("Diagnóstico Fuzzy de Doenças Comuns")
root.geometry("900x600")

# ==== FRAME PRINCIPAL COM SCROLLBAR ====
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Permitir rolagem com o mouse
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int(e.delta / 120), "units"))

# Frame interno que conterá o conteúdo
content_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# =============================
# COMPONENTES DA INTERFACE
# =============================

tk.Label(content_frame, text="🩺 Sistema de Diagnóstico Fuzzy", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(content_frame, text="Ajuste os sintomas e pesos conforme necessário.", font=("Arial", 11)).pack(pady=5)

# Lista de sintomas
sintomas_labels = [
    "Temperatura (°C)", "Tosse", "Dor de cabeça", "Dor muscular",
    "Congestão nasal", "Perda de olfato", "Fadiga", "Náusea"
]

# Sliders de sintomas
sintomas_scales = []
for label in sintomas_labels:
    frame = tk.Frame(content_frame)
    frame.pack(pady=4)
    tk.Label(frame, text=label, width=20, anchor="w").pack(side=tk.LEFT)
    scale = tk.Scale(frame, from_=0, to=10, orient=tk.HORIZONTAL, length=400, resolution=0.1)
    scale.pack(side=tk.LEFT)
    sintomas_scales.append(scale)

tk.Label(content_frame, text="Pesos adaptativos (0–1)", font=("Arial", 13, "bold")).pack(pady=10)

# Sliders de pesos
pesos_scales = []
for label in sintomas_labels:
    frame = tk.Frame(content_frame)
    frame.pack(pady=3)
    tk.Label(frame, text=f"Peso de {label}", width=20, anchor="w").pack(side=tk.LEFT)
    scale = tk.Scale(frame, from_=0, to=1, orient=tk.HORIZONTAL, length=400, resolution=0.05)
    scale.set(1)  # peso padrão
    scale.pack(side=tk.LEFT)
    pesos_scales.append(scale)


# =============================
# FUNÇÕES DE EVENTO
# =============================

def calcular_diagnostico():
    sintomas = [s.get() for s in sintomas_scales]
    pesos = [p.get() for p in pesos_scales]

    resultados = diagnostico_fuzzy(sintomas, pesos)
    nomes = ["Gripe", "Resfriado", "Sinusite", "Covid-19"]

    # Exibe resultado textual
    texto = "\n".join([f"{doenca}: {valor:.1f}%" for doenca, valor in zip(nomes, resultados)])
    messagebox.showinfo("Resultado do Diagnóstico", texto)

    # Exibe gráfico
    plt.figure(figsize=(6, 4))
    plt.bar(nomes, resultados, color=["#2196F3", "#4CAF50", "#FFC107", "#F44336"])
    plt.ylim(0, 100)
    plt.title("Probabilidade estimada (%)")
    plt.ylabel("Grau de suspeita")
    plt.show()


# =============================
# BOTÃO DE EXECUÇÃO
# =============================

tk.Button(
    content_frame,
    text="Calcular Diagnóstico",
    font=("Arial", 13, "bold"),
    bg="#4CAF50",
    fg="white",
    command=calcular_diagnostico
).pack(pady=20)

tk.Label(
    content_frame,
    text="* Este sistema é apenas educativo e não substitui diagnóstico médico real.",
    font=("Arial", 9, "italic"),
    fg="gray"
).pack(pady=10)

root.mainloop()
