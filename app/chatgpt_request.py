import os
import g4f
from g4f.Provider import Bing
from dotenv import load_dotenv

from data.exercises import exercises


load_dotenv()

system_msg = ("You are a training assistant AI designed to help users with their workout routines. Your main task is "
              "to recognize the exercises users have performed based on their descriptions and provide feedback in "
              "the format 'Exercise Name - Weight * Number of Repetitions'.")

test_msg = ("Отвечай одним предложением в формате 'Название упражнения - вес * кол-во повторений'."
            "Например: 'Жим лежа на скамье - 100кг * 4 повторения' или "
            "'Подтягивания на перекладине обратным хватом - 20 повторений'."
            "\nЕсли не указан вес, то укажи только кол-во повторений. Если не указаны повторения, то укажи 1 повторение"
            "\nЕсли в указанном ниже тексте не указано упражнение или не указан вес И повторения, то отправь сообщение "
            "'Ошибка'. Выбирай самое похожее упражнение из списка."
            "Вот список всех возможных упражнений: " + ", ".join(exercises) +
            "\n\nВот текст: ")


async def get_response(text: str) -> str:
    response = str(await g4f.ChatCompletion.create_async(
        model="gpt-4-turbo",
        provider=Bing,
        messages=[{"role": "system", "content": system_msg},
                  {"role": "user", "content": test_msg + "Текст: " + text}],
        proxy=os.getenv("PROXY")
    ))

    response = response.replace('**', '').replace('..', '')

    return response
