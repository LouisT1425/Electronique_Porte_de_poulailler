import serial
import tkinter as tk
from tkinter import ttk, StringVar
import time
import schedule


window = tk.Tk()
window.title("Contrôle du moteur")
window.geometry("900x600")

ser = serial.Serial('COM6', 9600)  # 'COM6' = port série

# Variable pour garder la trace de l'état de la porte
door_state = 'unknown'  # Les valeurs possibles sont 'open', 'closed', ou 'unknown'

# Label pour afficher l'état de la porte
state_label = tk.Label(window, text="État de la porte: Inconnu", font=("Arial", 16))
state_label.pack(pady=20)


def send_command(command):
    global door_state
    ser.write(command.encode())
    # Mettre à jour l'état de la porte en fonction de la commande envoyée
    if command == "1":
        door_state = 'transit'
        time.sleep(1.5)
        door_state = 'open'
    elif command == "2":
        door_state = 'transit'
        time.sleep(1.5)
        door_state = 'closed'
    update_state_label()


def update_state_label():
    if door_state == 'open':
        state_label.config(text="État de la porte: Ouverte")
    elif door_state == 'closed':
        state_label.config(text="État de la porte: Fermée")
    elif door_state == 'transit':
        state_label.config(text="État de la porte: En transit...")
    else:
        state_label.config(text="État de la porte: Inconnu")


# Modifier la taille des boutons
button_width = 30
button_height = 5

# Créer un frame pour centrer les boutons
frame = tk.Frame(window)
frame.pack(side="top", expand=True)


# Fonctions pour envoyer des commandes
def send_command_1():
    global door_state
    if door_state != 'open':
        send_command("1")
        print("Commande 1 envoyée")
    else:
        print("Erreur: La porte est déjà ouverte")


def send_command_2():
    global door_state
    if door_state != 'closed':
        send_command("2")
        print("Commande 2 envoyée")
    else:
        print("Erreur: La porte est déjà fermée")


def send_command_3():
    global door_state
    send_command("3")
    print("Calibrage en cours ...")
    time.sleep(2)
    door_state = 'open'
    update_state_label()
    print("Porte calibrée !")


# Fonction pour planifier l'envoi de commandes
def schedule_command(command, time_str):
    if command == "1":
        schedule.every().day.at(time_str).do(send_command_1)
    elif command == "2":
        schedule.every().day.at(time_str).do(send_command_2)


# Widgets pour choisir l'heure et planifier la commande 1
time_1 = StringVar()
time_1_entry = ttk.Entry(frame, textvariable=time_1, width=10)
time_1_entry.pack(pady=10, anchor="center")
schedule_button_1 = ttk.Button(frame, text="Planifier ouverture", command=lambda: schedule_command("1", time_1.get()), width=button_width)
schedule_button_1.pack(pady=10, anchor="center")

# Widgets pour choisir l'heure et planifier la commande 2
time_2 = StringVar()
time_2_entry = ttk.Entry(frame, textvariable=time_2, width=10)
time_2_entry.pack(pady=10, anchor="center")
schedule_button_2 = ttk.Button(frame, text="Planifier fermeture", command=lambda: schedule_command("2", time_2.get()), width=button_width)
schedule_button_2.pack(pady=10, anchor="center")


# Créer un frame pour les boutons en bas
bottom_frame = tk.Frame(window)
bottom_frame.pack(side="bottom", expand=True)

# Bouton pour ouvrir manuellement
manual_open = ttk.Button(bottom_frame, text="Ouvrir (Sens horaire)", command=send_command_1, width=button_width)
manual_open.pack(side="left", padx=20, pady=20)

# Bouton pour fermer manuellement
manual_close = ttk.Button(bottom_frame, text="Fermer (Sens anti-horaire)", command=send_command_2, width=button_width)
manual_close.pack(side="right", padx=20, pady=20)

calibrate = ttk.Button(bottom_frame, text="Calibrer", command=send_command_3, width=button_width)
calibrate.pack(side="right", padx=20, pady=20)


# Créer une fonction pour vérifier les tâches planifiées
def check_schedule():
    schedule.run_pending()
    window.after(1000, check_schedule)  # Vérifier toutes les secondes


# Démarrer la vérification des tâches planifiées
window.after(1000, check_schedule)

window.mainloop()

ser.close()
