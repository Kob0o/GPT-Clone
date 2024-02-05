from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
import requests
import os
import json

# API AI
API_TOKEN = os.environ["HUGGINGFACE_API_KEY"]
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
# ---------------------------------------------------------------------------------
#  Fonction qui affiche le prompt à l'écran
def show_prompt_query():
    # Récupération de l'éntrée de l'utilisateur pour la réponse du bot
    rep = query(entry1.get())
    reponses = rep[0]["generated_text"]
    # Ajout de la réponse à la liste des réponses
    prompt = {
        "input": entry1.get(),
        "response": reponses
    }
    prompts.append(prompt)
    # appel de toute les fonctions utile à l'affichage des prompts
    update_text_widget(prompt)
    create_button_history(prompt)
    create_button_restart(prompt)
    save_prompts()
    entry1.delete(0, END)

# Creation du boutton pour l'historique des prompts
def create_button_history(prompt):
    button = Button(ButtonWidget, text=prompt["input"], command=lambda: show_old_prompt(prompt), width=20)
    button.pack(pady=5)

# Fonction pour remettre l'ancien prompt dans la fenêtre d'entrée
def show_prompt(prompt):
    entry1.delete(0, END)
    entry1.insert(0, prompt["input"])

def show_old_prompt(prompt):
    """
    Fonction qui permet l'exécution des trois autres fonctions ci-dessous
    permettant le réafichage des ancines proompts ainsi que la création d'un bouton restart
    """
    create_button_restart(prompt)
    show_prompt(prompt)
    update_text_widget(prompt)

# Function pour créer le bouton restart
def create_button_restart(prompt):
    restart = Button(f2, text="Restart", width=10, height=1, bg="white", fg="black",
                     command=lambda: restart_Prompt(prompt))
    restart.place(x=15, y=492)

# Fonction pour mettre à jour le contenu de la fenêtre d'affichage
def update_text_widget(prompt):
    text_widget.config(state="normal")
    text_widget.delete(1.0, "end-1c")
    text_widget.insert("end", "Prompt: " + prompt["input"] + "\n", "bold")
    text_widget.insert("end", "Reponse: " + prompt["response"] + "\n")
    text_widget.config(state="disabled")

# Fonction pour restart/Rejouer le prompt
def restart_Prompt(prompt):
    # Récupération de l'éntrée de l'utilisateur pour la réponse du bot
    rep = query(prompt["input"])
    reponses = rep[0]["generated_text"]
    # Ajout de la réponse à la liste des réponses
    prompt = {
        "input": prompt["input"],
        "response": reponses
    }
    prompts.append(prompt)
    update_text_widget(prompt)
    entry1.delete(0, END)

# Création de la fenêtre principale
app = tk.Tk()
app.title("GPT Clone")
app.geometry("800x600")
app.resizable(False, False)

# Création de la Frame où se trouvera l'historique des prompts
f1 = LabelFrame(app, bd=2, text="Historique", bg="#454444",foreground="white",
                relief="groove", width=250, height=600)
f1.pack(side=LEFT, padx=10, pady=10)

# Création de la Frame où se trouvera le chatbot et tous les prompts que l'on écrit
f2 = LabelFrame(app, bd=2, text="Chatbot", bg="grey",foreground="white",
                relief="groove", width=550, height=600)
f2.pack(side=LEFT, padx=10, pady=10)

# Création de la Frame où se trouvera les boutons pour l'historique des prompts
ButtonWidget = LabelFrame(f1, bd=2, bg="#454444",
                         relief="groove", width=240, height=570)
ButtonWidget.place(x=(f1.winfo_reqwidth() - ButtonWidget.winfo_reqwidth()) / 2, y=2)

# Création de la fenêtre d'entrée des prompts que l'on souhaite donner à notre bot
entry1 = Entry(f2, width=40, bg="white", fg="black")
entry1.place(x=15, y=520)
entry1.bind("<Return>", show_prompt_query)

# Création d'un bouton send
send = Button(f2, text="Envoyer", width=10, height=1, bg="white", fg="black", command=show_prompt_query)

send.place(x=400, y=520)

# Fenêtre où l'on affiche les prompts que l'on a donné à notre bot
text_widget = Text(f2, width=52, height=25, bg="grey", fg="white")
text_widget.place(x=15, y=10)

# Liste pour stocker les prompts et les réponses du bot (stock temporaire le temps que l'application tourne)
prompts = []

# Mise en place de la police d'écriture
fontExample = tkFont.Font(family="Arial", size=13, weight="normal", slant="roman")
entry1.configure(font=fontExample)
text_widget.configure(font=fontExample)
text_widget.config(state="disabled")
bold_police = ("Helvetica", 12, "bold")
text_widget.tag_configure("bold", font=bold_police)
# sauvegarde des prompts dans un fichier Json
def save_prompts():
    with open("./prompts.json", "w") as json_file:
        json.dump(prompts, json_file)
    print("Prompts enregistrés dans prompts.json")

# Charger le fichier Json lors de l'ouverture de l'app
def load_prompts():
    try:
        with open("./prompts.json", "r") as json_file:
            loaded_prompts = json.load(json_file)
            prompts.extend(loaded_prompts)
            for prompt in prompts:
                create_button_history(prompt)
    except FileNotFoundError:
        print("Fichier prompts.json introuvable")

load_prompts()
# Mise en route de notre application
app.mainloop()
