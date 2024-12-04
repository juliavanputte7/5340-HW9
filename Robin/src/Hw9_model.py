

from ortools.linear_solver import pywraplp
from collections import defaultdict
from Hw9_helpers import *
def Hw9_model(REFACTOR, OPS, BOR, BOP, PROD, MATERIAL, CAPACITY, RESOURCE, TIME, NO_LATE, HAS_OFFSET,
              usage, baseprice, p_disc, demand, supply, make_pen, ord_offset, stoc_pen, scrap_pen, sub_pen, sub_usage,
              init_stoc, init_funds, min_buy, max_buy, demand_lb = {}):

    """Single Level Single Product Resource Allocation Model_Homework1"""

    # BigM
    BigM = 10 * sum(baseprice.values())
    # Solver
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    infinity = solver.infinity()
    objective_terms = []
    BinBuy = {}
    Exec = {}
    #VALUE TYPES FOR DECISION VARS
    bool_vars = {'action'}
    num_vars ={'scrap', 'stock'}
    int_vars = {'make', 'ship', 'transport', 'buy', 'sub'}
    #DECISION VARS
    for t in TIME:
        for op in OPS:
            typ, r = parse_op(op)
            if typ in int_vars:
                Exec[op, t] = solver.IntVar(0, infinity, f'{typ}[{r,t }]')
            elif typ in num_vars:
                Exec[op, t] = solver.NumVar(0, infinity, f'{typ}[{r, t}]')
            elif typ in bool_vars:
                Exec[op, t] = solver.BoolVar(f'{op}[{t}]')
            else:
                raise Exception(f"Unknown type {typ}")
    #INDICATORS
    for t in TIME:
        for op in REFACTOR.BUYOPS:
            BinBuy[op, t] = solver.BoolVar(f'BinBuy[{op, t}]')


    #OBJECTIVE
    for t in TIME:
        objective_terms += [BOP[op, 'cash'] * Exec[op, t] * (1-p_disc)**TIME.index(t) for op in OPS]
        objective_terms += [-1 * BOR[op, 'cash'] * Exec[op, t] * (1 - p_disc) ** TIME.index(t) for op in OPS]
        objective_terms += [-1 * make_pen[op] * Exec[op, t] for op in REFACTOR.MAKEOPS]
        objective_terms += [-1 * sub_pen[op] * Exec[op, t] for op in REFACTOR.SUBOPS]
        objective_terms += [-1 * scrap_pen[op] * Exec[op, t] for op in REFACTOR.SCRAPOPS]
        objective_terms += [-1 * stoc_pen[op] * Exec[op, t] for op in REFACTOR.STOCKOPS]
    solver.Maximize(solver.Sum(objective_terms))

    # Constraints

    for t in TIME:

        # resource availability
        for r in RESOURCE:
            if r in HAS_OFFSET:
                offset = ord_offset[r]
                buy_op = Exec[f"B_{r}", prev(TIME, t, n=offset)]
                prev_orders = 0 if TIME.index(t) < offset else buy_op * BOP[buy_op, r]
            else:
                prev_orders = 0
            prev_stock = 0 if r in CAPACITY else (Exec[f"St_{r}", prev(TIME, t)] if TIME.index(t) > 0 else init_stoc[r])
            consumed = [Exec[op, t] * BOR[op, r] for op in OPS if (op, r) in BOR]
            produced = [Exec[op, t] * BOP[op, r] for op in OPS if (op, r) in BOP]
            solver.Add((solver.Sum(consumed) - solver.Sum(produced)) ==
                       (supply[r,t] + prev_stock + prev_orders))
            #add no late ship for every customer in NO_late where the customer has some demand for r

        #CUMULATIVE DEMAND
        for op in REFACTOR.SHIPOPS:
            solver.Add(solver.Sum([Exec[op, s] for s in TIME if TIME.index(s) <= TIME.index(t)]) <=
                       solver.Sum([demand[op][TIME.index(s)] for s in TIME if TIME.index(s) <= TIME.index(t)]))
            _, c, p = parse_ship_op(op)
            if c in NO_LATE: #IF CUSTOMER IS IS NO LATE, CONSTRAIN SHIPMENT ON DAY TO AT MOST DEMAND ON DAY
                solver.Add(Exec[op, t] <= demand[op][TIME.index(t)])

            if c in REFACTOR.IS_SHIPPED: #can only ship to places which require in-person delivery if Doug ships
                solver.Add(Exec[op,t] <= BigM * Exec["DougShips", t], name=f'DougShips[{t}]')
        #cant sub for more products then products made (this shouldnt be necessary but it's safe so fine)
        for op in REFACTOR.SUBOPS:
            _, p, _, _ = parse_sub_op(op)
            solver.Add(Exec[op, t] <= Exec[create_op(p, "make"), t])

        #enforce buy indicators
        for op in REFACTOR.BUYOPS:
            #BinBuy indicators
            solver.Add(BigM * BinBuy[op, t] >= Exec[op, t], name=f'ForceBin[{t, r}]')
            solver.Add(Exec[op, t] >= BinBuy[op, t] * min_buy[op][TIME.index(t)], name=f'ForceMin[{t, r}]')
            solver.Add(Exec[op, t] <= BinBuy[op, t] * max_buy[op][TIME.index(t)], name=f'ForceMax[{t, r}]')
            #DoesBuy
            solver.Add(Exec[op, t] <= BigM * Exec["DougBuys", t], name = f'DougBuys[{t}') #can only buy if Doug buys

        #change material location only when we've purchased delivery service
        for op in REFACTOR.TRANSPORTOPS:
            typ, destination, origin, mat = parse_transport_op(op)
            if destination == "Studio":
                solver.Add(Exec[op, t] <= Exec["SendsToStudio",t] * BigM)
            else:
                solver.Add(Exec[op, t] <= Exec["SendsToGarage", t] * BigM)





    TotRev = solver.NumVar(-infinity, infinity, f'TotRev')  # total revenue of plan for reporting
    Profit = solver.NumVar(-infinity, infinity, f'Profit')
    solver.Add(TotRev == solver.Sum([Exec[op,t] * BOP[op, 'cash'] for op in REFACTOR.OPS for t in TIME]))
    solver.Add(Profit == TotRev - solver.Sum([Exec[op, t] * BOR[op, 'cash'] for op in REFACTOR.OPS for t in TIME]))

    # Solve
    status = solver.Solve()
    solver.set_time_limit(150000)  # 150 seconds
    stats = {}
    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Revenue = {:.2f}\n'.format(TotRev.solution_value()))
        print('Profit: {:.2f}\n'.format(Profit.solution_value()))
        print('Objective = {:.3f}\n'.format(solver.Objective().Value()))

        stats = {"Revenue": TotRev.solution_value(), "Profit": Profit.solution_value(),
                 "Objective": solver.Objective().Value()}
        for t in TIME:
            for op in REFACTOR.MAKEOPS:
                if Exec[op,t].solution_value() > 0.1:
                    print(op, Exec[op, t].solution_value(), t)

            for op in REFACTOR.SHIPOPS:
                if Exec[op,t].solution_value() > 0.1:
                    print(op, Exec[op, t].solution_value(), t)

            for op in REFACTOR.BUYOPS:
                if Exec[op,t].solution_value() > 0.1:
                    print(op, Exec[op, t].solution_value(), t)



        print('\nAdvanced usage:')
        print('Problem solved in ', solver.wall_time(), ' milliseconds')
        print('Problem solved in ', solver.iterations(), ' iterations')
    else:
        print('No solution found.')
    return stats, solver, Exec


