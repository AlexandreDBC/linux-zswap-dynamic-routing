import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, ScalarFormatter

noms_colonnes = ['cycles_score', 'cycles_comp', 'comp_len', 'comp_score', 'algo_id', 'creator_pid']

df = pd.read_csv('resultats_mixup.csv', names=noms_colonnes, on_bad_lines='skip')

# Utilisation de l'index comme axe de progression (ordre des événements)
df['temps_s'] = df.index

# Sous-échantillonnage 
df_opt = df.iloc[::5]
df_lzo  = df_opt[df_opt['algo_id'] == 0]
df_zstd = df_opt[df_opt['algo_id'] == 1]

# Figure
fig, ax = plt.subplots(figsize=(20, 6))

# Affichage des points (Axe Y = comp_len)
ax.plot(df_lzo['temps_s'],  df_lzo['comp_len'],
        'o', ms=0.5, alpha=0.4, color='#1f77b4', label='LZO')
ax.plot(df_zstd['temps_s'], df_zstd['comp_len'],
        'o', ms=0.5, alpha=0.4, color='#ff7f0e', label='ZSTD')

# Axe X calé dynamiquement du premier au dernier événement
ax.set_xlim(df['temps_s'].min(), df['temps_s'].max())

# Ajustement automatique de l'axe Y pour la taille des pages (octets)
ax.set_ylim(df['comp_len'].min() * 0.9, df['comp_len'].max() * 1.1)

# Graduations automatiques
ax.xaxis.set_major_locator(MaxNLocator(nbins=20))
formatter = ScalarFormatter(useOffset=False)
formatter.set_scientific(False)
ax.xaxis.set_major_formatter(formatter)

ax.grid(True, linestyle='-', alpha=0.5, color='gray')
ax.set_title("Évolution de la taille des pages compressées par zswap", fontsize=11)
ax.set_xlabel("Progression chronologique (Index séquentiel des compressions)", fontsize=9)
ax.set_ylabel("Taille de la page compressée (Octets)", fontsize=9)  
ax.legend(loc='upper right', fontsize=8, markerscale=15)

plt.tight_layout()
plt.savefig('graphique_mixup.png', dpi=300)
plt.show()
plt.close()