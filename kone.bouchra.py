import pulp
from pulp import (
    LpMinimize,
    LpProblem,
    LpVariable,
    lpSum,
    LpStatus,
)

def optimisation(demandes, cout_stockage, cout_approv):
    prob = LpProblem(name='Cabines', sense=LpMinimize)

    n = len(demandes)


    comm = LpVariable.dicts("Commandes", range(n), lowBound=0, cat='Continuous')
    stock = LpVariable.dicts("Stocks", range(n + 1), lowBound=0, cat='Continuous')
    approv = LpVariable.dicts("Approvisionnement", range(n), cat='Binary')

    prob += lpSum(cout_stockage * stock[i] for i in range(1, n + 1)) + \
            lpSum(cout_approv * comm[i] for i in range(n))
    
    
    for i in range(n):
        prob += stock[i] + comm[i] - demandes[i] == stock[i + 1]
        prob += comm [i] <= 10000 * approv[i]
        prob += comm[i] >= 0.0001 * approv[i]
    prob.solve()

    print()
    print('-' * 40)
    print("Statistiques")
    print()
    print("-" * 40)
    print()
    print(f"Nombre de variables: {len(prob.variables())}")
    print(f"Nombre de contraintes: {len(prob.constraints.values())}")
    print()
    print('Time:')
    print(f'- (real) {prob.solutionTime}')
    print(f'- (CPU) {prob.solutionCpuTime}')
    print()

    print(f'Solve status: {LpStatus[prob.status]}')
    print(f'Objective value: {prob.objective.value()}')

    print(f"Valeur de la stratégie optimale : {pulp.value(prob.objective)}")
    print("Description de la stratégie optimale :")
    print("-" * 83)
    print("| Mois | Approvisionnement | Stock | Commandes | Demandes |")
    print("-" * 83)

    for i in range(n):
        mois = i
        approvisionnement = comm[i].varValue if approv[i].varValue == 1.0 else 0.0
        stocks = stock[i+1].varValue
        commandes = comm[i].varValue
        vDemandes = demandes[i]
        print(f"| {mois:<4} | {approvisionnement:<17} | {stocks:<5} | {commandes:<8} | {vDemandes:<8} |")

    print("-" * 83)

# Test
demandes = [100, 200, 500, 700, 1000, 200, 300]
cout_stockage = 4
cout_approv = 1000

optimisation(demandes, cout_stockage, cout_approv)
