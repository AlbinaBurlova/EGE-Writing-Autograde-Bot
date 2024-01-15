import matplotlib.pyplot as plt

from aiogram import types, Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.filters import Command

# в будущем будет добавлена база данных
results = []

router = Router()


@router.message(Command("get_stat"))
async def show_stat(message: types.Message, bot: Bot):

    if not results:
        await message.answer("Для статистики пока не хватает данных.")
        return

    averages = calculate_averages(results)
    await message.answer(f"Средние результаты оценки: {averages}")

    plot_file = create_plot(averages)
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(plot_file))


@router.callback_query(F.data == "get_stat")
async def callback_show_stat(callback: CallbackQuery, bot: Bot):
    await show_stat(callback.message, bot)
    await callback.answer()


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

