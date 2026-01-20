from aiogram.fsm.state import StatesGroup, State


class UserSG(StatesGroup):
    main = State()
    settings = State()

    arm_settings = State()
    genesys_settings = State()
