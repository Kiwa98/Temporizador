import serial
import time
import threading
import tkinter as tk
from tkinter import ttk
from pynput import keyboard

# =========================
# CONFIGURAÇÕES
# =========================
porta_selecionada = "COM7"
BAUDRATE = 9600
arduino = None

# =========================
# CONTROLE DO SISTEMA
# =========================
sistema_ativo = False
esteira_ligada = False

tempo_esteira_ligada = 5
tempo_esteira_parada = 5

tempo_restante_ciclo = 0.0
modo_temporizador = "---"

lock = threading.Lock()

# =========================
# FUNÇÕES DE CONTROLE
# =========================
def ligar_esteira():
    global esteira_ligada
    if not esteira_ligada:
        if arduino:
            arduino.write(b"ESTEIRA_ON\n")
        esteira_ligada = True
        log("🚀 Esteira LIGADA")


def parar_esteira():
    global esteira_ligada
    if esteira_ligada:
        if arduino:
            arduino.write(b"ESTEIRA_OFF\n")
        esteira_ligada = False
        log("⏸ Esteira PARADA")


# =========================
# CICLO AUTOMÁTICO
# =========================
def controle_ciclo():
    global tempo_restante_ciclo, modo_temporizador

    while True:
        if sistema_ativo:

            # ===== LIGADA =====
            ligar_esteira()
            modo_temporizador = "LIGADA"

            inicio = time.time()
            while time.time() - inicio < tempo_esteira_ligada:
                with lock:
                    tempo_restante_ciclo = tempo_esteira_ligada - (time.time() - inicio)
                time.sleep(0.1)

            # ===== PARADA =====
            parar_esteira()
            modo_temporizador = "PARADA"

            inicio = time.time()
            while time.time() - inicio < tempo_esteira_parada:
                with lock:
                    tempo_restante_ciclo = tempo_esteira_parada - (time.time() - inicio)
                time.sleep(0.1)

        else:
            time.sleep(0.1)


# =========================
# ATUALIZAÇÃO DA UI (THREAD SAFE)
# =========================
def atualizar_ui():
    with lock:
        status_esteira.config(
            text="Esteira: LIGADA ✅" if esteira_ligada else "Esteira: PARADA ⛔",
            fg="green" if esteira_ligada else "red"
        )

        status_temporizador.config(
            text=f"Ciclo {modo_temporizador}: {tempo_restante_ciclo:.1f}s"
            if sistema_ativo else "Ciclo: ---"
        )

    root.after(100, atualizar_ui)


# =========================
# LOG
# =========================
def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)


# =========================
# ENTER → LUZ VERDE
# =========================
def on_press(key):
    if key == keyboard.Key.enter:
        if arduino:
            arduino.write(b"LUZ_VERDE_PULSO\n")
        log("💡 ENTER → Luz verde (0,5s)")


def iniciar_listener_teclado():
    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()


# =========================
# INICIAR SISTEMA
# =========================
def iniciar():
    global arduino, sistema_ativo
    try:
        arduino = serial.Serial(porta_selecionada, BAUDRATE, timeout=1)
        sistema_ativo = True
        log(f"✅ Sistema iniciado na porta {porta_selecionada}")
        iniciar_listener_teclado()
    except:
        log("❌ Erro ao abrir porta serial")


# =========================
# INTERFACE
# =========================
root = tk.Tk()
root.title("Temporizador da Esteira")

frame_left = tk.Frame(root)
frame_left.pack(side="left", padx=10, pady=10)

frame_right = tk.Frame(root)
frame_right.pack(side="right", padx=10, pady=10)

log_box = tk.Text(frame_left, width=60, height=20)
log_box.pack()

status_esteira = tk.Label(frame_right, text="Esteira: ---", font=("Arial", 12))
status_esteira.pack(pady=5)

status_temporizador = tk.Label(frame_right, text="Ciclo: ---", font=("Arial", 12), fg="blue")
status_temporizador.pack(pady=5)

# Porta COM
tk.Label(frame_right, text="Porta COM").pack()
combo_porta = ttk.Combobox(frame_right, values=[f"COM{i}" for i in range(1, 10)], state="readonly")
combo_porta.set(porta_selecionada)
combo_porta.pack()

def selecionar_porta(e):
    global porta_selecionada
    porta_selecionada = combo_porta.get()

combo_porta.bind("<<ComboboxSelected>>", selecionar_porta)

# Tempos
tk.Label(frame_right, text="Tempo LIGADA (s)").pack()
campo_ligada = ttk.Combobox(frame_right, values=list(range(1, 2000)), state="readonly")
campo_ligada.set(5)
campo_ligada.pack()

campo_ligada.bind("<<ComboboxSelected>>",
                  lambda e: globals().update(tempo_esteira_ligada=int(campo_ligada.get())))

tk.Label(frame_right, text="Tempo PARADA (s)").pack()
campo_parada = ttk.Combobox(frame_right, values=list(range(1, 2000)), state="readonly")
campo_parada.set(5)
campo_parada.pack()

campo_parada.bind("<<ComboboxSelected>>",
                  lambda e: globals().update(tempo_esteira_parada=int(campo_parada.get())))

# Botão
tk.Button(frame_right, text="▶️ Iniciar Sistema", command=iniciar, width=20).pack(pady=10)

# =========================
# THREADS
# =========================
threading.Thread(target=controle_ciclo, daemon=True).start()
root.after(100, atualizar_ui)

root.mainloop()
