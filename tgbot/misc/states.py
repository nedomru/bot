from aiogram.fsm.state import StatesGroup, State


class SalaryCountStates(StatesGroup):
    COUNT_TYPE = State()
    PREMIUM_PERCENT = State()
    POSITION = State()
    HOURS_WORKED = State()
    AHT = State()
    FLR = State()
    GOK = State()
    CLIENT_RATING = State()
    TESTS = State()
    ACKNOWLEDGMENTS = State()
    MENTOR = State()
    MENTOR_TYPE = State()
    MENTOR_DAYS = State()
    LAST_BOT_MESSAGE_ID = State()