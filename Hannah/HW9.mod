set MATERIAL;											#set of materials
set CAPACITY;	
set RESOURCE = MATERIAL union CAPACITY;	
set MAKE_OPS;
set SHIP_OPS;
set BUY_OPS;
set BACKLOG_OPS default {};
set OTHER_OPS default {};
set OPERATION = MAKE_OPS union SHIP_OPS  union BUY_OPS union OTHER_OPS;
set BOR within {OPERATION, RESOURCE};
set BOP within {OPERATION, RESOURCE};
set TIME ordered;

param usage {BOR};
param produce {BOP};
param offset {BOP} default 0;
param BigM := 10* sum {k in SHIP_OPS, d in MATERIAL: (k,d) in BOR} produce[k,"Money"]*usage[k, d] ;
param alpha := .001;
param supply {RESOURCE,TIME} default 0;
param unit_cost {OPERATION,TIME} default alpha;
param min_buy {BUY_OPS} default 1;
param max_op{OPERATION, TIME} default BigM;	
param p_disc default .001;

var Amt_Ops{k in OPERATION, t in TIME} >=0, <=max_op[k,t], integer;
var BinBuy {BUY_OPS, TIME} binary;    # if any purchased 
var TotRev;
var Prft;

maximize Profit:
	sum {t in TIME}(
		 sum{ (k, "Money") in BOP} (produce[k,"Money"])* Amt_Ops[k,t]
 		 - sum{ (k, "Money") in BOR} (usage[k,"Money"])* Amt_Ops[k,t]
		 - sum {k in OPERATION} (unit_cost[k,t]* Amt_Ops[k,t])
);
# constraint 
subject to Res_Balance  {t in TIME, r in RESOURCE}: 
sum { (k,r) in BOR} usage [k,r] * Amt_Ops[k,t] 
= sum  { (k,r) in BOP} 
	(if ord(t)-offset[k,r]>=1 then produce [k,r] * Amt_Ops[k,prev(t,offset[k,r])]
	else 0) 
	+ supply[r,t];
#for minimum purchase quantities  
subject to ForceBin {t in TIME, k in BUY_OPS }:
			Amt_Ops[k,t]<= BigM*BinBuy[k,t];			
subject to ForceMin { t in TIME,k in BUY_OPS}:
			Amt_Ops[k,t] >= min_buy[k]*BinBuy[k,t]; 


subject to ComputeRevenue: TotRev= sum{t in TIME, (k, "Money") in BOP} produce[k,"Money"]* Amt_Ops[k,t];
subject to ComputeProfit: Prft = TotRev 
		- sum{t in TIME,  (k, "Money") in BOR} (usage[k,"Money"])* Amt_Ops[k,t];			

