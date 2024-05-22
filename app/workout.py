from aiogram import types

user_variables = {}

last_msg_id = {}


async def add_new_user(message: types.Message):
    user_id = int(message.from_user.id)

    if user_id not in user_variables:
        user_variables[user_id] = {}
        last_msg_id[user_id] = None


async def save_user_exercise(message: types.Message, text: str) -> bool:
    user_id = int(message.from_user.id)

    try:
        exercise_data = text.split(" - ")
        if len(exercise_data) == 2:
            exercise = exercise_data[0].strip()
            weight_reps = exercise_data[1].strip()

            if exercise in user_variables[user_id]:
                user_variables[user_id][exercise].append(weight_reps)
            else:
                user_variables[user_id][exercise] = [weight_reps]
        return True

    except KeyError:
        await add_new_user(message)
        return False


async def get_user_exercises(message: types.Message) -> str:
    data = ""

    user_id = int(message.from_user.id)

    try:
        exercise_cnt = 0
        for exercise in user_variables[user_id]:
            sets_cnt = 0
            exercise_cnt += 1
            data += str(exercise_cnt) + ". " + exercise + ":\n"
            for sets in user_variables[user_id][exercise]:
                sets_cnt += 1
                data += "    " + str(sets_cnt) + ". " + sets + "\n"

        return data
    except KeyError:
        await add_new_user(message)
        return data


async def clear_user_exercises(message: types.Message):
    user_id = int(message.from_user.id)

    if user_id in user_variables:
        user_variables[user_id] = {}


async def change_last_msg_id(message: types.Message, msg_id):
    user_id = int(message.from_user.id)

    last_msg_id[user_id] = msg_id


async def get_last_msg_id(message: types.Message):
    user_id = int(message.from_user.id)

    return last_msg_id[user_id]


async def delete_last_msg_id(message: types.Message):
    user_id = int(message.from_user.id)

    last_msg_id[user_id] = None
