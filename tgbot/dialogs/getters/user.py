from aiogram_dialog import DialogManager

from infrastructure.database.models import User


# Settings options for checkboxes
ARM_SETTINGS_OPTIONS = [
    ("foldSpas", "Сворачивать СПАС"),
    ("foldTabInfo", "Сворачивать вкладку Инфо"),
    ("foldTabAppeals", "Сворачивать вкладку Обращения"),
    ("foldTabCRequests", "Сворачивать вкладку Заявки КЦ"),
    ("foldTabSRequests", "Сворачивать вкладку Заявки СК"),
    ("foldTabApplications", "Сворачивать вкладку Заявки"),
    ("removeAppealsColumns", "Скрывать колонки Обращений"),
    ("removeDiagnosticTabs", "Скрывать диагностические вкладки"),
]

GENESYS_SETTINGS_OPTIONS = [
    ("allowPaste", "Разрешить вставку"),
    ("hideButtons", "Скрывать кнопки"),
    ("showLineStatus", "Показывать статус линии"),
    ("customChatColors", "Цветные чаты"),
    ("customChatSounds", "Звуки чатов"),
    ("showDutyMessages", "Сообщения дежурства"),
    ("allowChatSizeEdit", "Размер чата редактируем"),
    ("autoCollapseChatHeader", "Сворачивать заголовок чата"),
]


async def settings_getter(user: User, dialog_manager: DialogManager, **_kwargs):
    """Main settings getter - shows access level."""
    return {"access": user.access}


async def arm_settings_getter(user: User, dialog_manager: DialogManager, **_kwargs):
    """Getter for ARM settings window - returns checkbox states."""
    settings = user.settings or {}
    arm_settings = settings.get("arm", {})

    # Return individual checkbox states
    data = {}
    for setting_key, _ in ARM_SETTINGS_OPTIONS:
        data[f"arm_{setting_key}"] = arm_settings.get(setting_key, False)

    return data


async def genesys_settings_getter(user: User, dialog_manager: DialogManager, **_kwargs):
    """Getter for Genesys settings window - returns checkbox states."""
    settings = user.settings or {}
    genesys_settings = settings.get("genesys", {})

    # Return individual checkbox states
    data = {}
    for setting_key, _ in GENESYS_SETTINGS_OPTIONS:
        data[f"genesys_{setting_key}"] = genesys_settings.get(setting_key, False)

    return data
