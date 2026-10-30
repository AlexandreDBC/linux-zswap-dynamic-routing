import pandas as pd
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# 1. Définition des fichiers CSV
# ─────────────────────────────────────────────
noms_colonnes = ['cycles_score', 'cycles_comp', 'comp_len', 'comp_score', 'algo', 'creator_pid']

fichiers_avant = [
    'resultats_mixup250k-75k.csv',
    'resultats_mixup350k-100k.csv',
    'resultats_mixup500k-150k.csv',
    'resultats_mixup750k-250k-limitcrashOOT.csv',
]

fichiers_apres = [
    'resultats_mixupgeneric250k-75k.csv',
    'resultats_mixupgeneric350k-100k.csv',
    'resultats_mixupgeneric500k-150k.csv',
    'resultats_mixupGeneric750k-250k-limitcrashOOT.csv',
]

# ─────────────────────────────────────────────
# 2. Chargement
# ─────────────────────────────────────────────
def charger_et_combiner(fichiers):
    frames = []
    for f in fichiers:
        try:
            df = pd.read_csv(f, names=noms_colonnes, on_bad_lines='skip')
            frames.append(df)
        except FileNotFoundError:
            print(f"Fichier introuvable : {f}")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

df_avant = charger_et_combiner(fichiers_avant)
df_apres = charger_et_combiner(fichiers_apres)

# ─────────────────────────────────────────────
# 3. Stats ZSTD uniquement (algo == 1)
# ─────────────────────────────────────────────
zstd_avant = df_avant[df_avant['algo'] == 1]['cycles_comp']
zstd_apres = df_apres[df_apres['algo'] == 1]['cycles_comp']

cycles_avant = round(zstd_avant.mean(), 1)
cycles_apres = round(zstd_apres.mean(), 1)

amelio = ((cycles_avant - cycles_apres) / cycles_avant * 100) if cycles_avant > 0 else 0
amelio_str = f"+{amelio:.2f}%" if amelio >= 0 else f"{amelio:.2f}%"
couleur_amelio = "#2ecc71" if amelio >= 0 else "#e74c3c"

# ─────────────────────────────────────────────
# 4. Tableau graphique
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 2.5))
ax.axis('off')

colonnes = [
    'Algorithme',
    'Cycles/page AVANT',
    'Cycles/page APRÈS',
    'Amélioration'
]

donnees = [[
    'ZSTD',
    f"{cycles_avant:,.1f}",
    f"{cycles_apres:,.1f}",
    amelio_str,
]]

table = ax.table(
    cellText=donnees,
    colLabels=colonnes,
    cellLoc='center',
    loc='center',
)

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 2.5)

# Style en-têtes
for col in range(len(colonnes)):
    table[0, col].set_facecolor('#2c3e50')
    table[0, col].set_text_props(color='white', fontweight='bold')

# Style ligne données
for col in range(len(colonnes)):
    table[1, col].set_facecolor('#f0f4f8')
    table[1, col].set_text_props(fontweight='bold')

# Couleur amélioration
table[1, 3].set_facecolor(couleur_amelio)
table[1, 3].set_text_props(color='white', fontweight='bold')

plt.title(
    "Performances ZSTD — Avant vs Après patch",
    fontsize=13,
    fontweight='bold',
    pad=20,
    color='#2c3e50'
)

plt.tight_layout()
plt.savefig('tableau_zstd.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

print(f"ZSTD avant : {cycles_avant:,.1f} cycles/page")
print(f"ZSTD après : {cycles_apres:,.1f} cycles/page")
print(f"Amélioration : {amelio_str}")