
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from optimization import optimize_cutting


class OpticutUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Initialize attributes
        self.min_drop_length = None
        self.bar_lengths = []
        self.cut_lengths = []

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 12), padding=10)
        self.style.configure("TEntry", font=("Helvetica", 12), padding=10)
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TText", font=("Helvetica", 12), padding=10)

        self.create_menu()
        self.create_min_drop_length()
        self.create_bar_lengths()
        self.create_cut_lengths()
        self.create_optimize_button()

    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Reset")
        file_menu.add_command(label="Quitter", command=self.master.quit)
        menu_bar.add_cascade(label="Menu", menu=file_menu)
        self.master.config(menu=menu_bar)

    def create_min_drop_length(self):
        frame_min_drop_length = ttk.Frame(self)
        frame_min_drop_length.pack(pady=10, anchor="w")

        lbl_min_drop_length = ttk.Label(frame_min_drop_length, text="Longueur de chute minimale:")
        lbl_min_drop_length.pack(side="left")

        self.entry_min_drop_length = ttk.Entry(frame_min_drop_length)
        self.entry_min_drop_length.insert(0, "0")
        self.entry_min_drop_length.pack(side="left")
        self.entry_min_drop_length.bind("<Return>", lambda event: self.accept_min_drop_length())  # Accepter la valeur saisie si l'utilisateur appuie sur la touche Entrée

        self.min_error_message = ttk.Label(self)
        self.min_error_message.pack()

        self.btn_accept_min_drop_length = ttk.Button(frame_min_drop_length, text="Accepter", command=self.accept_min_drop_length)
        self.btn_accept_min_drop_length.pack(side="left", padx=5)

        self.btn_modify_min_drop_length = ttk.Button(frame_min_drop_length, text="Modifier", state="disabled", command=self.modify_min_drop_length)
        self.btn_modify_min_drop_length.pack(side="left", padx=5)

    def accept_min_drop_length(self):
        min_drop_length = self.entry_min_drop_length.get()

        # Vérification que la valeur n'est pas vide et est un entier
        if min_drop_length.isdigit():
            self.min_drop_length = int(min_drop_length)
            self.entry_min_drop_length.configure(state="disabled")  # Griser l'entrée
            self.btn_accept_min_drop_length.configure(state="disabled")  # Désactiver le bouton "Accepter"
            self.btn_modify_min_drop_length.configure(state="normal")  # Activer le bouton "Modifier"

        else:
            # Afficher un message d'erreur
            self.min_error_message.configure(text="Veuillez saisir une valeur entière valide pour la longueur de chute minimale.")

    def modify_min_drop_length(self):
        self.entry_min_drop_length.configure(state="normal")  # Réactiver l'entrée
        self.btn_accept_min_drop_length.configure(state="normal")  # Activer le bouton "Accepter"
        self.btn_modify_min_drop_length.configure(state="disabled")  # Désactiver le bouton "Modifier"



    def create_bar_lengths(self):
        frame_bar_lengths = ttk.Frame(self)
        frame_bar_lengths.pack(pady=10, anchor="w")

        lbl_bar_lengths = ttk.Label(frame_bar_lengths, text="Longueurs des barres à scier:")
        lbl_bar_lengths.pack(side="left")

        self.entry_bar_lengths = ttk.Entry(frame_bar_lengths)
        self.entry_bar_lengths.insert(0, "0")
        self.entry_bar_lengths.pack(side="left", padx=5)
        self.entry_bar_lengths.bind("<Return>", lambda event: self.add_bar_length())  # Ajouter la longueur de barre à la liste si l'utilisateur appuie sur la touche Entrée

        self.bar_error_message = ttk.Label(self)
        self.bar_error_message.pack()

        btn_add_bar_length = ttk.Button(frame_bar_lengths, text="Ajouter")
        btn_add_bar_length.pack(side="left", padx=5)
        btn_add_bar_length.configure(command=self.add_bar_length)

        btn_delete_bar_length = ttk.Button(frame_bar_lengths, text="Effacer la dernière barre", command=self.delete_last_bar_length)
        btn_delete_bar_length.pack(side="left", padx=5)

        self.bar_lengths_window = tk.Text(self, height=10, width=60)
        self.bar_lengths_window.pack()

         # Initialiser la liste des longueurs des barres à scier
        self.bar_lengths = []


    def add_bar_length(self, event=None):
        bar_length = self.entry_bar_lengths.get()

        # Vérification que la valeur n'est pas vide et est un entier
        if bar_length.isdigit() and int(bar_length) != 0:
            self.bar_lengths.append(int(bar_length))

            # Definir l'état de la fenêtre de texte comme 'normal' pour pouvoir ajouter du texte
            self.bar_lengths_window.config(state='normal')
            self.bar_lengths_window.insert(tk.END, f"{bar_length}\n")

            # Une fois que vous avez ajouté le texte, remettez l'état de la fenêtre de texte sur 'disabled' pour empêcher la saisie
            self.bar_lengths_window.config(state='disabled')
        else:
            # Afficher un message d'erreur
            self.bar_error_message.configure(text="Veuillez saisir une valeur entière valide et supérieur a zéro.")

        self.entry_bar_lengths.delete(0, tk.END)  # Effacer le champ de saisie après ajout


    def delete_last_bar_length(self):
        if self.bar_lengths:
            self.bar_lengths.pop()

            # Définir l'état de la fenêtre de texte comme 'normal' pour pouvoir supprimer du texte
            self.bar_lengths_window.config(state='normal')
            self.bar_lengths_window.delete("end-2l", "end-1l")

            # Une fois que vous avez supprimé le texte, remettez l'état de la fenêtre de texte sur 'disabled' pour empêcher la saisie
            self.bar_lengths_window.config(state='disabled')


    def create_cut_lengths(self):
        frame_cut_lengths = ttk.Frame(self)
        frame_cut_lengths.pack(pady=10, anchor="w")

        lbl_cut_lengths = ttk.Label(frame_cut_lengths, text="Longueurs des découpes:")
        lbl_cut_lengths.pack(side="left")

        self.entry_cut_lengths = ttk.Entry(frame_cut_lengths)
        self.entry_cut_lengths.insert(0, "0")
        self.entry_cut_lengths.pack(side="left", padx=5)
        self.entry_cut_lengths.bind("<Return>", lambda event: self.add_cut_length())  # Ajouter la longueur de découpe à la liste si l'utilisateur appuie sur la touche Entrée

        self.cut_error_message = ttk.Label(self)   
        self.cut_error_message.pack()

        btn_add_cut_length = ttk.Button(frame_cut_lengths, text="Ajouter")
        btn_add_cut_length.pack(side="left", padx=5)
        btn_add_cut_length.configure(command=self.add_cut_length)

        btn_delete_cut_length = ttk.Button(frame_cut_lengths, text="Effacer la dernière découpe", command=self.delete_last_cut_length)
        btn_delete_cut_length.pack(side="left", padx=5)

        self.cut_lengths_window = tk.Text(self, height=10, width=60)
        self.cut_lengths_window.pack()

        # Initialiser la liste des longueurs des découpes
        self.cut_lengths = []

    def add_cut_length(self, event=None):
        cut_length = self.entry_cut_lengths.get()

        # Vérification que la valeur n'est pas vide et est un entier
        if cut_length.isdigit() and int(cut_length) != 0:
            self.cut_lengths.append(int(cut_length))

            # Définir l'état de la fenêtre de texte comme 'normal' pour pouvoir ajouter du texte
            self.cut_lengths_window.config(state='normal')
            self.cut_lengths_window.insert(tk.END, f"{cut_length}\n")

            # Une fois que vous avez ajouté le texte, remettez l'état de la fenêtre de texte sur 'disabled' pour empêcher la saisie
            self.cut_lengths_window.config(state='disabled')
        else:
            # Afficher un message d'erreur
            self.cut_error_message.configure(text="Veuillez saisir une valeur entière valide et supérieur a zéro.")

        self.entry_cut_lengths.delete(0, tk.END)
 


    def delete_last_cut_length(self):
        if self.cut_lengths:
            self.cut_lengths.pop()

            # Définir l'état de la fenêtre de texte comme 'normal' pour pouvoir supprimer du texte
            self.cut_lengths_window.config(state='normal')
            self.cut_lengths_window.delete("end-2l", "end-1l")

            # Une fois que vous avez supprimé le texte, remettez l'état de la fenêtre de texte sur 'disabled' pour empêcher la saisie
            self.cut_lengths_window.config(state='disabled')

 

    def create_optimize_button(self):
        btn_optimize = ttk.Button(self, text="Optimiser")
        btn_optimize.pack(pady=10)

        def print_result():
            # vérifie si toutes les valeurs ne sont pas vides
            if self.bar_lengths and self.cut_lengths and self.min_drop_length is not None:
                 # vérifie si la liste des longueurs de coupe est vide
                if not self.cut_lengths:
                    messagebox.showinfo("Info", "Aucune coupe nécessaire, toutes les barres sont non utilisées.")
                    return

                # vérifie si la plus grande longueur de coupe est supérieure à la plus grande longueur de barre
                if max(self.cut_lengths) > max(self.bar_lengths):
                    messagebox.showerror("Erreur", "Aucune barre ne peut contenir la plus grande coupe demandée.")
                    return
                
                 # vérifie si la somme de toutes les longueurs de coupe est supérieure à la somme de toutes les longueurs de barre en tenant compte des chutes minimales
                total_bar_length = sum(self.bar_lengths) - len(self.bar_lengths) * self.min_drop_length
                if sum(self.cut_lengths) > total_bar_length:
                    messagebox.showerror("Erreur", "Il n'y a pas assez de barres pour toutes les coupes demandées en tenant compte des chutes minimales.")
                    return

                # création d'une nouvelle fenêtre
                new_window = tk.Toplevel(self)

                # appelle la fonction d'optimisation avec les valeurs actuelles
                cutting_plans = optimize_cutting(self.bar_lengths, self.cut_lengths, self.min_drop_length)

                # Parce qu'il n'y a qu'un seul élément dans cutting_plans, on peut utiliser items pour obtenir directement le nom de l'algorithme et les résultats
                for plan, results in cutting_plans.items():
                    # affiche le nom de l'algorithme
                    label_plan = tk.Label(new_window, text=plan)
                    label_plan.pack()

                    # Pour chaque résultat (qui est un dictionnaire)
                    for i, result in enumerate(results):
                        # affiche le numéro de la barre et sa longueur
                        label_bar = tk.Label(new_window, text=f"Barre {i+1} (longueur {result['length']}) :")
                        label_bar.pack()

                        # affiche les découpes
                        label_cuts = tk.Label(new_window, text="Coupes : " + ", ".join(str(cut) for cut in result["cuts"]))
                        label_cuts.pack()

                        # affiche le reste
                        label_remainder = tk.Label(new_window, text="Reste : " + str(result["remainder"]))
                        label_remainder.pack()

            else:
                # affiche un message d'erreur si une ou plusieurs valeurs sont vides
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

        btn_optimize.configure(command=print_result)




    def run(self):
        self.pack()
        self.master.mainloop()


