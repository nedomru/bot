from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCheckbox


async def on_arm_setting_click(
    _event: CallbackQuery, widget: ManagedCheckbox, dialog_manager: DialogManager
):
    """
    Handler for ARM setting checkbox toggle.
    Setting path is extracted from widget ID (e.g., "arm_foldSpas" -> "arm.foldSpas").
    """
    user = dialog_manager.middleware_data.get("user")
    if not user:
        await _event.answer("Ошибка: пользователь не найден")
        return

    repo = dialog_manager.middleware_data.get("repo")
    if not repo:
        await _event.answer("Ошибка: база данных недоступна")
        return

    # Parse setting path from widget ID: "arm_foldSpas" -> "arm.foldSpas"
    setting_path = widget.widget_id.replace("_", ".")

    # Toggle the setting (use opposite of current state)
    new_value = not widget.is_checked()

    try:
        await repo.users.update_setting_path(user.user_id, setting_path, new_value)
        await _event.answer(f"Настройка обновлена: {new_value}")
    except Exception as e:
        await _event.answer(f"Ошибка: {str(e)}")


async def on_genesys_setting_click(
    _event: CallbackQuery, widget: ManagedCheckbox, dialog_manager: DialogManager
):
    """
    Handler for Genesys setting checkbox toggle.
    Setting path is extracted from widget ID (e.g., "genesys_allowPaste" -> "genesys.allowPaste").
    """
    user = dialog_manager.middleware_data.get("user")
    if not user:
        await _event.answer("Ошибка: пользователь не найден")
        return

    repo = dialog_manager.middleware_data.get("repo")
    if not repo:
        await _event.answer("Ошибка: база данных недоступна")
        return

    # Parse setting path from widget ID: "genesys_allowPaste" -> "genesys.allowPaste"
    setting_path = widget.widget_id.replace("_", ".")

    # Toggle the setting (use opposite of current state)
    new_value = not widget.is_checked()

    try:
        await repo.users.update_setting_path(user.user_id, setting_path, new_value)
        await _event.answer(f"Настройка обновлена: {new_value}")
    except Exception as e:
        await _event.answer(f"Ошибка: {str(e)}")
