from fastvk.fsm import State, StatesGroup


class SearchFilmRating(StatesGroup):
    rating = State()
    page = State()
