import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def detect_and_clusterize_zswap(csv_file, min_algos=1, max_algos=2, seuil_silhouette=0.40):
    print(f"Analyse du fichier : {csv_file}")

    noms_colonnes = ['cycles_score', 'cycles_comp', 'comp_len', 'comp_score', 'algo_id', 'creator_pid']
    colonne_x = 'comp_score'
    colonne_y = 'comp_len'

    try:
        test_df = pd.read_csv(csv_file, nrows=1)
        if 'comp_score' in test_df.columns:
            df = pd.read_csv(csv_file)
        else:
            df = pd.read_csv(csv_file, names=noms_colonnes, header=None)

        df = df.dropna(subset=[colonne_x, colonne_y])

        if len(df) > 3000:
            df = df.sample(n=3000, random_state=42)

        features = df[[colonne_x, colonne_y]]

    except Exception as e:
        print(f"Erreur lors de la lecture du CSV : {e}")
        return

    print(f"{len(df)} pages chargées. Recherche du nombre optimal d'algorithmes (entre {min_algos} et {max_algos})...")

    best_n_algos = 1
    best_score = -1
    
    if max_algos >= 2:
        start_k = max(2, min_algos)
        for k in range(start_k, max_algos + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(features)
            score = silhouette_score(features, labels)
            print(f"Test avec {k} algorithmes : Score = {score:.4f}")
            
            if score > best_score:
                best_score = score
                best_n_algos = k
                
        if min_algos == 1 and best_score < seuil_silhouette:
            print(f"\nLe meilleur score ({best_score:.4f}) est inférieur au seuil de {seuil_silhouette}.")
            print("Les données ne forment pas de groupes distincts évidents.")
            best_n_algos = 1
            best_score = 0

    if best_n_algos == 1:
        print("\nDétection terminée : Un seul algorithme global est recommandé.")
    else:
        print(f"\nDétection terminée : Le nombre optimal d'algorithmes est de {best_n_algos} (Score: {best_score:.4f})")

    kmeans = KMeans(n_clusters=best_n_algos, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(features)

    centers = kmeans.cluster_centers_
    sorted_idx = sorted(range(best_n_algos), key=lambda i: centers[i][0])
    label_mapping = {old_idx: new_idx for new_idx, old_idx in enumerate(sorted_idx)}
    df['Algo_ID_Calc'] = df['Cluster'].map(label_mapping)

    sorted_centers_x = [centers[i][0] for i in sorted_idx]
    sorted_centers_y = [centers[i][1] for i in sorted_idx]

    print(f"\nRépartition pour {best_n_algos} algorithme(s) :")
    for i in range(best_n_algos):
        count = len(df[df['Algo_ID_Calc'] == i])
        pourcentage = (count / len(df)) * 100
        print(f"Algo {i} (Centre X: {int(sorted_centers_x[i])}) : {count} pages ({pourcentage:.1f}%)")

    if best_n_algos > 1:
        thresholds = []
        for i in range(best_n_algos - 1):
            seuil = (sorted_centers_x[i] + sorted_centers_x[i+1]) / 2
            thresholds.append(int(seuil))
            
        thresholds_str = ",".join(map(str, thresholds))
        print("\nCommande pour le noyau Linux :")
        print(f'echo "{thresholds_str}" | sudo tee /sys/module/zswap/parameters/thresholds')
    else:
        print("\nUn seul algorithme est nécessaire. Aucun seuil de routage kernel à configurer.")

    plt.figure(figsize=(10, 7))
    colors = ['#3498db', '#2ecc71', '#f1c40f', '#e74c3c', '#9b59b6', '#e67e22']

    for i in range(best_n_algos):
        subset = df[df['Algo_ID_Calc'] == i]
        plt.scatter(
            subset[colonne_x], subset[colonne_y],
            s=15, alpha=0.6,
            color=colors[i % len(colors)],
            label=f'Algo {i}'
        )

    plt.scatter(
        sorted_centers_x, sorted_centers_y,
        s=120, color='black', marker='o',
        edgecolor='white', linewidth=1.5,
        zorder=5, label='Centres'
    )

    plt.title(f"Clustering optimal Zswap : {best_n_algos} Algorithme(s)", fontsize=15)
    plt.xlabel("Score de compressibilité (comp_score)", fontsize=12)
    plt.ylabel("Taille compressée (comp_len)", fontsize=12)
    
    plt.xlim(0, 4500)
    plt.ylim(0, 4500)
    
    if best_n_algos > 1:
        plt.legend()
        
    plt.grid(alpha=0.2)
    plt.tight_layout()

    plt.savefig("clusterRedisZSTD.png", dpi=300)
    print("\nGraphique généré et sauvegardé sous 'cluster.png'")

if __name__ == "__main__":
    detect_and_clusterize_zswap(csv_file='resultats_mixupRedisZSTD.csv', min_algos=1, max_algos=6, seuil_silhouette=0.40)