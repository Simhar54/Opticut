# main.py
import tkinter as tk
from ui import OpticutUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Opticut")

    # Récupère la largeur et la hauteur de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Définit la largeur et la hauteur de la fenêtre
    window_width = 800
    window_height = 730

    # Calcule la position pour centrer la fenêtre
    position_top = 0
    position_right = int(screen_width/2 - window_width/2)

    # Positionne et dimensionne la fenêtre
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    root.resizable(width=False, height=False)

    # le reste de votre code


    app = OpticutUI(root)
    app.run()
