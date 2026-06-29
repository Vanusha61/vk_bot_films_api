from fastvk.fsm import State, StatesGroup

class SearchFilmName(StatesGroup):
    name = State()
    page = State()