def first_fit(bar_lengths, cut_lengths, min_drop_length):
    # Soustrait min_drop_length de chaque barre
    bar_lengths = [bar - min_drop_length for bar in bar_lengths]
    
    # Trie les longueurs de découpe dans l'ordre décroissant
    cut_lengths.sort(reverse=True)
    
    # Prépare la liste des barres utilisées
    bins = []
    
    # Parcourt chaque longueur de découpe
    for i in range(len(cut_lengths)):
        # Parcourt chaque barre déjà utilisée
        for j in range(len(bins)):
            # Si la découpe peut être réalisée sur cette barre
            if bins[j]["remainder"] >= cut_lengths[i]:
                # Ajoute la découpe à la liste des découpes pour cette barre
                bins[j]["cuts"].append(cut_lengths[i])
                # Met à jour le reste de la barre
                bins[j]["remainder"] -= cut_lengths[i]
                break
        # Si aucune barre n'a été trouvée pour la découpe, utilise une nouvelle barre
        else:
            # Trouve la plus petite barre qui peut contenir la découpe
            bar = min(bar for bar in bar_lengths if bar >= cut_lengths[i])
            # Retire cette barre de la liste des barres
            bar_lengths.remove(bar)
            # Ajoute la barre à la liste des barres utilisées
            bins.append({"cuts": [cut_lengths[i]], "remainder": bar - cut_lengths[i], "length": bar + min_drop_length})
    
    # Ajoute les barres restantes non utilisées à la fin de la liste des barres utilisées
    for bar in bar_lengths:
        bins.append({"cuts": [], "remainder": bar + min_drop_length, "length": bar + min_drop_length})  # remainder et length sont les mêmes ici
    
    # Ajoute min_drop_length au reste de chaque barre dans les résultats
    for bin in bins:
        if bin["cuts"]:  # Si la barre a été utilisée
            bin["remainder"] += min_drop_length
    
    return bins



def best_fit(bar_lengths, cut_lengths, min_drop_length):
    # Soustrait min_drop_length de chaque barre
    bar_lengths = [bar - min_drop_length for bar in bar_lengths]
    
    # Trie les longueurs de découpe dans l'ordre décroissant
    cut_lengths.sort(reverse=True)

    # Prépare la liste des barres utilisées
    bins = []

    # Parcourt chaque longueur de découpe
    for i in range(len(cut_lengths)):
        # Trouve la barre avec le plus petit reste qui peut encore contenir la découpe
        best_fit_index = -1
        min_remainder = float('inf')

        for j in range(len(bins)):
            if bins[j]["remainder"] >= cut_lengths[i] and bins[j]["remainder"] - cut_lengths[i] < min_remainder:
                best_fit_index = j
                min_remainder = bins[j]["remainder"] - cut_lengths[i]

        if best_fit_index != -1:
            # Ajoute la découpe à la liste des découpes pour cette barre
            bins[best_fit_index]["cuts"].append(cut_lengths[i])
            # Met à jour le reste de la barre
            bins[best_fit_index]["remainder"] -= cut_lengths[i]
        else:
            # Si aucune barre n'a été trouvée pour la découpe, utilise une nouvelle barre
            bar = min(bar for bar in bar_lengths if bar >= cut_lengths[i])
            bar_lengths.remove(bar)
            # Ajoute la barre à la liste des barres utilisées
            bins.append({"cuts": [cut_lengths[i]], "remainder": bar - cut_lengths[i], "length": bar + min_drop_length})

    # Ajoute les barres non utilisées
    for bar in bar_lengths:
        bins.append({"cuts": [], "remainder": bar + min_drop_length, "length": bar + min_drop_length})

    # Ajoute la valeur de min_drop_length à chaque barre restante
    for bin in bins:
        if bin["cuts"]:  # Si la barre a été utilisée
            bin["remainder"] += min_drop_length

    return bins


def next_fit(bar_lengths, cut_lengths, min_drop_length):
    # Trie les longueurs de découpe dans l'ordre décroissant
    cut_lengths.sort(reverse=True)

    # Prépare la liste des barres utilisées
    bins = [{"cuts": [], "remainder": min(bar_lengths), "length": min(bar_lengths)}]
    current_bin = 0

    # Retire la première barre de bar_lengths car elle est déjà utilisée
    bar_lengths.remove(min(bar_lengths))

    # Parcourt chaque longueur de découpe
    for i in range(len(cut_lengths)):
        # Si la découpe peut être réalisée sur la barre courante
        if bins[current_bin]["remainder"] >= cut_lengths[i]:
            # Ajoute la découpe à la liste des découpes pour cette barre
            bins[current_bin]["cuts"].append(cut_lengths[i])
            # Met à jour le reste de la barre
            bins[current_bin]["remainder"] -= cut_lengths[i]
        else:
            # Si la découpe ne peut pas être réalisée sur la barre courante, utilise une nouvelle barre
            bar = min(bar for bar in bar_lengths if bar >= cut_lengths[i])
            # Retire la barre de bar_lengths car elle va être utilisée
            bar_lengths.remove(bar)
            # Ajoute la barre à la liste des barres utilisées
            bins.append({"cuts": [cut_lengths[i]], "remainder": bar - cut_lengths[i], "length": bar})
            current_bin += 1

    # Ajoute les barres non utilisées
    for bar in bar_lengths:
        bins.append({"cuts": [], "remainder": bar, "length": bar})

    # Ajoute la valeur de min_drop_length à chaque barre restante
    for bin in bins:
        if bin["cuts"]:  # Si la barre a été utilisée
            bin["remainder"] += min_drop_length

    return bins





def optimize_cutting(bar_lengths, cut_lengths, min_drop_length):
    # Exécute les trois algorithmes et stocke leurs résultats
    result_ff = first_fit(bar_lengths, cut_lengths, min_drop_length)
    result_bf = best_fit(bar_lengths, cut_lengths, min_drop_length)
    result_nf = next_fit(bar_lengths, cut_lengths, min_drop_length)

    # Stocke les résultats dans un dictionnaire
    results = {"First-Fit": result_ff, "Best-Fit": result_bf, "Next-Fit": result_nf}

    # Étape 1 : Trouve l'algorithme qui utilise le moins de barres
    min_bars = min(len(results[algo]) for algo in results)
    best_algos = [algo for algo in results if len(results[algo]) == min_bars]

    # S'il y a un seul meilleur algorithme, renvoie son résultat
    if len(best_algos) == 1:
        return {best_algos[0]: results[best_algos[0]]}

    # Étape 2 : Parmi les algorithmes restants, trouve celui qui laisse la plus grande chute individuelle
    max_remainder = max(max(bar["remainder"] for bar in results[algo]) for algo in best_algos)
    best_algo = [algo for algo in best_algos if max(bar["remainder"] for bar in results[algo]) == max_remainder][0]

    # Renvoie le meilleur résultat
    return {best_algo: results[best_algo]}

