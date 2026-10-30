import pandas as pd
import matplotlib.pyplot as plt

# 1. Définition des colonnes 
colonnes = ['cycles_score', 'cycles_comp', 'comp_len', 'comp_score', 'algo', 'creator_pid']

# Chargement du fichier 
try:
    df = pd.read_csv('resultats_mixup.csv', names=colonnes, on_bad_lines='skip')
except FileNotFoundError:
    print("Erreur : Le fichier CSV est introuvable.")
    exit()

# 2. Filtrer les données pour garder uniquement les scores entre 0 et 4000
df = df[(df['comp_score'] >= 0) & (df['comp_score'] <= 4000)]

# 3. Création des tranches de 100 (0-100, 100-200, ..., 3900-4000)
# 'right=False' signifie que l'intervalle est [0, 100) : il inclut 0 mais exclut 100
tranches = range(0, 4100, 500)
df['tranche_score'] = pd.cut(df['comp_score'], bins=tranches, right=False)

# 4. Comptage du nombre de pages par tranche
# On groupe par la tranche, on compte la taille de chaque groupe, et on renomme la colonne
resultat = df.groupby('tranche_score').size().reset_index(name='nombre_de_pages')

# Pour avoir un affichage plus propre, on convertit l'intervalle en chaîne de caractères
resultat['tranche_score'] = resultat['tranche_score'].astype(str)

# 5. Affichage du résultat dans le terminal
print("--- RÉPARTITION DES PAGES PAR COMP_SCORE ---")
print(resultat.to_string(index=False))
print("-" * 45)
print(f"Total des pages analysées : {resultat['nombre_de_pages'].sum()}")

# 6. Génération d'un histogramme visuel
plt.figure(figsize=(14, 6))
# On extrait juste la limite inférieure de chaque tranche pour l'axe X (ex: 0 pour [0-100))
x_labels = [i.left for i in df['tranche_score'].cat.categories]
plt.bar(x_labels, resultat['nombre_de_pages'], width=90, align='edge', color='#1f77b4', edgecolor='black')

plt.title('Distribution des pages par score de compressibilité (Tranches de 100)', fontsize=14, pad=15)
plt.xlabel('Score de compressibilité (comp_score)', fontsize=12)
plt.ylabel('Nombre de pages compressées', fontsize=12)
plt.xticks(range(0, 4100, 200)) # Afficher une graduation tous les 200 pour la lisibilité
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Sauvegarde de l'image
plt.tight_layout()
plt.savefig('distribution_comp_score.png', dpi=300)
print("\nUn graphique visuel a été sauvegardé sous le nom 'distribution_comp_score.png'.")