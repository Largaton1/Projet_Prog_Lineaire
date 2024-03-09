import pulp

def initialiser_probleme():
    # Paramètres du problème
    demandes = [100, 200, 500, 700, 1000, 200, 300]  # demandes pour chaque mois
    cout_stockage_par_mois = 4  # coût de stockage par mois
    cout_approvisionnement_fixe = 1000  # coût fixe d'approvisionnement
    n = len(demandes)  # nombre de mois

    # Initialisation du problème
    prob = pulp.LpProblem("Optimisation_telecabines", pulp.LpMinimize)
    return prob, demandes, cout_stockage_par_mois, cout_approvisionnement_fixe, n

def definir_variables(prob, n):
    # Variables de décision
    commandes = pulp.LpVariable.dicts("Commandes", range(n), lowBound=0, cat='Continuous')
    stocks = pulp.LpVariable.dicts("Stocks", range(n + 1), lowBound=0, cat='Continuous')
    approvisionnement = pulp.LpVariable.dicts("Approvisionnement", range(n), cat='Binary')
    return commandes, stocks, approvisionnement

def definir_fonction_objectif(prob, stocks, cout_stockage_par_mois, approvisionnement, cout_approvisionnement_fixe, n):
    # Fonction objectif
    prob += pulp.lpSum([cout_stockage_par_mois * stocks[i] for i in range(1, n + 1)]) + \
            pulp.lpSum([cout_approvisionnement_fixe * approvisionnement[i] for i in range(n)])

def definir_contraintes(prob, stocks, commandes, demandes, approvisionnement, n):
    # Contraintes
    prob += stocks[0] == 0

    for i in range(n):
        prob += stocks[i] + commandes[i] - demandes[i] == stocks[i + 1]
        prob += commandes[i] <= 10000 * approvisionnement[i]
        prob += commandes[i] >= 0.0001 * approvisionnement[i]

def resoudre_et_afficher(prob, demandes, approvisionnement, stocks, cout_stockage_par_mois, n):
    # Résolution du problème
    prob.solve()

    # Affichage de la valeur optimale du coût total
    print("Statistiques")
    print("-" * 40)
    print(f"Nombre de variables: {len(prob.variables())}")
    print(f"Nombre de contraintes: {len(prob.constraints.values())}")
    print(f"Valeur de la stratégie optimale : {pulp.value(prob.objective)}")
    print("Description de la stratégie optimale :")
    print("-" * 83)
    print("| Mois | Approvisionnement | Stock | Commande | Demandes |")
    print("-" * 83)

    # Affichage des résultats dans un tableau
    for i in range(n):
        mois = i
        approvisionnement_val = commandes[i].varValue if approvisionnement[i].varValue == 1.0 else 0.0
        stock_val = stocks[i + 1].varValue
        commande_val = approvisionnement[i].varValue
        demande_val = demandes[i]
        print(f"| {mois:<4} | {approvisionnement_val:<17} | {stock_val:<5} | {commande_val:<8} | {demande_val:<8} |")

    print("-" * 83)

def main():
    prob, demandes, cout_stockage_par_mois, cout_approvisionnement_fixe, n = initialiser_probleme()
    commandes, stocks, approvisionnement = definir_variables(prob, n)
    definir_fonction_objectif(prob, stocks, cout_stockage_par_mois, approvisionnement, cout_approvisionnement_fixe, n)
    definir_contraintes(prob, stocks, commandes, demandes, approvisionnement, n)
    resoudre_et_afficher(prob, demandes, approvisionnement, stocks, cout_stockage_par_mois, n)

if __name__ == "__main__":
    main()
