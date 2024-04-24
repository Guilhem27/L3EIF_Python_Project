
### Interface graphique dans laquelle l'utilisateur va indiquer les paramètres de la startégie utilisée pour le test

#import tkinter as tk
#from tkinter import ttk
#import subprocess
#import csv

#dictionnaire_pays = {}
#with open('Documents/code/projet_eif/L3EIF_Python_Project/data_lists/physical_currency_list.csv', mode='r') as fichier_csv:
 #   lecteur_csv = csv.reader(fichier_csv)
  #  for pays in lecteur_csv:
   #     tuple_ligne = tuple(pays)
        
        # Utiliser la première valeur comme clé dans le dictionnaire
    #    cle = tuple_ligne[1]
        
        # Ajouter le tuple au dictionnaire
     #   dictionnaire_pays[cle] = tuple_ligne[0]


#def start_backtest():
    # Récupérer les valeurs des paramètres saisis par l'utilisateur

#    param2_value = param2_entry.get()
    
    # Appeler le programme de backtest avec les paramètres spécifiés
#    command = ["python", "backtest.py", param2_label, param2_value]
 #   result = subprocess.run(command, capture_output=True, text=True)
    
    # Afficher la sortie du backtest dans la console
  #  print(result.stdout)

# Créer une fenêtre principale
#root = tk.Tk()
#root.title("Paramétrage du backtest")


# Créer des libellés et des champs de saisie pour les paramètres


#param2_label = ttk.Label(root, text="Paramètre 2:")
#param2_label.grid(row=1, column=0, padx=5, pady=5)
#param2_entry = ttk.Entry(root)
#param2_entry.grid(row=1, column=1, padx=5, pady=5)

# Créer un bouton pour démarrer le backtesting
#start_button = ttk.Button(root, text="Démarrer Backtest", command=start_backtest)
#start_button.grid(row=2, columnspan=2, padx=5, pady=5)

# Lancer la boucle principale de l'interface utilisateur
#root.mainloop()