from aiogram.filters.callback_data import CallbackData

class My_callbackdata(CallbackData,prefix='lang'):
    language_:str

