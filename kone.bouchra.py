#Author: Largaton KONE and Salma BOUCHRA
import pulp
from pulp import (
    PULP_CBC_CMD,
    LpMinimize,
    LpProblem,
    LpVariable,
    lpSum,
    LpStatus,
    LpBinary,
    LpInteger,
)


# ============================================================================ #
#                                  SET MODEL                                   #
# ============================================================================ #

def optimisation(demandes, cout_stockage, cout_approv):
    # ------------------------------------------------------------------------ #
    # Linear problem with minimization
    # ------------------------------------------------------------------------ #
    prob = LpProblem(name='Cabines', sense=LpMinimize)
    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #

    n = len(demandes) 

    comm =[
            LpVariable(f'Commandes{i}', lowBound=0, cat=LpBinary)
        for i in range(n)
        ]
    
    stock =[
            LpVariable(f'Stocks{i}', lowBound=0, cat=LpInteger)
        for i in range(n)
        ]
    
    approv =[
            LpVariable(f'Approvisionnement{i}', lowBound=0, cat=LpInteger)
        for i in range(n)
        ]
    
    # ------------------------------------------------------------------------ #
    # The objective function
    # ------------------------------------------------------------------------ #
        

    prob += cout_approv * lpSum(comm)+ cout_stockage * lpSum(stock)
    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #

    prob += approv[0] == lpSum ([stock[0] , demandes[0]])
    prob += approv[n-1]+ stock[n-2] == demandes[n-1]

    for i in range(1, n-1):

        prob += approv[i] + stock[i-1]  == stock[i] + demandes[i]
        
    for i in range(n):
        prob += comm[i] <= approv[i]
        prob += approv[i] <= sum (demandes)*comm[i]


# ============================================================================ #
#                               SOLVE WITH DATA                                #
# ============================================================================ #
    prob.solve( PULP_CBC_CMD(
            msg=False, logPath='./CBC_adm_array.log',
        ),
    )


# ============================================================================ #
#                                   UTILITIES                                  #
# ============================================================================ #
    print()
    print('-' * 40)
    print('Statistiques')
    print('-' * 40)
    print()
    
    print(f'Number variables: {prob.numVariables()}')
    print(f'Number constraints: {prob.numConstraints()}')
    print()
   

  
    print('Time:')
    print(f'- (real) {prob.solutionTime}')
    print(f'- (CPU) {prob.solutionCpuTime}')
   

    print(f'Solve status: {LpStatus[prob.status]}')
    print(f'Objective value: {prob.objective.value()}')

    print(f'Valeur de la stratégie optimale : {pulp.value(prob.objective)}')
    print('Description de la stratégie optimale :')
    print('-' * 80)
    print('| Mois | Approvisionnement | Stock | Commandes | Demandes |')
    print('-' * 80)
    for i in range(n):
        mois = i
        approvisionnement = approv[i].varValue
        stocks = stock[i].varValue
        commandes = comm[i].varValue
        dmd = demandes[i]
        print(f'| {mois:<4} | {approvisionnement:<17} | {stocks:<5} | {commandes:<8} | {dmd:<8} |')

    print('-' * 80)

# Test
demandes = [100, 200, 500, 700, 1000, 200, 300]
cout_stockage = 4
cout_approv = 1000

optimisation(demandes, cout_stockage, cout_approv)
