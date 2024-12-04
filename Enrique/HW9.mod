var DoOp {TIME, OPERATION} integer >= 0; # number of times to do an operation in a period
var OpBin {TIME, HAS_MIN} binary; # for operations with nonzero minimums, binary variable for if it is done
var Sub {TIME, SUBSTITUTIONS} >=0 integer;	# sub variables, excludes self sub. 
var Selfsub {TIME, SUB_PAIRS} >= 0 integer;	# self sub vaiables (prime used)
var TotalProfit;
var TotRev;
var TotCost;

maximize profit : TotalProfit  - sum {k in OPERATION, t in TIME} penalty[k] * DoOp[t,k];

subject to ComputeProfit: 
	TotalProfit = TotRev - TotCost;

subject to ComputeRevenue : 
	TotRev = # money production is revenue
	sum {k in SHIP_OP, t in TIME} (if (k,"Money") in BOP then produce[k, "Money"] else 0) * DoOp[t, k]; 

subject to ComputeCost : 
	TotCost = # money usage is cost
	sum {k in PROC_OP union DRIV_OP, t in TIME} (if (k,"Money") in BOR then use[k,"Money"] else 0) * DoOp[t, k];
	
subject to ResourceBalance {r in RESOURCE, t in TIME} :
	sum {(p,r) in BOR diff SUB_PAIRS} (DoOp[t,p] * use[p,r])   		# used as self, no sub possible 
	+ sum {(p,r) in SUB_PAIRS}  (Selfsub[t,p,r] * use[p,r]) 			# has subs, used as prime
	+ sum {(p,j,r) in SUBSTITUTIONS} (Sub[t,p,j,r] * sub_use[p,j,r]) 	# used as sub 
	= new_supply[r,t]  # newly introduced quantity
	+ sum {(k,r) in BOP} (if ord(t) > offset[k, r] then produce[k, r] * DoOp[prev(t, offset[k, r]),k] else 0); # production, based on offset

subject to Same_make {t in TIME, (op,r) in SUB_PAIRS}:	 # operation is either done with prime or a substitute
	DoOp[t,op] = Selfsub[t,op,r] + sum {(op,r,q) in SUBSTITUTIONS} Sub[t,op,r,q];	
		
subject to Maximums {t in TIME, op in HAS_MAX} : # operations can't be done more than their maximum number of times
	DoOp[t, op] <= maximum[op, t];	
 
subject to EnforceBinary {t in TIME, op in HAS_MIN} : # if DoOp > 0, the OpBin must be 1
	DoOp[t, op] <= bigM * OpBin[t, op];
	
subject to Minimums {t in TIME, op in HAS_MIN} : # if OpBin = 1, the DoOp > minimum
	DoOp[t, op] >= minimum[op] * OpBin[t, op];
