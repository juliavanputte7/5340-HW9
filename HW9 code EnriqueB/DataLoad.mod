# Load sets from old data format
set MATERIAL; # resources that can be stocked
set CAPACITY; # resources that cannot be stocked
set NO_PICKUP within {MATERIAL union CAPACITY}; # resources that don't need pickup when purchased
set PICKUP within CAPACITY; # resources used for pickup
set CUSTOMER; # sources of demand
set NO_LATE within CUSTOMER; # customers that don't accept late satsifaction of demand
set NO_DELIVER within CUSTOMER; # customers that don't need delivery when shipped to
set DELIVER within CAPACITY; # resources used for delivery
set SUB_TRIPLES within {MATERIAL union CAPACITY, MATERIAL union CAPACITY, MATERIAL union CAPACITY}; 
	# (p, r, j) -> products p that can have a prime resource r substituted for another resource j

set TIME ordered; # days of work
set LOCATION; # locations
set PRIMARY_LOCATION within LOCATION;
set NONPRIMARY_BUYS within {MATERIAL union CAPACITY};
set EXTRA_BUYS within {MATERIAL union CAPACITY, LOCATION};
set BOM within {MATERIAL union CAPACITY, MATERIAL union CAPACITY}; # (p, r) -> resource r used to make product p

param init_cash default 0; # money to start with
param pick_up_time default 0; # time to pickup all resources purchased in a day
param deliver_time default 0; # time to deliver all resources shipped in a day
param usage {BOM}; # (p, r) -> amount of r used to make a unit of p
param cost {MATERIAL union CAPACITY} default 0; # cost to purchase a product 
param ord_qty {MATERIAL union CAPACITY} default 1; # quantity in a unit of purchase
param max_buy {MATERIAL union CAPACITY, TIME} default 0; # upper bound for purchase units of r in time t
param min_buy {MATERIAL union CAPACITY} default 0; # non-zero lower bounds for purchase units of r
param baseprice {CUSTOMER, MATERIAL union CAPACITY} default 0; # price to sell a product
param demand {CUSTOMER, MATERIAL union CAPACITY, TIME} default 0; # demand by customer c for product p in time t
param supply {MATERIAL union CAPACITY,TIME,LOCATION} default 0; # newly aquired r in time t
param sub_usage {SUB_TRIPLES}; # (p, r, j) -> amount of j used to satisfy all of the usage of r in p
param late_delivery_penalty default 0; # penalty for meeting demand late
param transport_out_cost default 0;
param transport_in_cost default 0;
set SMALL_BOX;