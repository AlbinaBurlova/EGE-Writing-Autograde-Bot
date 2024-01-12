from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


BUTTONS_NAMES: dict[str, str] = {
    'btn_1': 'Письмо 1',
    'btn_2': 'Письмо 2',
    'btn_3': 'Письмо 3',
    'btn_4': 'Статистика',
    'btn_5': 'Оценить бота',
    'btn_6': 'Получить комментарии',
    'btn_7': 'Посмотреть на текст моей работы',
    'btn_8': 'Попробовать еще раз',
    'btn_9': 'Посмотреть статистику'
}

BUTTONS: dict[str, str] = {
    'btn_1': 'email_1',
    'btn_2': 'email_2',
    'btn_3': 'email_3',
    'btn_4': 'get_stat',
    'btn_5': 'rate',
    'btn_6': 'get_comments',
    'btn_7': 'view_my_work',
    'btn_8': 'restart',
    'btn_9': 'get_stat',
}


def create_inline_kb(width: int,
                     *args: str) -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=BUTTONS_NAMES[button],
                callback_data=BUTTONS[button]))

    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()
