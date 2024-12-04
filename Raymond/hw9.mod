set MATERIAL;
set CAPACITY;
set DEMAND;
set RESOURCE := MATERIAL union CAPACITY;

set OTHER_OPS;
set SHIP_Nolate_OPS;
set SHIP_Late_OPS;
set SHIP_OPS = SHIP_Nolate_OPS union SHIP_Late_OPS;

#set OFFSET {OPERATION, RESOURCE} default 0;
set TIME ordered;
set OPS = SHIP_OPS union OTHER_OPS;
set BOR within {OPS, RESOURCE};
set BOP within {OPS, RESOURCE};

# Parameters
param usage {BOR}; 
param produce {BOP}; 

param supply {RESOURCE, TIME} default 0;
param demand {DEMAND, TIME} default 0;

 
param demand_lb{o in SHIP_OPS,t in TIME} default 0; # lower bound on shipment in t

param min_ops {OPS} default 1;
param max_ops {OPS, TIME} default 10000; 

param BigM := 10000000;

param offset {BOP} default 0;

set HAS_MIN :=setof{r in OPS: min_ops[r]>=2} r;

# Variables
# var Backlog{o in SHIP_OPS, t in TIME} >=0;    #  shortage relative to demand 

var Stock{RESOURCE,TIME} >=0;    # stocked MATERIAL

var Scrap{RESOURCE,TIME} >=0; # scrapped RESOURCE (not allowed or products)       # self sub vaiable  # sub variables, excludes self sub. 

var BinBuy {HAS_MIN,TIME} binary;    # if any purchased 

var Z {o in OPS, t in TIME} <= max_ops[o,t], >=0, integer;

var TotRev = sum {t in TIME}(
		 sum{ (k, "Money") in BOP} (produce[k,"Money"])* Z[k,t]);  
/*
maximize Profit: 
 #profit part
 sum {t in TIME} (
     sum{o in SHIP_OPS, r in RESOURCE: r="Money"} (produce[o,r] * Z[o,t])
     - sum {o in OTHER_OPS, r in RESOURCE: r="Money"} (usage[o,r] * Z[o,t])); */
     
maximize Profit: 
 #profit part
     sum {t in TIME}(
		 sum{ (k, "Money") in BOP} (produce[k,"Money"])* Z[k,t]
 		 - sum{ (k, "Money") in BOR} (usage[k,"Money"])* Z[k,t]);
  
/*   
subject to C_Ship {t in TIME,o in SHIP_OPS }: # cumulative shipment does not exceed cummulative demand
 Backlog [o,t]= demand[o,t] 
   + sum {s in TIME: ord(s)<ord(t)} demand[o,s]
   -(Z[o,t] 
   + sum {s in TIME: ord(s)<ord(t)} Z[o,s] ) ;
*/   

/*  
subject to C_Ship {t in TIME,o in SHIP_OPS, d in DEMAND }: # cumulative shipment does not exceed cummulative demand
 Backlog [o,t]= ( if o=='Ship_'&d then  demand[d,t] else 0 ) 
   + (if o in SHIP_OPS diff SHIP_Nolate_OPS then 
   sum {s in TIME: ord(s)<ord(t)} ( if o=='Ship_'&d then  demand[d,s] else 0 ))
   -(Z[o,t] 
   + (if o in SHIP_OPS diff SHIP_Nolate_OPS then
   sum {s in TIME: ord(s)<ord(t)} Z[o,s] )) ;
*/   

subject to Avail {t in TIME,r in RESOURCE}:               #Resource balance 
 sum { (o,r) in BOR} (Z[o,t] * usage[o,r])       # used as self, no sub possible 
  + (if r in RESOURCE then Stock[r,t] else 0)             #stock if material 
  + (if r in RESOURCE then Scrap[r,t] else 0)
  = supply[r,t]
  + (if ord(t)>1 and r in MATERIAL then Stock [r,prev(t, TIME)] else 0 )         #only if not first period
  + (sum{(o,r) in BOP}	(if ord(t)-offset[o,r]>=1 then produce [o,r] * Z[o,prev(t,offset[o,r])]
	else 0));  #Z[r,t] * produce[o,r])
  

subject to cummulative_demand1 {o  in SHIP_Late_OPS , t in TIME}:
   sum { d in DEMAND, s in TIME: ord(s)<=ord(t)}
      (if o == 'Ship_'&d
           then  demand[d,s] else 0 )
       >=    
 	 sum{s in TIME: ord(s)<=ord(t)} Z[o,s];


subject to cummulative_demand2 {o in SHIP_Nolate_OPS, t in TIME}:
  sum{ d in DEMAND}
      ( if o=='Ship_'&d
           then  demand[d,t] else 0 )
       >=    
 	  Z[o,t];


#for minimum purchase quantities  
subject to ForceBin {t in TIME, r in HAS_MIN }:
			Z[r,t]<= BigM*BinBuy[r,t];			
subject to ForceMin { t in TIME,r in HAS_MIN}:
			Z[r,t] >= min_ops[r]*BinBuy[r,t]; 
  
  

;

