import sys
sys.path.append("releaseMaterials")
from Hw9_helpers import *
from collections import defaultdict
"""

accepts: exact same parameters as HW 7 model (or less)

returns: old_data for HW8 model

"""
class Refactor:
    def __init__(self, MATERIAL=None, LOCATION=None, CAPACITY=None, CUSTOMER=None, NO_LATE=None, LOW_PRIORITY=None,BUYSandSHIPS=None,
                 IS_SHIPPED=None, TIME=None, NEEDS_LARGE_BOX=None, HAS_OFFSET=None, usage=None, sub_usage=None, baseprice=None, p_disc=None, demand=None, supply=None, ord_qty=None,
                 ord_cost=None, init_funds=None, ord_offset=None, default_location=None, min_buy=None, max_buy=None, mult=None, scrap_pen=None, init_stoc = None, stoc_pen=None,
                 sub_pen = None, make_pen=None, demand_lb={}, beta_weight=0, epsilon=100000, alpha = .5):

        ###TODO: baseprice setup?
        ###TODO: convert dicts to op dicts as appropriate and handle accordingly?
        """
        might seem unnecessary / clutter to turn a lot of these into class parameters, but makes it much easier to
        easily write class methods, and distinguish which data has not been processed (feature in __init__() args) vs
        which has been (class params)
        """

        ###leave in original form, store for easier access if necessary later
        self.init_funds = init_funds
        self.p_disc = p_disc
        self.CAPACITY = CAPACITY
        self.HAS_OFFSET = HAS_OFFSET

        self.LOCATION = LOCATION
        self.TIME = TIME
        self.IS_SHIPPED = IS_SHIPPED
        self.NO_LATE = NO_LATE
        self.usage = usage

        self.PROD = {p for (p, r) in self.usage.keys()}
        self.MATERIAL = {f"{m}{l}" for m in MATERIAL for l in LOCATION} #make a material for new lcoations
        self.RESOURCE = (self.MATERIAL.union(self.CAPACITY))
        self.sub_usage = sub_usage
        # self.sub_usage = {**sub_usage, **{(p, "LBox", "SBox"): 1 for p in self.PROD if p not in NEEDS_LARGE_BOX}}

        ###create default dicts, but leave in original form
        self.init_stoc = defaultdict(lambda: 0, init_stoc)
        self.baseprice = defaultdict(lambda: 0, baseprice)
        self.supply = defaultdict(lambda: 0, supply)
        ###dicts w/ operation penalties
        self.scrap_pen = defaultdict(lambda: alpha, {create_op(k, "scrap"): v for k, v in scrap_pen.items()})
        self.stoc_pen = defaultdict(lambda: .5 * alpha, {create_op(k, "stock"): v for k, v in stoc_pen.items()})
        self.sub_pen = defaultdict(lambda: 2*alpha, {create_op(k, "sub"): v for k,v in sub_pen.items()})
        self.make_pen = defaultdict(lambda:alpha, {create_op(k, "make"): v for k,v in make_pen.items()})
        ###dicts w/ information about operations
        self.demand_lb = defaultdict(lambda: 0, {create_op(m, "ship"): lb for m, lb in demand_lb.items()})
        self.demand = defaultdict(lambda: [0] * len(TIME), {create_op(r, "ship", customer=c): d for (r, c), d in demand.items()})
        ###Could change these back to resources?
        self.ord_cost = defaultdict(lambda: 0, {create_op(r, "buy"): v for r,v in ord_cost.items()})
        self.ord_qty = defaultdict(lambda: 0, {create_op(r, "buy"): v for r,v in ord_qty.items()})
        self.ord_offset = defaultdict(lambda: 0, {create_op(r, "buy"): v for r,v in ord_offset.items()})
        ###max buy uses list, but min_buy usese integers, so force both to be lists
        list_min_buy =  {k: v if (type(v) == list) else ([v]*len(TIME)) for k, v in min_buy.items()}
        list_max_buy =  {k: v if (type(v) == list) else ([v]*len(TIME)) for k, v in max_buy.items()}
        self.min_buy = defaultdict(lambda: [1]*len(TIME),{create_op(r, "buy"): v for r, v in list_min_buy.items()})
        self.max_buy = defaultdict(lambda: [1e9]*len(TIME), {create_op(r, "buy"): v for r, v in list_max_buy.items()})
        ### dicts to bound ops
        self.lower_bds = {**self.min_buy, **self.demand_lb}
        self.upper_bds = {**self.max_buy}
        #### FINAL OPERATION SETS
        self.shipable = {p for p in self.PROD}
        self.buyable = {r for r in self.RESOURCE if
                        (self.ord_cost[create_op(r, "buy")] * self.ord_qty[
                            create_op(r, "buy")] > 0)}  ### has buying data, need Buy vars
        self.makeable = {p for p in self.PROD}
        self.scrapable = {r for r in  self.RESOURCE}
        self.stockable = {m for m in self.MATERIAL}
        self.transportable = {m for m in self.MATERIAL}
        self.subable = {(p, r1, r2) for p,r1,r2 in self.sub_usage}
        ###create actual ops
        self.SUBOPS = {create_op(su, "sub", r1=r1, r2=r2) for su, r1, r2 in self.subable}
        self.BUYOPS = {create_op(b, "buy") for b in self.buyable}
        self.SHIPOPS = {create_op(sh, "ship", customer=c) for sh in self.shipable for c in CUSTOMER}
        self.MAKEOPS = {create_op(m, "make") for m in self.makeable}
        self.SCRAPOPS = {create_op(sc, "scrap") for sc in self.scrapable}
        self.STOCKOPS = {create_op(st, "stock") for st in self.stockable}
        self.ACTIONOPS = {"DougBuys", "DougShips", "SendsToStudio", "SendsToGarage"}
        self.TRANSPORTOPS = {create_op(m, 'transport', destination=l1, origin=l2) for m in self.transportable
                             for l1 in self.LOCATION for l2 in self.LOCATION if l1 != l2} #make op transporting from every location to every other location
        self.OPS = (self.BUYOPS | self.SHIPOPS | self.MAKEOPS | self.SCRAPOPS | self.STOCKOPS | self.SUBOPS |
                    self.ACTIONOPS | self.TRANSPORTOPS)
        self.BOP = defaultdict(lambda: 0, self.create_BOP())
        self.BOR = defaultdict(lambda: 0, self.create_BOR())
        ###OUTPUT DICTIONARY
        self.new_data = {
                        "OPS": self.OPS,
                        "BOR": self.BOR,
                        "BOP": self.BOP,
                        "MATERIAL": self.MATERIAL,
                        "PROD": self.PROD,
                        "NO_LATE": self.NO_LATE,
                        "RESOURCE": self.RESOURCE,
                        "CAPACITY": self.CAPACITY,
                        "TIME": self.TIME,
                        "HAS_OFFSET": self.HAS_OFFSET,
                        "usage": self.usage,
                        "ord_offset": self.ord_offset,
                        "baseprice": self.baseprice,
                        "demand": self.demand,
                        "demand_lb": self.demand_lb,
                        "supply": self.supply,
                        "min_buy": self.min_buy,
                        "sub_usage": self.sub_usage,
                        "init_stoc": self.init_stoc,
                        "init_funds": self.init_funds,
                        "p_disc": self.p_disc,
                        "max_buy": self.max_buy,
                        "sub_pen": self.sub_pen,
                        "make_pen": self.make_pen,
                        "scrap_pen": self.scrap_pen,
                        "stoc_pen": self.stoc_pen,
                         }

    #INITIALIZE BORS AND BOPS ON CASE BY CASE BASIS
    def create_BOR(self):
        return {**self.init_make_BOR(), **self.init_buy_BOR(), **self.init_ship_BOR(), **self.init_scrap_BOR(),
                **self.init_sub_BOR(), **self.init_stock_BOR(), **self.init_action_BOR(), **self.init_transport_BOR()}

    def create_BOP(self):
        return {**self.init_make_BOP(), **self.init_buy_BOP(), **self.init_ship_BOP(), **self.init_scrap_BOP(),
                **self.init_sub_BOP(), **self.init_stock_BOP(), **self.init_action_BOP(), **self.init_transport_BOP()}

    def init_make_BOR(self):
        make_BOR = {}
        for op in self.MAKEOPS:
            _, p = parse_op(op)
            make_BOR = {**make_BOR, **{(op, r): self.usage[p,r] for r in self.RESOURCE if (p, r) in self.usage.keys()}}

        return make_BOR

    def init_sub_BOR(self):
        sub_BOR = {}
        for op in self.SUBOPS:
            _, p, r1, r2 = parse_sub_op(op)
            sub_BOR[op, r2] = self.sub_usage[p, r1, r2] ###cost of subbing r2 for r1

        return sub_BOR

    def init_ship_BOR(self):
        ship_BOR = {}
        for op in self.SHIPOPS:
            _, c, p = parse_ship_op(op)
            ship_BOR[op, p] = 1
            if c == "Online":
                ship_BOR[op, 'LBox'] = 1 #default to large box, add small as subs except for Large beds

        return ship_BOR

    def init_scrap_BOR(self):
        scrap_BOR = {}
        for op in self.SCRAPOPS:
            _, r = parse_op(op)
            scrap_BOR[op, r] = 1

        return scrap_BOR

    def init_buy_BOR(self):
        buy_BOR = {}
        for op in self.BUYOPS:
            _, r = parse_op(op)
            buy_BOR[op, 'cash'] = self.ord_cost[op]

        return buy_BOR

    def init_stock_BOR(self):
        stock_BOR = {}
        for op in self.STOCKOPS:
            _, r = parse_op(op)
            stock_BOR[op, r] = 1

        return stock_BOR

    def init_transport_BOR(self):
        transport_BOR = {}
        for op in self.TRANSPORTOPS:
            typ, d, o, m = parse_transport_op(op)
            transport_BOR[op, m] = 1

        return transport_BOR

    #hard code these because limited cases and hard to abstract
    def init_action_BOR(self):
        action_BOR = {}
        action_BOR["DougBuys", "Labor"] = 120
        action_BOR["DougShips", "Labor"] = 120
        action_BOR["SendsToStudio", "cash"] = 30
        action_BOR["SendsToGarage", "cash"] = 50
        return action_BOR


    def init_make_BOP(self):
        make_BOP = {}
        for op in self.MAKEOPS:
            _, p = parse_op(op)
            make_BOP[op, p] = 1

        return make_BOP


    def init_ship_BOP(self):
        ship_BOP = {}
        for op in self.SHIPOPS:
            _, c_p = parse_op(op)
            c, p = parse_ship_suffix(c_p)
            ship_BOP[op, 'cash'] = self.baseprice[p, c] ###index by product, customer

        return ship_BOP

    def init_scrap_BOP(self):
        scrap_BOP = {}

        return scrap_BOP

    def init_buy_BOP(self):
        buy_BOP = {}
        for op in self.BUYOPS:
            _, r = parse_op(op)
            buy_BOP[op, r] = self.ord_qty[op]
        return buy_BOP

    def init_stock_BOP(self):
        stock_BOP = {}

        return stock_BOP

    def init_sub_BOP(self):
        sub_BOP = {}
        for op in self.SUBOPS:
            _, suff = parse_op(op)
            p, r1, r2 = parse_sub_suffix(suff)
            #TODO: abstract this
            if r1 == "LBox":
                sub_BOP[op, "LBox"] = 1
            else:
                sub_BOP[op, r1] = self.usage[p, r1]  ### subbing r2 for r1 gives back amount of r1 otherwise in p

        return sub_BOP


    def init_transport_BOP(self):
        transport_bop = {}
        for op in self.TRANSPORTOPS:
            typ, d, o, m = parse_transport_op(op)
            transport_bop[op, change_mat_location(m, d)] = 1
        return transport_bop

    def init_action_BOP(self):
        return {}



