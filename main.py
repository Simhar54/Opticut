# main.py
import tkinter as tk
from ui import OpticutUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Opticut")
    root.geometry("800x1000")  # Définir la taille de la fenêtre principale
    root.resizable(width=False, height=False)

    app = OpticutUI(root)
    app.run()
