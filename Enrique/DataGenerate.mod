set HAS_DEMAND := setof {c in CUSTOMER, r in MATERIAL union CAPACITY : sum {t in TIME} demand[c,r,t]>=1} (c,r); # customer, product pairs that have demand on any day
set RESOURCE = setof {r in MATERIAL union CAPACITY, l in LOCATION} (r & "_at_" & l)
	union (setof {(c,r) in HAS_DEMAND} (c & "_Demand_" & r)) union {"Money", "Pick_Up_Time", "Deliver_Time", "Move_Out", "Move_In"}; 
	# resources, demand for resources, money, pickup and delivery time
set PRODUCT = setof {(p,r) in BOM} p; # any resource that can be made
set CAN_BUY := setof {r in MATERIAL union CAPACITY : cost[r] > 0} r; # any resource that can be purchased
set HAS_MAX_BUY := setof {r in CAN_BUY : sum {t in TIME} max_buy[r, t] > 0} r; # any resource that has a maximum purchase amount
set HAS_MAX := setof {r in HAS_MAX_BUY} "Buy_" & r; # corresponding operations to resources with maximum
set HAS_MIN_BUY := setof {r in CAN_BUY : min_buy[r] > 0} r; # any resource that has a non-zero minimum purchase amount
set HAS_MIN := setof {r in HAS_MIN_BUY} "Buy_" & r; # corresponding operatiosn to resources with minimums
 
set MAKE_OP = setof {p in PRODUCT, l in LOCATION} ("Make_" & p & "_at_" & l); # operations for making any product
set PROC_OP = setof {r in CAN_BUY} ("Buy_" & r); # operations for buying any resource that can be bought
set SHIP_OP = setof {(c,r) in HAS_DEMAND} (c & "_Ship_" & r); # operations for shipping resource to a customer
set SCRP_OP = setof {r in RESOURCE} ("Scrap_" & r); # operation for scrapping any resource
set STCK_OP = setof {r in MATERIAL, l in LOCATION} ("Stock_" & r & "_at_" & l) union {"Stock_Money"}; # operation for stocking any material
set BDMD_OP = setof {(c, r) in HAS_DEMAND : not (c in NO_LATE)} (c & "_Late_" & r); # operation for converting demand into demand on a later day
set DRIV_OP = {"Pick_Up", "Deliver", "Trans_Out", "Trans_In"}; # operations for driving to do delivery/pickup on a day
set MOVE_OP = setof {r in MATERIAL, s in LOCATION, d in LOCATION : s != d and (s in PRIMARY_LOCATION or d in PRIMARY_LOCATION)} ("Move_" & r & "_from_" & s & "_to_" & d);
set OPERATION = MAKE_OP union PROC_OP union SHIP_OP union SCRP_OP union STCK_OP union BDMD_OP union DRIV_OP union MOVE_OP; # all operations

set BOR within {OPERATION, RESOURCE} = # resources used in operations
	setof {(p, r) in BOM, l in LOCATION} ("Make_" & p & "_at_" & l, r & "_at_" & l) union # making a product uses resources in its BOM
	setof {r in CAN_BUY} ("Buy_" & r, "Money") union # buying a resource costs money
		setof {r in CAN_BUY diff NO_PICKUP} ("Buy_" & r, "Pick_Up_Time") union # buying a resource that needs pickup costs pickup time
	setof {(c, p) in HAS_DEMAND, l in PRIMARY_LOCATION} (c & "_Ship_" & p, p & "_at_" & l) union # shipping a product uses a unit of that product
		setof {(c, p) in HAS_DEMAND} (c & "_Ship_" & p, c & "_Demand_" & p) union # shipping a product satisfies a unit of demand for that product
		setof {(c, p) in HAS_DEMAND : not c in NO_DELIVER} (c & "_Ship_" & p, "Deliver_Time") union # shipping a product that requires delivery uses delivery time
		setof {p in MATERIAL : ("Online", p) in HAS_DEMAND and p in SMALL_BOX} ("Online_Ship_" & p, "SmallBox_at_Garage") union
		setof {p in MATERIAL : ("Online", p) in HAS_DEMAND and p not in SMALL_BOX} ("Online_Ship_" & p, "LargeBox_at_Garage") union
	setof {r in RESOURCE} ("Scrap_" & r, r) union # scrapping a resource uses a unit of that resource
	setof {r in MATERIAL, l in LOCATION} ("Stock_" & r & "_at_" & l, r & "_at_" & l) union 
		({("Stock_Money", "Money")}) union # scrapping a resource uses a unit of that resource in this time period
	setof {(c, r) in HAS_DEMAND : not (c in NO_LATE)} (c & "_Late_" & r, c & "_Demand_" & r) union # backlogging demand uses a unit of demand in this time period
	setof {r in PICKUP, l in PRIMARY_LOCATION} ("Pick_Up", r & "_at_" & l) union 
		setof {r in DELIVER, l in PRIMARY_LOCATION} ("Deliver", r & "_at_" & l) union
	({("Trans_Out", "Money"), ("Trans_In", "Money")}) union # picking up and delivering use resources specified in the data
	setof {r in MATERIAL, s in PRIMARY_LOCATION, d in LOCATION : s != d} ("Move_" & r & "_from_" & s & "_to_" & d, r & "_at_" & s) union
		setof {r in MATERIAL, s in PRIMARY_LOCATION, d in LOCATION : s != d} ("Move_" & r & "_from_" & s & "_to_" & d, "Move_Out") union
		setof {r in MATERIAL, s in LOCATION, d in PRIMARY_LOCATION : s != d} ("Move_" & r & "_from_" & s & "_to_" & d, r & "_at_" & s) union
		setof {r in MATERIAL, s in LOCATION, d in PRIMARY_LOCATION : s != d} ("Move_" & r & "_from_" & s & "_to_" & d, "Move_In");
	
set BOP within {OPERATION, RESOURCE} = # resources produced by operations
	setof {p in PRODUCT, l in LOCATION} ("Make_" & p & "_at_" & l, p & "_at_" & l) union # making a product produces that product
	setof {r in CAN_BUY diff NONPRIMARY_BUYS, l in PRIMARY_LOCATION} ("Buy_" & r, r & "_at_" & l) union # buying a resource produces that resource
	setof {(r, l) in EXTRA_BUYS} ("Buy_" & r, r & "_at_" & l) union
	setof {(c, p) in HAS_DEMAND} (c & "_Ship_" & p, "Money") union # shipping a product earns money
	setof {r in MATERIAL, l in LOCATION} ("Stock_" & r & "_at_" & l, r & "_at_" & l) union 
		({("Stock_Money", "Money")}) union	
	setof {(c, r) in HAS_DEMAND : not (c in NO_LATE)} (c & "_Late_" & r, c & "_Demand_" & r) union # backlogging demand produces demand in the next period
	({("Pick_Up", "Pick_Up_Time"), ("Deliver", "Deliver_Time"), ("Trans_Out", "Move_Out"), ("Trans_In", "Move_In")}) union # picking up and delivering give access to as much pickup or delivery time as needed
	setof {r in MATERIAL, s in PRIMARY_LOCATION, d in LOCATION : s != d} ("Move_" & r & "_from_" & s & "_to_" & d, r & "_at_" & d) union
		setof {r in MATERIAL, s in LOCATION, d in PRIMARY_LOCATION : s != d} ("Move_" & r & "_from_" & s & "_to_" & d, r & "_at_" & d);
 
param use {BOR}; # quantities of resources used, as determined by the supplied data when necessary
let {(p, r) in BOM, l in LOCATION} use["Make_" & p & "_at_" & l, r & "_at_" & l] := usage[p,r]; 
let {r in CAN_BUY} use["Buy_" & r, "Money"] := cost[r]; 
let {r in CAN_BUY diff NO_PICKUP} use["Buy_" & r, "Pick_Up_Time"] := 1; 
let {(c, p) in HAS_DEMAND, l in PRIMARY_LOCATION} use[c & "_Ship_" & p, p & "_at_" & l] := 1; 
let {(c, p) in HAS_DEMAND} use[c & "_Ship_" & p, c & "_Demand_" & p] := 1; 
let {(c, p) in HAS_DEMAND : not c in NO_DELIVER} use[c & "_Ship_" & p, "Deliver_Time"] := 1; 
let {p in MATERIAL : ("Online", p) in HAS_DEMAND and p in SMALL_BOX} use["Online_Ship_" & p, "SmallBox_at_Garage"] := 1;
let {p in MATERIAL : ("Online", p) in HAS_DEMAND and p not in SMALL_BOX} use["Online_Ship_" & p, "LargeBox_at_Garage"] := 1;
let {r in RESOURCE} use["Scrap_" & r, r] := 1; 
let {r in MATERIAL, l in LOCATION} use["Stock_" & r & "_at_" & l, r & "_at_" & l] := 1; 
let use["Stock_Money", "Money"] := 1;
let {(c, r) in HAS_DEMAND : not (c in NO_LATE)} use[c & "_Late_" & r, c & "_Demand_" & r] := 1; 
let {r in PICKUP, l in PRIMARY_LOCATION} use["Pick_Up", r & "_at_" & l] := pick_up_time;
let {r in DELIVER, l in PRIMARY_LOCATION} use["Deliver", r & "_at_" & l] := deliver_time;
let use["Trans_In", "Money"] := transport_in_cost;
let use["Trans_Out", "Money"] := transport_out_cost;
let {r in MATERIAL, s in PRIMARY_LOCATION, d in LOCATION : s != d} use["Move_" & r & "_from_" & s & "_to_" & d, r & "_at_" & s] := 1;
let {r in MATERIAL, s in PRIMARY_LOCATION, d in LOCATION : s != d} use["Move_" & r & "_from_" & s & "_to_" & d, "Move_Out"] := 1;
let {r in MATERIAL, s in LOCATION, d in PRIMARY_LOCATION : s != d} use["Move_" & r & "_from_" & s & "_to_" & d, r & "_at_" & s] := 1;
let {r in MATERIAL, s in LOCATION, d in PRIMARY_LOCATION : s != d} use["Move_" & r & "_from_" & s & "_to_" & d, "Move_In"] := 1;

param bigM := 10 * sum {(c, r) in HAS_DEMAND, t in TIME} demand[c, r, t]; # large enough number to satisfy all pickups/deliveries
param produce {BOP};
let {p in PRODUCT, l in LOCATION} produce["Make_" & p & "_at_" & l, p & "_at_" & l] := 1;
let {r in CAN_BUY diff NONPRIMARY_BUYS, l in PRIMARY_LOCATION} produce["Buy_" & r, r & "_at_" & l] := ord_qty[r];
let {(r, l) in EXTRA_BUYS} produce["Buy_" & r, r & "_at_" & l] := ord_qty[r];
let {(c, p) in HAS_DEMAND} produce[c & "_Ship_" & p, "Money"] := baseprice[c, p];
let {r in MATERIAL, l in LOCATION} produce["Stock_" & r & "_at_" & l, r & "_at_" & l] := 1; 
let produce["Stock_Money", "Money"] := 1;
let {(c, r) in HAS_DEMAND : not (c in NO_LATE)} produce[c & "_Late_" & r, c & "_Demand_" & r] := 1;
let produce["Pick_Up", "Pick_Up_Time"] := bigM;
let produce["Deliver", "Deliver_Time"] := bigM;
let produce["Trans_In", "Move_In"] := bigM;
let produce["Trans_Out", "Move_Out"] := bigM;
let {r in MATERIAL, s in PRIMARY_LOCATION, d in LOCATION : s != d} produce["Move_" & r & "_from_" & s & "_to_" & d, r & "_at_" & d] := 1;
let {r in MATERIAL, s in LOCATION, d in PRIMARY_LOCATION : s != d} produce["Move_" & r & "_from_" & s & "_to_" & d, r & "_at_" & d] := 1;


param offset {BOP} default 0; # delay between time period of execution of operation and when the production is recieved 
#let offset["Buy_QTop", "QTop_at_Garage"] := 2;
let {(c, p) in HAS_DEMAND} offset[c & "_Ship_" & p, "Money"] := 1; # money for a shipment comes at the end of the day
let {r in MATERIAL, l in LOCATION} offset["Stock_" & r & "_at_" & l, r & "_at_" & l] := 1; 
let offset["Stock_Money", "Money"] := 1;
let {(c, r) in HAS_DEMAND : not (c in NO_LATE)} offset[c & "_Late_" & r, c & "_Demand_" & r] := 1; # backlogging demand comes in the next period
let {r in MATERIAL, s in LOCATION, d in PRIMARY_LOCATION : s != d} offset["Move_" & r & "_from_" & s & "_to_" & d, r & "_at_" & d] := 1;


param new_supply {RESOURCE, TIME} default 0; # resources introduced at no cost in any period
let new_supply["Money", first(TIME)] := init_cash; # initial supply of money
let {r in MATERIAL union CAPACITY, t in TIME, l in LOCATION} new_supply[r & "_at_" & l, t] := supply[r, t, l]; # supply of resources
let {(c, p) in HAS_DEMAND, t in TIME} new_supply[c & "_Demand_" & p, t] := demand[c, p, t]; # supply of demand for products

param maximum {OPERATION, TIME} default 0; # maximum number of times an operation can be done in any period
let {r in HAS_MAX_BUY, t in TIME} maximum["Buy_" & r, t] := max_buy[r, t]; # enforces maximum labor hours

param minimum {OPERATION} default 0; # minimum number of times an operation must be done, if a nonzero amount
let {r in HAS_MIN_BUY} minimum["Buy_" & r] := min_buy[r]; # enforces minimum order quantities

set SUBSTITUTIONS = setof {(p, r1, r2) in SUB_TRIPLES, l in LOCATION} ("Make_" & p & "_at_" & l, r1 & "_at_" & l, r2 & "_at_" & l); # substitutions of inputs for operations
set SUB_PAIRS within BOR = setof {(p,r,j) in SUBSTITUTIONS} (p,r); # operation/input pairs that have a substitute
param sub_use {SUBSTITUTIONS}; # (k, r, j) -> quantity of j to replace r as input in operation k
let {(p, r1, r2) in SUB_TRIPLES, l in LOCATION} sub_use["Make_" & p & "_at_" & l, r1 & "_at_" & l, r2 & "_at_" & l] := sub_usage[p, r1, r2];

param penalty {OPERATION} default 0; # penalties for doing an operation
let {k in BDMD_OP} penalty[k] := late_delivery_penalty; # discourage late delivery by penalizing backlogging demand