# import pandas as pd
import pandas as pd
import numpy as np
# Data
MATERIAL = {'R1', 'R2', 'S1', 'S2', 'P1', 'P2'}  # set of materials
CAPACITY = {'C1', 'C2'}  # set of capacities

TIME = ['day1', 'day2', 'day3']
CUSTOMER = {'Cu1', 'Cu2'}
NO_LATE = {'Cu2'}
IS_SHIPPED = {'Cu2'}
HAS_OFFSET = {'S1'}
LOCATION = {'L1', ''}


usage = {  # usage data given as list of Prod, resource qty
    # BOM is defined through this list
    ('P1', 'S1'): 1,
    ('P1', 'C1'): 1,
    ('P2', 'S2'): 1,
    ('P2', 'C2'): 1,
    ('S1', 'R1'): 4,
    ('S2', 'R2'): 2 }

p_disc = .02

baseprice = {  # product price
('Cu1','R1'): 2,
('Cu1','R2'): 1,
('Cu1','S1'): 8,
('Cu1','S2'): 4,
('Cu1','P1'): 32,
('Cu1','P2'): 16,

('Cu2', 'R1'): 1,
('Cu2', 'R2'): 2,
('Cu2', 'S1'): 4,
('Cu2', 'S2'): 8,
('Cu2', 'P1'): 16,
('Cu2', 'P2'): 32
}

demand = {  # day1 day2 day3 		#product  demand

    ('Cu1','R1'): [1, 2, 3],
    ('Cu1','R2'): [1, 2, 3],
    ('Cu1','S1'): [1, 2, 3],
    ('Cu1','S2'): [1, 2, 3],
    ('Cu1','P1'): [0, 5, 10],
    ('Cu1','P2'): [5, 10, 15],

    ('Cu2', 'R1'): [1, 2, 3],
    ('Cu2', 'R2'): [1, 2, 3],
    ('Cu2', 'S1'): [1, 2, 3],
    ('Cu2', 'S2'): [1, 2, 3],
    ('Cu2', 'P1'): [5, 10, 15],
    ('Cu2', 'P2'): [0, 5, 10],

}

scrap_pen = {  # scrap penalty
    'R1': .025,
    'R2': .025,
    'S1': 1,
    'S2': 1,
    'P1': 100,
    'P2': 100,
    'C1': .025,
    'C2': .025}

stoc_pen = {  # small numbers
    'R1': .05,
    'R2': .10,
    'S1': .2,
    'S2': .4,
    'P1': .8,
    'P2': .10}

supply = {  # day1 day2 day3 		#resource supply
    ('R1', 'day1'): 5,
    ('R2', 'day1'): 12,
    ('S1', 'day1'): 5,
    ('S2', 'day1'): 10,
    ('P1', 'day1'): 0,
    ('P2', 'day1'): 2,
    ('C1', 'day1'): 20,
    ('C2', 'day1'): 0,

    ('R1', 'day2'): 10,
    ('R2', 'day2'): 25,
    ('S1', 'day2'): 0,
    ('S2', 'day2'): 0,
    ('P1', 'day2'): 0,
    ('P2', 'day2'): 0,
    ('C1', 'day2'): 10,
    ('C2', 'day2'): 10,

    ('R1', 'day3'): 20,
    ('R2', 'day3'): 30,
    ('S1', 'day3'): 0,
    ('S2', 'day3'): 0,
    ('P1', 'day3'): 0,
    ('P2', 'day3'): 0,
    ('C1', 'day3'): 10,
    ('C2', 'day3'): 10}

sub_usage = {  # defines SUB_TRIPLES as list.
    ('S1', 'R1', 'R2'): 2,  # sets suage values
    ('P2', 'C2', 'C1'): 1,
    ('P1', 'S1', 'S2'): 3}

ord_qty = {
'R1': 10 ,
'R2': 5 }
ord_cost = {
'R1' : 10 ,
'R2' : 15 }
ord_offset = {
    'S1': 1
}
min_buy = {
'R1' : 1 ,
'R2' : 1 }


max_buy = {'R2': 4}
init_cash = 150

tiny_dict = {"MATERIAL": MATERIAL,
             "CAPACITY": CAPACITY,
             "TIME": TIME,
             "LOCATION": LOCATION,
             "HAS_OFFSET": HAS_OFFSET,
             "ord_offset": ord_offset,
             "p_disc": p_disc,
             "usage": usage,
             "baseprice": baseprice,
             "demand": demand,
             "supply": supply,
             "scrap_pen": scrap_pen,
             "init_stoc": {'cash': init_cash},
            "min_buy": min_buy,
             "max_buy": max_buy,
             "ord_cost": ord_cost,
             "ord_qty": ord_qty,
             "stoc_pen": stoc_pen,
             "sub_pen": {},
             "make_pen": {},
             "sub_usage": sub_usage}