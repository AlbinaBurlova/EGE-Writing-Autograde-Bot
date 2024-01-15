ASK_FOR_RECOMMENDATIONS = "Спасибо, что оценили работу бота! У вас будут пожелания по улучшению бота?"

LETTER_ONE = """
You have received an email message from your English-speaking pen-friend Mark:
From: Mark@mail.uk
To: Russian_friend@ege.ru
Subject: Household chores
…Can you imagine we’ve just come home from the supermarket and it turned out that we spent 5 hours there! I can’t believe it! We wasted so much time shopping for food. I just hate it when mum asks me to help her with that. What about you? How do you help your parents during the week? What is your least favourite household chore? Why don’t you like doing it?
By the way, father bought a new lawnmower last week…

Write an email to Mark.
In your message:
– answer his questions;
– ask 3 questions about his father’s lawn mower.

Write 100–140 words.
Remember the rules of email writing.
"""

LETTER_TWO = """
You have received an email message from your English-speaking pen-friend Nora.
From: NoraJ@uk.com
To: Russian_friend@mail.ru
Subject: Dreams
... My mom says I have too many dreams. What kind of dreams do you have? What personal qualities do you need to realise your wishes? Do you tell anyone about your dreams, why yes or no?
Last weekend my elder brother went hiking...
Write a email to Nora.
In your message:
− answer her questions;
− ask 3 questions about her elder brother.
Write 100-140 words.
Remember the rules of email writing.
"""

LETTER_THREE = """
You have received an email message from your English-speaking pen-friend Andy:
From: Andy@mail.uk
To: Russian_friend@ege.ru
Subject: Friends
...Last week I attended an interesting lecture on photography and met some interesting people there. I hope we’ll be friends. What about you? How do you make new friends? Have you ever become friends with someone via social media? Do think that online friends are not as good as real ones? By the way, I’ve bought a wedding present for my sister...
Write an email to Andy.
In your message:
– answer his questions;
– ask 3 questions about his sister’s wedding.
Write 100–140 words.
Remember the rules of email writing.
"""

RATE_BOT = "Оцените работу бота:"

THANKS = "Спасибо за вашу обратную связь!"

SECRET = """
Я знаю один секрет...

Ты справишься с экзаменом и поступишь туда, куда хочешь!
Твои родители будет гордиться тобой.

А знаешь почему?

Потому что ты лучше всех 🥰
"""

SKIP = "Пропустить"

START_MESSAGE = """
Продуктивное письмо - одно из самых сложных заданий экзамена, вместе мы успешно сможем подготовиться! Давай начнем!

Сейчас я могу предложить вам три разные темы письма на выбор, вам нужно выбрать тему, а затем отправить текст своего ответа в форме сообщения.

Жду с нетерпением вашего выбора 🤓

"""

COMMANDS: dict[str, str] = {
    '/start': 'Начать сначала',
    '/evaluate': 'Отправить письмо на проверку',
    '/get_stat': 'Посмотреть статистику',
    '/rate': 'Оценить работу бота',
    '/help': 'Показать описание команд'
}

HELP_MESSAGE = """
Вот основные мои функции:

/start: Начать сначала. Используйте эту команду, если хотите начать все сначала.
/evaluate: Отправить письмо на проверку. Пришлите мне свое электронное письмо, и я оценю его по критериям ЕГЭ.
/get_stat: Посмотреть статистику. Я предоставлю вам статистику по вашим ошибкам, чтобы вы могли видеть свой прогресс.
/rate: Оценить работу бота. Если вам нравится моя работа, не забудьте оценить меня!
/help: Показать описание команд. Если вы забыли, что делает та или иная команда, используйте эту команду, чтобы увидеть описание всех команд.

Не забывайте, что я здесь, чтобы помочь вам. А еще я знаю один секрет 😋
"""

SEND_TO_MENU = """
К сожалению, у меня нет такой функции - обратите внимание на меню: там описан весь мой функционал!
"""

WAITING_MESSAGE = "Подождите, идет оценивание текста... 😊"

ERROR = "Ой, что-то пошло не так.."

RESTART_MESSAGE = """
У вас три темы на выбор - выберите одну и напишите ответ в сообщении, а я его проверю. 😉
"""

WAIT_FOR_TOO_LONG = "Ой, простите, но сервер сейчас не отвечает."

RESTART_MESSAGE = """
У вас три темы на выбор - выберите одну и напишите ответ в сообщении, а я его проверю. 😉
"""
TRY_AGAIN = "Простите, но что-то пошло не так.. \nПопробуем сначала?"
