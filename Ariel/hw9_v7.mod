### Options
reset;
option solver gurobi;
option gurobi_options 'MIPGap=.01' ; # 
option gurobi_options 'MIPGapABs=.01';

### PROVIDED DATA SETS AND PARAMS ###
set MATERIAL;
set CAPACITY;
set QUILTED_PRODUCTS;
set RESOURCE = MATERIAL union CAPACITY union QUILTED_PRODUCTS;
set CUSTOMER;	
set TIME ordered;
set BOM within RESOURCE cross RESOURCE;
set BIG_ITEMS;
set BUNDLES;
set LOCATIONS;
set TRANSPORTABLE;

param demand{CUSTOMER, MATERIAL, TIME} default 0;
param baseprice{CUSTOMER, MATERIAL} default 0;
param supply{RESOURCE,TIME,LOCATIONS} default 0; 
param usage{BOM};
param cost{RESOURCE} default 0;
param ord_qty{RESOURCE} default 0;
param min_buy{RESOURCE} default 0;
param max_buy{RESOURCE, TIME} default 0;
param bundle_qty{BUNDLES, RESOURCE} default 0;
param bundleCost{BUNDLES} default 0;
param smallUsage := 0.001;

###########-------- [Buy Days and Ship Days] --------###########
set EXTRA_CAPACITY := {'Shipping_Token','Buying_Token'};
set TRANSPORT_TOKENS := {'Transport_Janey_to_Doug','Transport_Doug_to_Janey'};


###############################################################################################################
###############################################################################################################

#############-------- [USEFUL SETS] --------#############
set HAS_DEMAND := setof{r in MATERIAL, c in CUSTOMER, t in TIME: demand[c,r,t]>0} (c,r);
set HAS_MIN := setof{r in RESOURCE: min_buy[r] >= 1} r;
set HAS_MAX := setof{r in RESOURCE, t in TIME: max_buy[r,t]>0} r; 
set CAN_MAKE := setof{(p,r) in BOM: usage[p,r]>0} (p);
set CAN_BUY := setof{r in RESOURCE: ord_qty[r] > 0} (r);
set DEM_RES_SUP := setof{r in MATERIAL, c in CUSTOMER, t in TIME: sum{x in TIME}demand[c,r,x]>0}('Dem_'&c&'_'&r, t);
set DEM_RES := setof{r in MATERIAL, c in CUSTOMER, t in TIME: demand[c,r,t]>0}('Dem_'&c&'_'&r);
set FULL_RES = DEM_RES union MATERIAL union CAPACITY union EXTRA_CAPACITY union BUNDLES;
set SMALL_ITEMS := MATERIAL diff BIG_ITEMS diff {'SmallBox', 'BigBox'};

param dem_supply {(d,t) in DEM_RES_SUP} = 
	sum{r in MATERIAL, c in CUSTOMER}(if d = 'Dem_'&c&'_'&r then demand[c,r,t] else 0);

param full_supply {r in FULL_RES, t in TIME, l in LOCATIONS} :=
    if (r in MATERIAL and l=='DougHouse') then supply[r, t, l]
    else if (r in DEM_RES and l=='DougHouse') then dem_supply[r, t]
    else 0;
    
param token_usage {r in EXTRA_CAPACITY, c in CAPACITY} :=
		if c == 'DougTime' then 120 else 0;
		
param full_usage {(r,c) in BOM union (EXTRA_CAPACITY cross CAPACITY)} :=
	if ((r,c) in BOM) then usage[r,c]
	else if ((r,c) in EXTRA_CAPACITY cross CAPACITY) then token_usage[r,c]
	else 0;
    
###########-------- [MAKING] --------###########
set MAKE_OPS := setof {p in CAN_MAKE union EXTRA_CAPACITY, l in LOCATIONS:l=='DougHouse'} ('Make_'&p, l);

set MAKE_BOP within MAKE_OPS cross (CAN_MAKE union EXTRA_CAPACITY):=
	setof{p in CAN_MAKE union EXTRA_CAPACITY, l in LOCATIONS:l=='DougHouse'} ('Make_'&p, l, p);
	
set MAKE_BOR within MAKE_OPS cross FULL_RES :=
	setof{(p,r) in BOM union (EXTRA_CAPACITY cross CAPACITY), l in LOCATIONS:l=='DougHouse'} 
	('Make_'&p, l, r);

param make_usage {(o,l,s) in MAKE_BOR} = 
	sum {p in CAN_MAKE union EXTRA_CAPACITY}
	(if o == 'Make_'&p then full_usage[p,s] else 0);

param make_produce {(o,l,s) in MAKE_BOP} = 
	sum {p in CAN_MAKE union EXTRA_CAPACITY} 
	(if o == 'Make_'&p then 1 else 0);
	
param make_offset {(o,l,s) in MAKE_BOP} = 0;

###########-------- [SHIPPING] --------###########
set SHIP_OPS := setof {(c,r) in HAS_DEMAND, l in LOCATIONS : l =='DougHouse'} 
				('Ship_'&r&'_to_'&c, l);

set SHIP_BOP within SHIP_OPS cross FULL_RES := 
	setof {(c,r) in HAS_DEMAND, l in LOCATIONS:l=='DougHouse'} ('Ship_'&r&'_to_'&c, l, 'Money'); 
	
set SHIP_BOR within SHIP_OPS cross FULL_RES :=
    setof{(c, r) in HAS_DEMAND, l in LOCATIONS:l=='DougHouse'} ('Ship_' & r & '_to_' & c, l, r) union
    setof{(c, r) in HAS_DEMAND, l in LOCATIONS:l=='DougHouse'} ('Ship_' & r & '_to_' & c, l,'Dem_' & c & '_' & r) union
    setof{(c, r) in HAS_DEMAND, l in LOCATIONS:l=='DougHouse'} ('Ship_' & r & '_to_' & c, l,'Shipping_Token') union
    setof{(c, r) in HAS_DEMAND, l in LOCATIONS : r in BIG_ITEMS and c in CUSTOMER and l == 'DougHouse'}
        ('Ship_' & r & '_to_' & c,l, 'BigBox') union
    setof{(c, r) in HAS_DEMAND, l in LOCATIONS: not (r in BIG_ITEMS and c in CUSTOMER) and l == 'DougHouse'}
        ('Ship_' & r & '_to_' & c, l,'SmallBox');

/*
param ship_produce {(o,l,p) in SHIP_BOP} = 
	sum{(c,r) in HAS_DEMAND} 
	(if o == 'Ship_'&r&'_to_'&c then baseprice[c,r] else 0);
*/

param ship_produce {(o,l,r) in SHIP_BOP} :=
    if r == 'Money' then
        sum{(c,s) in HAS_DEMAND} (if o == 'Ship_' & s & '_to_' & c then baseprice[c,s] else 0)
    else
        0;


param ship_usage {(o,l,p) in SHIP_BOR} =

    sum {(c,r) in HAS_DEMAND} 
    (if o == 'Ship_'&r&'_to_'&c then 
        (if p == 'Dem_'&c&'_'&r then 1 else 0)
    else 0) 
    
    + sum {(c,r) in HAS_DEMAND}
    (if o == 'Ship_'&r&'_to_'&c && p == r then 1 else 0)
    + sum{(c,r) in HAS_DEMAND}
    (if o == 'Ship_'&r&'_to_'&c and p == 'Shipping_Token' then smallUsage else 0)
    + sum{(c,r) in HAS_DEMAND}
    (if o == 'Ship_'&r&'_to_'&c and p == 'BigBox' then 1 else 0)
    + sum{(c,r) in HAS_DEMAND}
    (if o == 'Ship_'&r&'_to_'&c and p == 'SmallBox' then 1 else 0);

param ship_offset {(o,l,p) in SHIP_BOP} = 
	sum{(c,r) in HAS_DEMAND} 
	(if o == 'Ship_'&r&'_to_'&c then 1 else 0);

###########-------- [BUYING] --------###########
set BUY_OPS := setof {r in CAN_BUY union BUNDLES, l  in LOCATIONS:l=='DougHouse' and r!='Transport_Janey_to_Doug'} ('Buy_'&r, l)
                union {('Buy_Transport_Janey_to_Doug', 'JaneyStudio')};

set FabricBundledItems := setof {b in BUNDLES, r in MATERIAL : bundle_qty[b,r] > 0 and b=='FabricBundle'} r;
set MetalBundledItems := setof {b in BUNDLES, r in MATERIAL : bundle_qty[b,r] > 0 and b=='MetalBundle'} r;

set HAS_MIN_BUY_OPS := setof{r in HAS_MIN} ('Buy_'&r);
set HAS_MAX_BUY_OPS := setof{r in HAS_MAX} ('Buy_'&r);
	
set BUY_BOP within BUY_OPS cross FULL_RES :=
	setof {r in CAN_BUY, l in LOCATIONS:l=='DougHouse'and r!='Transport_Janey_to_Doug'} ('Buy_'&r, l, r) union
	setof {r in FabricBundledItems, l in LOCATIONS:l=='DougHouse'and r!='Transport_Janey_to_Doug'} ('Buy_FabricBundle', l, r) union
	setof {r in MetalBundledItems, l in LOCATIONS:l=='DougHouse'and r!='Transport_Janey_to_Doug'} ('Buy_MetalBundle', l, r) union
    {('Buy_Transport_Janey_to_Doug', 'JaneyStudio', 'Transport_Janey_to_Doug')};

set BUY_BOR within BUY_OPS cross FULL_RES :=
    setof {r in CAN_BUY, l in LOCATIONS: l == 'DougHouse' and r!='Transport_Janey_to_Doug'} ('Buy_' & r, l, 'Money') union
    setof {r in CAN_BUY, l in LOCATIONS: l == 'DougHouse' and r!='Transport_Janey_to_Doug'} ('Buy_' & r, l, 'Buying_Token') union
    setof {b in BUNDLES, l in LOCATIONS: l == 'DougHouse' and b!='Transport_Janey_to_Doug'} ('Buy_' & b, l, 'Money') union
    setof {b in BUNDLES, l in LOCATIONS: l == 'DougHouse' and b!='Transport_Janey_to_Doug'} ('Buy_' & b, l, 'Buying_Token');# union
    #{('Buy_Transport_Janey_to_Doug', 'JaneyStudio', 'Money'), ('Buy_Transport_Janey_to_Doug', 'JaneyStudio', 'Buying_Token')};

param buy_produce {(o,l,r) in BUY_BOP} = 
		if r in BUNDLES then sum{s in BUNDLES} (if o == 'Buy_'&s then bundle_qty[s, r] else 0) else ord_qty[r]
        ;

param buy_usage {(o,l,s) in BUY_BOR} = ### Buying JaneyTime and DougTime with Tokens
	sum {r in CAN_BUY} 
	(if o == 'Buy_'&r then 
        (if s == 'Buying_Token' and o != 'Buy_DougTime' and o != 'Buy_JaneyTime' and o != 'Buy_Transport_Janey_to_Doug' then smallUsage 
        else if s == 'Buying_Token' then 0
        else cost[r])
     else 0);


param buy_offset {(o,l,r) in BUY_BOP} = if r in QUILTED_PRODUCTS then 2 else 0;

###########-------- [SCRAP] --------###########
set SCRAP_OPS := setof {r in RESOURCE, l in LOCATIONS} ('Scrap_'&r, l);

set SCRAP_BOP within SCRAP_OPS cross RESOURCE :=
	setof {r in RESOURCE, l in LOCATIONS} ('Scrap_'&r, l, r);

set SCRAP_BOR within SCRAP_OPS cross RESOURCE :=
	setof {r in RESOURCE, l in LOCATIONS} ('Scrap_'&r, l, r);
	
param scrap_produce {(o,l,r) in SCRAP_BOP} = 0;

param scrap_usage {(o,l,r) in SCRAP_BOR} = if (r == 'Transport_Doug_to_Janey' or r == 'Transport_Janey_to_Doug') then smallUsage else 1;

param scrap_offset {(o,l,r) in SCRAP_BOP} = 0;

###########-------- [STOCK] --------###########
set STOCK_OPS := setof {r in FULL_RES, l in LOCATIONS} ('Stock_'&r,l);

set STOCK_BOP within STOCK_OPS cross FULL_RES := ##### CHANGE TO FULL_RES FROM MATERIAL
	setof {r in FULL_RES, l in LOCATIONS} ('Stock_'&r, l, r);		 ##### CHANGE TO FULL_RES FROM MATERIAL

set STOCK_BOR within STOCK_OPS cross FULL_RES :=
	setof {r in FULL_RES, l in LOCATIONS} ('Stock_'&r, l, r);
	
param stock_produce {(o,l,r) in STOCK_BOP} = (if r in CAPACITY or o == 'Stock_Shipping_Token' or o == 'Stock_Buying_Token'
											or o == 'Stock_Transport_Doug_to_Janey' or o == 'Stock_Transport_Janey_to_Doug'
											then 0 else 1);

param stock_usage {(o,l,r) in STOCK_BOR} = if o == 'Stock_Shipping_Token'
										 	or o == 'Stock_Buying_Token' 
											or o == 'Stock_Transport_Doug_to_Janey'
											or o == 'Stock_Transport_Janey_to_Doug'
											then smallUsage else 1;

param stock_offset {(o,l,r) in STOCK_BOP} = (if r in CAPACITY then 0 else 1);

#############-------- [SUBSTITUTIONS] --------#############
set SUB_TRIPLES within {MATERIAL,RESOURCE,RESOURCE} default{};
param subusage{SUB_TRIPLES} >= 0;

set SUB_OPS := setof{(p,r,s) in SUB_TRIPLES, l in LOCATIONS} ('Make_'&p&'_With_'&s, l);

set SUB_BOP within SUB_OPS cross MATERIAL :=
    setof{(p,r,s) in SUB_TRIPLES, l in LOCATIONS} ('Make_'&p&'_With_'&s, l, p);

set SUB_BOR within SUB_OPS cross RESOURCE :=
    setof{(p,r,s) in SUB_TRIPLES, l in LOCATIONS, (p, w) in BOM}
        ('Make_' & p & '_With_' & s, l, if w == r then s else w);

param subs_usage{(o,l,r) in SUB_BOR} :=
    sum{(p,r1,s) in SUB_TRIPLES:
        o == 'Make_' & p & '_With_' & s}
        if (r=s) then subusage[p, r1, s] else usage[p, r];

param subs_produce{(o,l,p) in SUB_BOP} = 1;
param subs_offset{(o,l,p) in SUB_BOP} = 0;

###########-------- [TRANSPORTATION SETS] --------###########
set TRANSPORT_FROM_OPS := setof{r in TRANSPORTABLE union TRANSPORT_TOKENS, f in LOCATIONS, d in LOCATIONS: f!=d and r!= 'Transport_Doug_to_Janey' and r != 'Transport_Janey_to_Doug'}
					('Transport_'&r&'_From_'&f&'_To_'&d, f);
					
set TRANSPORT_TO_OPS := setof{r in TRANSPORTABLE union TRANSPORT_TOKENS, f in LOCATIONS, d in LOCATIONS: f!=d}
					('Transport_'&r&'_From_'&f&'_To_'&d, d);
					
set TRANSPORT_OPS := TRANSPORT_FROM_OPS union TRANSPORT_TO_OPS;


set TRANSPORT_BOP := setof{(o,f) in TRANSPORT_OPS, d in LOCATIONS diff {f}, r in TRANSPORTABLE union TRANSPORT_TOKENS: o == 'Transport_'&r&'_From_'&f&'_To_'&d} 
					('Transport_'&r&'_From_'&f&'_To_'&d, d, r);


set TRANSPORT_BOR := setof {(o,f) in TRANSPORT_FROM_OPS, d in LOCATIONS diff {f}, r in TRANSPORTABLE union TRANSPORT_TOKENS: o == 'Transport_'&r&'_From_'&f&'_To_'&d} 
					('Transport_'&r&'_From_'&f&'_To_'&d, f, r)
					union 
					setof {(o,f) in TRANSPORT_OPS, d in LOCATIONS diff {f}, r in TRANSPORTABLE union TRANSPORT_TOKENS: o == 'Transport_'&r&'_From_'&f&'_To_'&d and d=='DougHouse'} 
					('Transport_'&r&'_From_'&f&'_To_'&d, f, 'Transport_Janey_to_Doug')
					union 
					setof {(o,f) in TRANSPORT_OPS, d in LOCATIONS diff {f}, r in TRANSPORTABLE union TRANSPORT_TOKENS: o == 'Transport_'&r&'_From_'&f&'_To_'&d and d=='JaneyStudio'} 
					('Transport_'&r&'_From_'&f&'_To_'&d, f, 'Transport_Doug_to_Janey');
					#union
					#setof {(o,f) in TRANSPORT_OPS, d in LOCATIONS diff {f}, r in RESOURCE: o == 'Transport_'&r&'_From_'&f&'_To_'&d} 
					#('Transport_'&r&'_From_'&f&'_To_'&d, f, 'Money');

param transport_usage {(o,l,r) in TRANSPORT_BOR} :=
                        if o != 'Transport_'&r&'_From_'&l&'_To_JaneyStudio' and l=='DougHouse' and r == 'Transport_Doug_to_Janey' then smallUsage else
                        if o != 'Transport_'&r&'_From_'&l&'_To_DougHouse' and l=='JaneyStudio' and r == 'Transport_Janey_to_Doug' then smallUsage else
                        
						if o == 'Transport_'&r&'_From_'&l&'_To_JaneyStudio' and l=='DougHouse' then 1 else
						if o == 'Transport_'&r&'_From_'&l&'_To_DougHouse'  and l=='JaneyStudio' then 1 else 0;

param transport_produce {(o,l,r) in TRANSPORT_BOP} := 
						if o == 'Transport_'&r&'_From_DougHouse_To_'&l and l=='JaneyStudio' then 1 else
						if o == 'Transport_'&r&'_From_JaneyStudio_To_'&l and l=='DougHouse' then 1 
						else 0;

param transport_offset {(o,l,r) in TRANSPORT_BOP} := 
    if o == ('Transport_' & r & '_From_JaneyStudio_To_DougHouse') then 1 else 0;

	
###########-------- [COMBINED SETS] --------###########
set OPS = SHIP_OPS union MAKE_OPS union BUY_OPS union SCRAP_OPS union STOCK_OPS union SUB_OPS union TRANSPORT_OPS;

param ops_usage {(o,l) in OPS, r in FULL_RES} :=
    if (o, l, r) in STOCK_BOR then stock_usage[o, l, r]
    else if (o, l, r) in MAKE_BOR then make_usage[o, l, r]
    else if (o, l, r) in SHIP_BOR then ship_usage[o, l, r]
    else if (o, l, r) in BUY_BOR then buy_usage[o, l, r]
    else if (o, l, r) in SCRAP_BOR then scrap_usage[o, l, r]
    else if (o, l, r) in SUB_BOR then subs_usage[o, l, r]
    else if (o, l, r) in TRANSPORT_BOR then transport_usage[o, l, r]
    else 0;

param ops_produce {(o,l) in OPS, r in FULL_RES} :=
    if (o, l, r) in STOCK_BOP then stock_produce[o, l, r]
    else if (o, l, r) in MAKE_BOP then make_produce[o, l, r]
    else if (o, l, r) in SHIP_BOP then ship_produce[o, l, r]
    else if (o, l, r) in BUY_BOP then buy_produce[o, l, r]
    else if (o, l, r) in SCRAP_BOP then scrap_produce[o, l, r]
    else if (o, l, r) in SUB_BOP then subs_produce[o, l, r]
    else if (o, l, r) in TRANSPORT_BOP then transport_produce[o, l, r]
    else 0;
    
param ops_offset {(o,l) in OPS, r in FULL_RES} :=
    if (o, l, r) in STOCK_BOP then stock_offset[o, l, r]
    else if (o, l, r) in MAKE_BOP then make_offset[o, l, r]
    else if (o, l, r) in SHIP_BOP then ship_offset[o, l, r]
    else if (o, l, r) in BUY_BOP then buy_offset[o, l, r]
    else if (o, l, r) in SCRAP_BOP then scrap_offset[o, l, r]
    else if (o, l, r) in SUB_BOP then subs_offset[o, l, r]
    else if (o, l, r) in TRANSPORT_BOP then transport_offset[o, l, r]
    else 0;

###############################################################################################################
###############################################################################################################

### -------------- [VARIABLES (and additional params)] -------------- ###
var Do{OPS, TIME} >= 0 integer;
var rev >=0;
var BinBuy{HAS_MIN union HAS_MAX, TIME} binary;
param BigM = 1e6;
#100*sum{(o,r, l) in SHIP_BOR, c in CUSTOMER: l=='DougHouse'} if r in MATERIAL then ship_usage[o,r,l]*baseprice[c,r] else 0;
param max_time = max{t in TIME} ord(t);

###--------------- [HANDLING OFFSET] ---------------###

param max_offset := max{(o,l) in OPS, r in RESOURCE} ops_offset[o,l,r];

param time_pos {t in TIME} := ord(t);

param x_prev_time {t in TIME, x in 0..max_offset} symbolic :=
    if x = 0 then t  
    else if ord(t) > x then x_prev_time[prev(t), x - 1] 
    else t;
    
param nth_prev {t in TIME, x in 0..max_offset} symbolic :=
    if x = 0 then t
    else nth_prev[prev(t), x - 1];

param prev_time_map {t in TIME, x in 0..max_offset} symbolic :=
    if ord(t) > x then nth_prev[t, x] else t;

### -------------- [OBJECTIVE] -------------- ###
maximize profit: sum{(o,l,'Money') in SHIP_BOP, t in TIME : l=='DougHouse'} (ship_produce[o,l,'Money'] * Do[o,l,t])
			   - sum{(o,l,'Money') in BUY_BOR, t in TIME}(buy_usage[o,l,'Money'] * Do[o,l,t]);
			   

### -------------- [CONSTRAINTS] -------------- ###

subject to Avail {t in TIME, l in LOCATIONS, r in FULL_RES}:
    sum {(o,l) in OPS} (Do[o, l, t] * ops_usage[o, l, r]) =
    full_supply[r, t, l]
    + sum {(o,l) in OPS} (
        if ord(t) > ops_offset[o, l, r]
        then Do[o, l, prev_time_map[t, ops_offset[o, l, r]]] * ops_produce[o, l, r]
        else 0);

subject to EnforceBinBuy {t in TIME, r in HAS_MIN, l in LOCATIONS: l=='DougHouse' and r !='Transport_Janey_to_Doug'}:	#HAS_MIN_BUY_OPS set means you don't need if then logic
	Do['Buy_'&r,l,t] <= BinBuy[r,t] * BigM;

subject to MaxBuy {t in TIME, r in HAS_MAX,l in LOCATIONS: l=='DougHouse'}:
    Do['Buy_'&r,l,t] <= BinBuy[r,t] * max_buy[r,t];

subject to MinBuy {r in HAS_MIN, t in TIME, l in LOCATIONS: l=='DougHouse' and r !='Transport_Janey_to_Doug'}:
    Do['Buy_'&r,l,t] >= BinBuy[r,t] * min_buy[r];
    
    
### Assumption: If you ship one way you have to ship the other way
subject to balance_shipments:
    sum { (o, f, r) in TRANSPORT_BOR, t in TIME : f == 'DougHouse' } Do[o, f, t] = 
    sum { (o, t_loc, r) in TRANSPORT_BOP, t in TIME : t_loc == 'DougHouse' } Do[o, t_loc, t];
;

subject to revenue: rev = sum{(o,l,'Money') in SHIP_BOP, t in TIME : l=='DougHouse'} (ship_produce[o,l,'Money'] * Do[o,l,t]);

###############################################################################################################
###############################################################################################################
#data hw9_v2.dat;
#data hw8tiny1.dat;
#data hw9_tinydat.dat;
#data regression_testing.dat;
data hw9_tiny2.dat
solve;
display Do;
display profit;
display rev;
