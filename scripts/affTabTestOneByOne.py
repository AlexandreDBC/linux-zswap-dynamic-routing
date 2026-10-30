import pandas as pd
import matplotlib.pyplot as plt

# 1. Définition des paires de fichiers CSV
noms_colonnes = ['cycles_score', 'cycles_comp', 'comp_len', 'comp_score', 'algo', 'creator_pid']

paires = [
    {
        'label'  : '250k-75k',
        'avant'  : 'resultats_mixup250k-75k.csv',
        'apres'  : 'resultats_mixupgeneric250k-75k.csv',
    },
    {
        'label'  : '350k-100k',
        'avant'  : 'resultats_mixup350k-100k.csv',
        'apres'  : 'resultats_mixupgeneric350k-100k.csv',
    },
    {
        'label'  : '500k-150k',
        'avant'  : 'resultats_mixup500k-150k.csv',
        'apres'  : 'resultats_mixupgeneric500k-150k.csv',
    },
    {
        'label'  : '750k-250k',
        'avant'  : 'resultats_mixup750k-250k-limitcrashOOT.csv',
        'apres'  : 'resultats_mixupGeneric750k-250k-limitcrashOOT.csv',
    },
]

# 2. Calcul des stats ZSTD par paire
def cycles_moyen_zstd(fichier):
    try:
        df = pd.read_csv(fichier, names=noms_colonnes, on_bad_lines='skip')
        zstd = df[df['algo'] == 1]['cycles_comp']
        return round(zstd.mean(), 1) if len(zstd) > 0 else 0
    except FileNotFoundError:
        print(f"Fichier introuvable : {fichier}")
        return 0

resultats = []
for paire in paires:
    avant = cycles_moyen_zstd(paire['avant'])
    apres = cycles_moyen_zstd(paire['apres'])
    amelio = ((avant - apres) / avant * 100) if avant > 0 else 0
    amelio_str = f"+{amelio:.2f}%" if amelio >= 0 else f"{amelio:.2f}%"
    resultats.append({
        'label'   : paire['label'],
        'avant'   : avant,
        'apres'   : apres,
        'amelio'  : amelio,
        'amelio_str' : amelio_str,
    })

# 3. Tableau graphique
fig, ax = plt.subplots(figsize=(10, 1.2 * (len(paires) + 1) + 1))
ax.axis('off')

colonnes = [
    'Test',
    'Cycles/page AVANT',
    'Cycles/page APRÈS',
    'Amélioration'
]

donnees = []
couleurs_amelio = []
for r in resultats:
    donnees.append([
        r['label'],
        f"{r['avant']:,.1f}",
        f"{r['apres']:,.1f}",
        r['amelio_str'],
    ])
    couleurs_amelio.append("#2ecc71" if r['amelio'] >= 0 else "#e74c3c")

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

couleurs_lignes = ['#f0f4f8', '#e8ecf0']
for row in range(len(resultats)):
    for col in range(len(colonnes)):
        table[row + 1, col].set_facecolor(couleurs_lignes[row % 2])
        table[row + 1, col].set_text_props(fontweight='bold')
    table[row + 1, 3].set_facecolor(couleurs_amelio[row])
    table[row + 1, 3].set_text_props(color='white', fontweight='bold')

plt.title(
    "Comparaison ZSTD par test Avant vs Après patch",
    fontsize=13,
    fontweight='bold',
    pad=20,
    color='#2c3e50'
)

plt.tight_layout()
plt.savefig('tableau_zstd_par_test.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

print("\n" + "="*60)
print("  ZSTD — Comparaison par test")
print("="*60)
for r in resultats:
    print(f"  {r['label']:20s} | avant: {r['avant']:>12,.1f} | après: {r['apres']:>12,.1f} | {r['amelio_str']}")
print("="*60)