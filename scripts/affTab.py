import pandas as pd
import matplotlib.pyplot as plt

# 1. Chargement des données avec les noms de colonnes 
noms_colonnes = ['cycles_score', 'cycles_comp', 'comp_len', 'comp_score', 'algo_id', 'creator_pid']

try:
    df = pd.read_csv('resultats_mixupRedisLZ4HC.csv', names=noms_colonnes, on_bad_lines='skip')
except FileNotFoundError:
    print("Erreur : Le fichier 'resultats_mixup.csv' est introuvable.")
    exit()

# 2. CALCULS DES NOUVELLES MÉTRIQUES
df['cycles_totaux'] = df['cycles_score'] + df['cycles_comp']
# AJOUT ICI : LZ4HC mappé sur l'ID 2
df['Nom_Algo'] = df['algo_id'].map({1:'LZ4', 4: 'deflate', 1: 'ZSTD', 0: 'LZ4HC',1: 'LZO'})

# 3. AGRÉGATION DES DONNÉES 
tableau_donnees = []

for algo_name in df['Nom_Algo'].dropna().unique():
    df_algo = df[df['Nom_Algo'] == algo_name]
    if not df_algo.empty:
        tableau_donnees.append([
            algo_name,
            f"{len(df_algo):,}".replace(",", " "),
            f"{round(df_algo['comp_len'].sum() / (1024 * 1024), 2):,}".replace(",", " "),
            f"{df_algo['cycles_totaux'].sum():,}".replace(",", " "),
            f"{int(df_algo['cycles_totaux'].mean()):,}".replace(",", " ")
        ])

tableau_donnees.append([
    'TOTAL SYSTEME',
    f"{len(df):,}".replace(",", " "),
    f"{round(df['comp_len'].sum() / (1024 * 1024), 2):,}".replace(",", " "),
    f"{df['cycles_totaux'].sum():,}".replace(",", " "),
    f"{int(df['cycles_totaux'].mean()):,}".replace(",", " ")
])

# En-têtes correspondants aux colonnes
en_tetes = [
    'Groupe/Algorithme', 
    'Nombre Total de Pages', 
    'Totale Compressée (Mo)', 
    'Cycles CPU Totaux', 
    'Cycles Moyens par Page'
]

# 4. CRÉATION DU TABLEAU GRAPHIQUE 
fig, ax = plt.subplots(figsize=(12, 2.5))
ax.axis('off') # Masquer les axes X/Y pour ne garder que le tableau

# Dessiner le tableau graphique
table_visuelle = ax.table(
    cellText=tableau_donnees, 
    colLabels=en_tetes, 
    loc='center', 
    cellLoc='center'
)

# PERSONNALISATION ET STYLE GRAPHIQUE 
table_visuelle.auto_set_font_size(False)
table_visuelle.set_fontsize(10)
table_visuelle.scale(1.2, 2.2) # Ajustement de la largeur des colonnes et hauteur des lignes

for col_idx in range(len(en_tetes)):
    cellule_header = table_visuelle[0, col_idx]
    cellule_header.set_text_props(weight='bold', color='white')
    cellule_header.set_facecolor('#1f77b4') 

for col_idx in range(len(en_tetes)):
    cellule_total = table_visuelle[len(tableau_donnees), col_idx]
    cellule_total.set_text_props(weight='bold')
    cellule_total.set_facecolor('#f2f2f2')

# Sauvegarde propre de l'image
plt.tight_layout()
plt.savefig('tableau_performances_zswapRedisLZ4HC.png', dpi=300, bbox_inches='tight')
plt.close()

print("Le tableau graphique visuel a été généré avec succès sous le nom 'tableau_performances_zswap.png'.")