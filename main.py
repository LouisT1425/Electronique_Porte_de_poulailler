import serial
import tkinter as tk
from tkinter import ttk
import time

start_time = time.time()

window = tk.Tk()
window.title("Contrôle du moteur")
window.geometry("900x600")

ser = serial.Serial('COM6', 9600)  # 'COM6' = port série

def send_command(command):
    ser.write(command.encode())

# Modifier la taille des boutons
button_width = 30
button_height = 5

# Créer un frame pour centrer les boutons
frame = tk.Frame(window)
frame.pack(side="top", expand=True)

clockwise_button = ttk.Button(frame, text="Sens horaire", command=lambda: send_command("1"), width=button_width)
clockwise_button.pack(pady=20, anchor="center")

counter_clockwise_button = ttk.Button(frame, text="Sens anti-horaire", command=lambda: send_command("2"), width=button_width)
counter_clockwise_button.pack(anchor="center")



window.mainloop()

ser.close()
