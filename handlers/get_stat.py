import os
from typing import Union

import matplotlib.pyplot as plt
from aiogram import types, Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile

# в будущем будет добавлена база данных
results = []

router = Router()


async def show_stat(event: Union[types.Message, CallbackQuery], bot: Bot):
    if not results:
        await event.answer("Для статистики пока не хватает данных.")
        return

    averages = calculate_averages(results)
    await event.answer(f"Средние результаты оценки: {averages}")

    plot_file = create_plot(averages)
    await bot.send_photo(chat_id=event.from_user.id, photo=FSInputFile(plot_file))

    os.remove(plot_file)


router.message(Command("get_stat"))(show_stat)
router.callback_query(F.data == "get_stat")(show_stat)


def calculate_averages(result_list):
    averages = {}
    for key in result_list[0]:
        if key != 'comments':
            total = sum(result[key] for result in result_list if key in result)
            count = sum(1 for result in result_list if key in result)
            averages[key] = total / count if count > 0 else 0
    return averages


def create_plot(averages):
    keys = list(averages.keys())
    values = list(averages.values())

    plt.figure(figsize=(6, 4))
    plt.bar(keys, values, color='skyblue')
    plt.xlabel('Components of the English Exam')
    plt.ylabel('Average Scores')
    plt.title('Average Scores for Each Component of the English Exam')

    plot_file = 'plot.png'
    plt.savefig(plot_file)
    plt.close()

    return plot_file
