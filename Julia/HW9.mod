# we dont have to deliver for show
# we dont have to pickup for janey time

### Decision Variables

var Operation{OPERATIONS, TIME} >= 0 integer; 		# Quantity of operation k started in period t
var Stock{MATERIAL, TIME} >= 0; 					# Stock levels of materials (not integer to enable capacity optimization tricks)
var Scrap{r in RESOURCE diff PROD, TIME} >= 0; 		# Scrap material quantities (not integer for flexibility)
var Backlog{t in TIME, (c, m) in HAS_DEMAND} >= 0; 	# Shortage relative to cumulative demand
var BinBuy{t in TIME, r in HAS_MIN} binary; 		# Binary variable to enforce minimum purchase quantity constraints
var Sub {TIME, O_SUB_TRIPLES} >= 0; 				# Substitution variables (excludes self-substitutions)
var Selfsub{TIME, O_SUB_PAIRS} >= 0; 				# Variables for self-substitutions (used as prime substitutes)

var Revenue >=0; # For reporting, total revenue 
var Profit >= 0; # For reporting, total profit
var Cost >= 0; # For reporting, total cost

### Objective Function

# The objective is to maximize profit while accounting for various penalties and costs.
maximize profit: sum {t in TIME} 
    (
        # Revenue from shipments
        (sum {(c, p) in HAS_DEMAND}
            (Operation["Ship_" & p & "_" & c, t] * price[c, p, t])
        )
        # Purchasing cost (incentivizes late purchases using discounted costs)
        - (sum {o in OPERATIONS} 
            (if o in BUY then
                (Operation[o, t] * steering_cost[substr(o, length("Buy_") + 1), t])
            else 0)
        )
        # Scrap penalty (for wasted materials/resources)
        #- sum {r in RESOURCE diff PROD diff CAPACITY} (scrap_pen[r] * Scrap[r, t])
        # Stock penalty (carrying cost for storing materials)
        #- sum {r in PROD} (stock_pen[r] * Stock[r, t])
        # Penalty for using substitutes
        - sum {(o, i, r) in O_SUB_TRIPLES} (O_penalty[o, i, r] * Sub[t, o, i, r])
        # Penalty for operations to discourage unnecessary actions
        - sum {o in OPERATIONS} (op_pen[o] * Operation[o, t])
        # Penalty for late demand
        - sum{(c,r) in HAS_DEMAND} (1000 * Backlog[t,c,r])
    );

### Constraints

# Resource Balance Constraint Material
subject to RB_Material {t in TIME, r in MATERIAL}:
    # Usage of resources for production, considering direct and substitute usage
    sum {(o, r) in BOR diff O_SUB_PAIRS} 
        (Operation[o, t] * usages[o, r]) # Resources used directly without substitutions
    + sum {(o, r) in O_SUB_PAIRS} 
        (Selfsub[t, o, r] * usages[o, r]) # Prime resources used with substitutions
    + sum {(o, j, r) in O_SUB_TRIPLES} 
        (Sub[t, o, j, r] * sub_usages[o, j, r]) # Substitute resources used
    + Stock[r, t] # Material remaining in stock at time t
    + if r in RESOURCE diff PROD then Scrap[r, t] else 0 # Scrap material added back to balance
    =
    # Production, supply, and previous stock levels contribute to available resources
    sum {(o, r) in BOP} 
        (if ord(t) > offset[o, r] then produce[o, r] * Operation[o, prev(t, offset[o, r])] else 0)
    + supply[r, t] # Resource supply in the current time period
    + if ord(t) > 1 then Stock[r, prev(t, TIME)] else 0; # Previous period's stock

# Resource Balance Constraint Capacity
subject to RB_Capacity {t in TIME, r in CAPACITY}:
    sum {(o, r) in BOR diff O_SUB_PAIRS} 
        (Operation[o, t] * usages[o, r]) # Resources used directly without substitutions
    + sum {(o, r) in O_SUB_PAIRS} 
        (Selfsub[t, o, r] * usages[o, r]) # Prime resources used with substitutions
    + sum {(o, j, r) in O_SUB_TRIPLES} 
        (Sub[t, o, j, r] * sub_usages[o, j, r])
	+ Scrap[r, t]
    =
    # Capacity production and supply
    sum {o in OPERATIONS : (o, r) in BOP}
        produce[o, r] * Operation[o, t] + supply[r, t];

# Cumulative Shipment Constraint
subject to C_Ship {t in TIME, (c, p) in HAS_DEMAND}:
    # Backlog equals the cumulative demand minus cumulative shipments
    Backlog[t, c, p] = 
        (sum {s in TIME: ord(s) <= ord(t)} demand[c, p, s] # Total cumulative demand
        - sum {s in TIME: ord(s) <= ord(t)} Operation["Ship_" & p & "_" & c, s]); # Total cumulative shipments

# No Late Shipment Constraint
subject to No_Late {t in TIME, (c, p) in HAS_DEMAND : c in NO_LATE}:
    # For specific customers, shipments cannot be late
    demand[c, p, t] >= Operation["Ship_" & p & "_" & c, t];

# Minimum and Maximum Purchase Quantities

# Enforce binary variable for minimum purchase quantities
subject to ForceBin {t in TIME, r in HAS_MIN}:
    Operation["Buy_" & r, t] <= BigM * BinBuy[t, r];

# Ensure minimum purchase quantities are met when binary variable is activated
subject to ForceMin {t in TIME, r in HAS_MIN}:
    Operation["Buy_" & r, t] >= min_buy[r] * BinBuy[t, r];

# Ensure maximum purchase quantities are not exceeded
subject to MaxPurchase {t in TIME, r in CAN_BUY}:
    Operation["Buy_" & r, t] <= max_buy[t, r];

# Critical Substitution Constraints
subject to Same_make {t in TIME, (o, r) in O_SUB_PAIRS}:
    # Operations involving substitutions must balance primary and substitute resources
    Operation[o, t] = 
        Selfsub[t, o, r] + sum {(o, r, s) in O_SUB_TRIPLES} Sub[t, o, r, s];

# Compute revenue and profit (over time)
subject to Compute_Revenue:
	Revenue = sum{t in TIME,(c,p) in HAS_DEMAND} baseprice[c, p] * Operation["Ship_" & p & "_" & c,t];
	
subject to Compute_Profit:
	Profit = Revenue - Cost;
	
subject to Compute_Cost: Cost = sum{r in CAN_BUY, t in TIME} cost[r] * Operation["Buy_"&r,t];