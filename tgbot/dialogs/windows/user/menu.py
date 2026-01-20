from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Url,
    WebApp,
    Group,
    Back,
    Start,
    SwitchTo,
    Row,
    Column,
    Checkbox,
)
from aiogram_dialog.widgets.text import Const, Format, Multi

from tgbot.dialogs.events.user import (
    on_arm_setting_click,
    on_genesys_setting_click,
)
from tgbot.dialogs.getters.user import (
    settings_getter,
    arm_settings_getter,
    genesys_settings_getter,
    ARM_SETTINGS_OPTIONS,
    GENESYS_SETTINGS_OPTIONS,
)
from tgbot.dialogs.states.user import UserSG


menu_window = Window(
    Const("<b>☎️ Главное меню</b>\n\nЯ - бот проекта <b>Не Дом.ру</b>\n"),
    Start(Const("⚙️ Настройки Хелпера"), state=UserSG.settings, id="settings"),
    Group(
        Url(Const("🤝 Группа"), url=Const("https://t.me/+2vVZ0vXJiWFkOWZi")),
        Url(Const("📺 Канал"), url=Const("https://t.me/+jH1mblw0ytcwOWUy")),
    ),
    Group(
        WebApp(Const("✏️ Фломастер"), url=Const("https://flomaster.chrsnv.ru/")),
    ),
    state=UserSG.main,
)

settings_window = Window(
    Const("<b>⚙️ Настройки Хелпера</b>"),
    Multi(
        Const("<b>Доступ к расширению:</b> "),
        Format("{access}" if "{access}" else "Неизвестно"),
    ),
    Row(
        SwitchTo(Const("ARM"), state=UserSG.arm_settings, id="arm_settings"),
        SwitchTo(
            Const("Genesys"), state=UserSG.genesys_settings, id="genesys_settings"
        ),
    ),
    Back(Const("🔙 Назад")),
    getter=settings_getter,
    state=UserSG.settings,
)


def create_arm_checkboxes():
    """Create checkboxes for ARM settings."""
    checkboxes = []
    for setting_key, setting_name in ARM_SETTINGS_OPTIONS:
        widget_id = f"arm_{setting_key}"
        checkboxes.append(
            Checkbox(
                Const(f"✅ {setting_name}"),
                Const(f"☑️ {setting_name}"),
                id=widget_id,
                on_click=on_arm_setting_click,
            )
        )
    return checkboxes


def create_genesys_checkboxes():
    """Create checkboxes for Genesys settings."""
    checkboxes = []
    for setting_key, setting_name in GENESYS_SETTINGS_OPTIONS:
        widget_id = f"genesys_{setting_key}"
        checkboxes.append(
            Checkbox(
                Const(f"✅ {setting_name}"),
                Const(f"☑️ {setting_name}"),
                id=widget_id,
                on_click=on_genesys_setting_click,
            )
        )
    return checkboxes


arm_settings = Window(
    Const("<b>Настройки ARM'а</b>"),
    Column(*create_arm_checkboxes()),
    SwitchTo(Const("🔙 Назад"), state=UserSG.settings, id="back"),
    getter=arm_settings_getter,
    state=UserSG.arm_settings,
)

genesys_settings = Window(
    Const("<b>Настройки Genesys'а</b>"),
    Column(*create_genesys_checkboxes()),
    SwitchTo(Const("🔙 Назад"), state=UserSG.settings, id="back"),
    getter=genesys_settings_getter,
    state=UserSG.genesys_settings,
)

user_dialog = Dialog(menu_window, settings_window, arm_settings, genesys_settings)
