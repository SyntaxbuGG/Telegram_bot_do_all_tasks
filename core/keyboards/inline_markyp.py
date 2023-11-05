from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.filters.callback_queries import *


def get_language():
    builder = InlineKeyboardBuilder()
    builder.button(text='🇺🇿 Özbekcha', callback_data=My_callbackdata(language_='uz'))
    builder.button(text='🏴󠁧󠁢󠁥󠁮󠁧󠁿 English', callback_data=My_callbackdata(language_='eng'))
    builder.button(text='🇷🇺 Русский', callback_data=My_callbackdata(language_='ru'), )
    builder.adjust(1, 1)
    return builder.as_markup()



