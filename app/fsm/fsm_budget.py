from fastvk.fsm import State, StatesGroup

class BudgetStatesMin(StatesGroup):
    budget_mins = State()
    page = State()

class BudgetStatesMax(StatesGroup):
    budget_maxs = State()
    page = State()