from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram import types

from states import Test


@dp.message_handler(text="Test")
async def enter_test(message: types.Message):
    await message.answer('Вы начали тестирование\n'
                         'Вопрос № 1')

    await Test.first()


@dp.message_handler(state=Test.q1)
async def answer_q1(messgae: types.Message, state: FSMContext):
    answer = messgae.text

    await state.update_data(
        {
            "answer1": answer,
            "id": messgae.from_user.id
        }
    )

    await messgae.answer("Вопрос №2")
    await Test.q2.set()


@dp.message_handler(state=Test.q2)
async def answer_q2(messgae: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = messgae.text

    await messgae.answer('Спасибо за ответы')
    await messgae.answer(answer1)
    await messgae.answer(answer2)

    await state.reset_state(with_data=False)