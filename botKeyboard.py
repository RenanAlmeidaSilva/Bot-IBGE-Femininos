"""
This bot is created for the demonstration of a usage of regular keyboards.
"""
import json
import logging

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '1808365262:AAEqk_xCHTQsfbOuf_JO4GbLR3R_gY4DplE'    # chave do bot

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

with open('nomesFemininos.json', 'r') as f:
    full = json.load(f)


@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm NomesFemininosBot!\nPowered by: \nDev. Laura Sorato. (Estagiário Developer) \nDev. Renan Almeida. (Estagiário Developer)\n")


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup()

    # adds buttons. New rows are formed according to row_width parameter
    keyboard_markup.add("Nome e Variações", "Gênero")
    keyboard_markup.add("Frequência Fememinina", "Frequência Masculina")
    keyboard_markup.add("Frequência Total", "Razão")

    await message.reply("Olá, o que você gostaria de saber sobre este nome?", reply_markup=keyboard_markup)

async def send_welcome(message: types.Message):
    # abre arquivo de usuários permitidos
    with open('user.txt') as file:
        userList = file.read()
    user = userList.split('\n')

    textomsg1 = ''
    if message['chat']['username']:
        textomsg1 += message["chat"]["username"]
        with open('logs.log', 'a') as arquivo:
            arquivo.write('\n' + message["chat"]["username"] + '\n\n')
        if textomsg1 in user:
            await message.answer('Olá ' + message['chat'][
                'first_name'] + ', eu sou o Bot de consulta de nomes femininos, criado para encontrar as informações gerais do nome.\n'
                                'Você deve me fornecer um nome para pesquisa.')
        else:
            await message.answer("Olá, eu sou o Bot de consulta de nomes femininos, criado para encontrar as informações gerais do nome.\n"
                                 "No momento você não possui permissão para acessar as informações internas.\n"
                                 "Entre em contato com os desenvolvedores.\n"
                                 "Para mais informações dos meu criadores digite '/info'")
    else:
        await message.answer('Olá ' + message['chat'][
            'first_name'] + ', no momento não encontrei seu username. Você deve verificá-lo nas configurações do Telegram.')


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    # escreve arquivo de logs
    segundos = message['date']
    with open('logs.log', 'a') as arquivo:
        arquivo.write(segundos.__str__())

    # abre arquivo de usuários permitidos
    with open('user.txt') as file:
        userList = file.read()
    # print(userList)

    user = userList.split('\n')
    # print(user)

    textomsg = ''
    if message["chat"]["username"]:
        textomsg += message["chat"]["username"]
        with open('logs.log', 'a') as arquivo:
            arquivo.write('\n' + message["chat"]["username"] + '\n\n')
    else:
        await message.answer("Você não possui um Username. Logo, deverá ir em suas configurações e nomeá-lo.")

    # pesquisa nome no dicionário
    if textomsg in user:
        entradas = ['oi', 'olá', 'oie', 'roi', 'hey', 'eai', 'eae', 'salve', 'hello', 'ei', 'hi', 'oii', 'oiee']
        full
        txtN, txtG, txtF, txtM, txtT, txtR = ''
        ex = message.text.upper()
        for n in full:
            if ex in n['nome']:
                txtN += f'<b>Nome e Variações:</b> \n<i>{n["nome"]}</i>\n'
                if n['genero']:
                    txtG += f'\n<b>Genero:</b> \n<i>{n["genero"]}</i>\n'
                if n['freqFem']:
                    txtF += f'\n<b>Frequência Fememinina:</b> <i>\n{n["freqFem"]}</i>\n'
                if n['freqMasc']:
                    txtM += f'\n<b>Frequência Masculina:</b> <i>\n{n["freqMasc"]}</i>\n'
                if n['freqTot']:
                    txtT += f'\n<b>Frequência Total:</b> <i>\n{n["freqTot"]}</i>\n'
                if n['ratio']:
                    txtR += f'\n<b>Razão:</b> <i>\n{n["ratio"]}</i>\n'
        # print(txt)

# async def all_msg_handler(message: types.Message):
    button_text = message.text
    logger.debug('The answer is %r', button_text)  # print the text we've got

    if button_text == 'Nome e Variações':
        reply_text = txtN
    elif button_text == 'Gênero':
        reply_text = txtG
    elif button_text == 'Frequência Fememinina':
        reply_text = txtF
    elif button_text == 'Frequência Masculina':
        reply_text = txtM
    elif button_text == 'Frequência Total':
        reply_text = txtT
    else:
        reply_text = txtR

    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())
    # with message, we send types.ReplyKeyboardRemove() to hide the keyboard


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
