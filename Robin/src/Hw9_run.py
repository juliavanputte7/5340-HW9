from Hw9_model import Hw9_model
from Hw9_Refactor import Refactor
from Hw9_TINY import tiny_dict
from Hw9_data import data_dict
# from Hw8_data import data_dict
from Hw9_model import *

if __name__ == '__main__':
    # use_tiny = True
    # data_dict = tiny_dict if use_tiny else data_dict

    REFACTOR = Refactor(**data_dict)
    refactored_dict = REFACTOR.new_data
    stats, solver, Exec = Hw9_model(REFACTOR, **refactored_dict)
    save_to_excel(REFACTOR, stats, solver, Exec, "hw9_out.xlsx")
