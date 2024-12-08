# Model for HW 9

# Sets Definition

set MATERIAL;											# Set of materials used in the production process
set CAPACITY_RESOURCES;									# Set of resources associated with capacity constraints
set CAPACITY := CAPACITY_RESOURCES union {"Deliver_Time", "Pickup_Time"};  # Set of all capacity resources, including delivery and pickup times
set DELIVER_PICKUP; 									# Set of resources used specifically for delivery and pickup tasks
set CUSTOMER;											# Set of customers to whom the products are delivered
set NO_LATE within CUSTOMER default {};					# Subset of customers for whom late shipments are not allowed
set LOW_PRIORITY within CUSTOMER default {};			# Subset of customers with low-priority demand
set HIGH_PRIORITY within CUSTOMER default {};			# Subset of customers with high-priority demand
set LARGE_PRODUCTS default {};

set RESOURCE = MATERIAL union CAPACITY;					# Set of all resources, combining materials and capacities
set BOM within {MATERIAL, RESOURCE};	 				# Set of Bill of Materials (BOM) pairs, linking materials to resources
set PROD within MATERIAL = setof {(p, r) in BOM} p;    	# Set of products derived from BOM
set RAW within MATERIAL = MATERIAL diff PROD;			# Set of raw materials (materials not classified as products)
set SUB_TRIPLES within {PROD, RESOURCE, RESOURCE} default {}; 	# Set of substitution triples (Product, Prime Resource, Substitute Resource)
set SUB_PAIRS within BOM = setof {(p, r, j) in SUB_TRIPLES} (p, r); # Set of BOM pairs that have substitutions
set TIME ordered;										# Ordered set of time periods for the planning horizon

# Parameter Definitions

# Parameters with Defaults
param cost {RESOURCE} default 0;						# Cost associated with each resource
param ord_qty {RESOURCE} default 0;						# Order quantity for resources that can be purchased
param min_buy {RESOURCE} default 1;						# Minimum purchase quantity for resources
param init_cash default 0;								# Initial cash available for the planning period
param baseprice {CUSTOMER, MATERIAL} default 0;			# Base price of materials for each customer
param p_disc default 0;									# Discount rate on prices over time
param usage {BOM};    				   		  			# Usage rate of each resource in producing products
param sub_usage {SUB_TRIPLES};							# Usage rate of substitute resources in substitution triples
param penalty {SUB_TRIPLES} default 0;					# Penalty for using substitute resources
param mix {SUB_TRIPLES} within {0, 1};					# Binary parameter indicating whether a substitution mix is allowed
param supply {RESOURCE, TIME} default 0;       			# Supply of resources available in each time period
param demand {CUSTOMER, MATERIAL, TIME} default 0;   	# Demand for materials from each customer in each time period
param c_demand {c in CUSTOMER, r in MATERIAL, t in TIME} := 
					sum {s in TIME: ord(s) <= ord(t)} demand[c, r, s];  # Cumulative demand up to time t

# Priority-Based Parameters
param mult {c in CUSTOMER} default 1;	 				# Multiplier to "turn off" low-priority demand
param beta_weight default 0; 							# Weight for penalizing maximum bias in demand satisfaction

# Calculated Sets and Parameters Based on Inputs
set CAN_BUY := setof {r in RESOURCE: cost[r] * ord_qty[r] >= 1} r; 	# Resources that can be purchased
set HAS_MIN := setof {r in CAN_BUY: min_buy[r] >= 2} r; 			# Resources with a minimum purchase quantity

# Subset of Customer-Material pairs that have demand
set HAS_DEMAND := setof {c in CUSTOMER, r in MATERIAL: c_demand[c, r, last(TIME)] >= 1} (c, r); 

# Materials with high-priority demand
set MAT_DEMAND := setof {(c, r) in HAS_DEMAND: c in HIGH_PRIORITY} r;	

# Scaled price of materials for each customer, adjusted for priority and discount rate
param price {(c, m) in HAS_DEMAND, t in TIME} = 		
					 mult[c] * 						# Adjust for priority level
					 baseprice[c, m] * (1 - p_disc)**(ord(t, TIME) - 1); 

# Scaled cost of purchasing resources as late as possible (adjusted for discount rate)
param steering_cost {r in CAN_BUY, t in TIME} = 
					 cost[r] * (1 - p_disc)**(ord(t, TIME) - 1);  					 

# BigM and Alpha Definitions
param BigM := 10 * sum {(c, m) in HAS_DEMAND} 
					baseprice[c, m] * c_demand[c, m, last(TIME)] ;  # Large constant for modeling constraints
param alpha := .05 * min {c1 in CUSTOMER, c2 in CUSTOMER, (p, q) in {MATERIAL, MATERIAL}: 
														baseprice [c1, p] >= baseprice[c2, q] + 1} 
					(baseprice [c1, p] - baseprice[c2, q]);  # Minimum price difference weighted by 5%

param epsilon default BigM;								# Small tolerance parameter for constraints

# Lower and Upper Bounds on Shipments and Backlogs
param demand_lb {(c, m) in HAS_DEMAND, t in TIME} default 0 <= 
					floor(c_demand[c, m, t]); 			# Lower bound for shipment
param max_backlog {(c, m) in HAS_DEMAND, t in TIME} default 
					c_demand[c, m, t]; 					# Upper bound for backlog

# Penalties for Inventory, Scrap, and Maximum Purchases
param stock_pen {MATERIAL} default .5 * alpha;   		# Carrying cost penalty for inventory
param scrap_pen {RESOURCE} default alpha; 				# Penalty for scrap materials
param max_buy {TIME, RESOURCE} default BigM; 			# Upper limit on resource purchases per time period

# Parameter for offset for receiving when people (like the seamstress) want their money in advance
param receive_offset {CAN_BUY} default 0;