from fastvk.fsm import State, StatesGroup

class History(StatesGroup):
    history_page = State()
    viewing = State()
    evaluation = State()

class NewEvaluation(State):

    film_name = State()
    evaluation = State()

class DateTimeFilm(State):

    start_date = State()
    # end_date = State()
    page = State()