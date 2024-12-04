
# HELPERS
import pandas as pd
def save_to_excel(REFACTOR, stats, solver, Exec, target):
    #give plan/run stats
    stats_index = ["Revenue", "Profit", "Objective"]
    stats_sheet = {**stats, "Plan results": stats_index}
    stats_sheet = pd.DataFrame(stats_sheet).set_index("Plan results")
    #make the excel sheets for the ops
    ship_index = [op for op in REFACTOR.SHIPOPS]
    sub_index = [op for op in REFACTOR.SUBOPS]
    make_index = [op for op in REFACTOR.MAKEOPS]
    buy_index = [op for op in REFACTOR.BUYOPS]
    scrap_index = [op for op in REFACTOR.SCRAPOPS]
    stock_index = [op for op in REFACTOR.STOCKOPS]
    transport_index = [op for op in REFACTOR.TRANSPORTOPS]
    
    ship_sheet = {**{t: [0]*len(ship_index) for t in REFACTOR.TIME},"Operations": ship_index}
    sub_sheet = {**{t: [0]*len(sub_index) for t in REFACTOR.TIME}, "Operations": sub_index}
    make_sheet = {**{t: [0]*len(make_index) for t in REFACTOR.TIME}, "Operations": make_index}
    buy_sheet = {**{t: [0]*len(buy_index) for t in REFACTOR.TIME}, "Operations": buy_index}
    scrap_sheet = {**{t: [0]*len(scrap_index) for t in REFACTOR.TIME}, "Operations": scrap_index}
    stock_sheet = {**{t: [0]*len(stock_index) for t in REFACTOR.TIME}, "Operations": stock_index}
    transport_sheet = {**{t: [0]*len(transport_index) for t in REFACTOR.TIME}, "Operations": transport_index}


    ship_sheet = pd.DataFrame(ship_sheet).set_index("Operations")
    sub_sheet = pd.DataFrame(sub_sheet).set_index("Operations")
    make_sheet = pd.DataFrame(make_sheet).set_index("Operations")
    buy_sheet = pd.DataFrame(buy_sheet).set_index("Operations")
    scrap_sheet = pd.DataFrame(scrap_sheet).set_index("Operations")
    stock_sheet = pd.DataFrame(stock_sheet).set_index("Operations")
    transport_sheet = pd.DataFrame(transport_sheet).set_index("Operations")

    for t in REFACTOR.TIME:
        for op in REFACTOR.OPS:
            if op in REFACTOR.MAKEOPS:
                if Exec[op, t].solution_value() > 0.1:
                    make_sheet.loc[(op, t)] = Exec[op, t].solution_value()


            elif op in REFACTOR.SHIPOPS:
                if Exec[op, t].solution_value() > 0.1:
                    ship_sheet.loc[(op, t)] = Exec[op, t].solution_value()

            elif op in REFACTOR.BUYOPS:
                if Exec[op, t].solution_value() > 0.1:
                    buy_sheet.loc[(op, t)] = Exec[op, t].solution_value()

            elif op in REFACTOR.SUBOPS:
                if Exec[op, t].solution_value() > 0.1:
                    sub_sheet.loc[(op, t)] = Exec[op, t].solution_value()

            elif op in REFACTOR.SCRAPOPS:
                if Exec[op, t].solution_value() > 0.1:
                    scrap_sheet.loc[(op, t)] = Exec[op, t].solution_value()

            elif op in REFACTOR.STOCKOPS:
                if Exec[op,t].solution_value() > 0.1:
                    stock_sheet.loc[(op, t)] = Exec[op, t].solution_value()

            elif op in REFACTOR.TRANSPORTOPS:
                if Exec[op,t].solution_value() > 0.1:
                    transport_sheet.loc[(op, t)] = Exec[op, t].solution_value()


    with pd.ExcelWriter(target) as writer:
        stats_sheet.to_excel(writer, sheet_name="Plan results", index=True)
        ship_sheet.to_excel(writer, sheet_name="Ship", index=True)
        make_sheet.to_excel(writer, sheet_name="Make", index=True)
        buy_sheet.to_excel(writer, sheet_name="Buy", index=True)
        sub_sheet.to_excel(writer, sheet_name="Sub", index=True)
        scrap_sheet.to_excel(writer, sheet_name="Scrap", index=True)
        stock_sheet.to_excel(writer, sheet_name="Stock", index=True)
        transport_sheet.to_excel(writer, sheet_name="Transport", index=True)
def prev(TIME, t, n = 1):
    """
        Helper method to select an element from an ordered set.
        :param TIME: Ordered set
        :param t: index of current element
        :param n: shift steps
        :return: element at requested position
        """
    return TIME[TIME.index(t) - n]

def create_op(mat, op_type, destination=None, origin=None, customer=None, r1=None, r2=None):
    if op_type == "ship":
        if customer is None:
            raise Exception("ship ops require customer parameter")
        else:
            return f"Sh_{customer}_{mat}"
    elif op_type == "sub":
        if r1 is None or r2 is None:
            raise Exception("sub ops require r1 and r2 args")
        else:
            return f"Su_{mat}_{r1}_{r2}"
    elif op_type == "buy":
        return f"B_{mat}"
    elif op_type == "make":
        return f"M_{mat}"
    elif op_type == "scrap":
        return f"Sc_{mat}"
    elif op_type == "stock":
        return f"St_{mat}"
    elif op_type == "transport":
        return f"T_To{destination}_From{origin}_{mat}"
    else:
        raise Exception("Unrecognized op_type")

def parse_op(op):
    if op[:2] == "Sh":
        return "ship", op[3:]
    elif op[:1] == "B":
        return "buy", op[2:]
    elif op[:1] == "M":
        return "make", op[2:]
    elif op[:2] == "Sc":
        return "scrap", op[3:]
    elif op[:2] == "St":
        return "stock", op[3:]
    elif op[:2] == "Su":
        return "sub", op[3:]
    elif op[:1] == "T":
        return "transport", op[2:]
    #TODO: fix hardcode later
    elif op in {"DougBuys", "DougShips", "SendsToStudio", "SendsToGarage"}:
        return "action", op
    else:
        raise Exception("unrecognized op_type")

def parse_sub_op(sub_op):
    typ, p_r1_r2 = parse_op(sub_op)
    p, r1, r2 = parse_sub_suffix(p_r1_r2)
    return typ, p, r1, r2

def parse_ship_op(ship_op):
    typ, c_p = parse_op(ship_op)
    c, p = parse_ship_suffix(c_p)
    return typ, c, p

def parse_transport_op(transport_op):
    typ, td_fo_m = parse_op(transport_op)
    d, o, m = parse_transport_suffix(td_fo_m)
    return typ, d, o, m

def parse_ship_suffix(cust_and_prod):
    split_on = cust_and_prod.index('_')
    customer, prod = cust_and_prod[:split_on], cust_and_prod[split_on + 1:]
    return customer, prod


def parse_sub_suffix(p_r1_r2):
    split_on = p_r1_r2.index('_')
    p, r1_r2 = p_r1_r2[:split_on], p_r1_r2[split_on + 1:]
    split_on = r1_r2.index('_')
    r1, r2, = r1_r2[:split_on], r1_r2[split_on+1:]

    return p, r1, r2

def parse_transport_suffix(toD_fromO_mat):
    split_on = toD_fromO_mat.index('_')
    toD, fromO_mat = toD_fromO_mat[:split_on], toD_fromO_mat[split_on+1:]
    dest = toD[2:]
    split_on = fromO_mat.index('_')
    orig, mat = fromO_mat[:split_on], fromO_mat[split_on + 1:]
    return dest, orig, mat



#not abstractable, but fine for now

def get_mat_location(mat):
    if mat[:6] == "Studio":
        return "Studio" if mat[-6:] == "Studio" else ""
def change_mat_location(mat, destination):
    if get_mat_location(mat) == "Studio":
        return mat[:-6]
    else:
        return mat + "Studio"
