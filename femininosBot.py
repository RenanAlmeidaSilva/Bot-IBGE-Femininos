import logging
import json

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = 'API'    # chave do bot


# Configure logging
logging.basicConfig(level=logging.DEBUG)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
with open('nomesFemininos.json', 'r') as f:
    full = json.load(f)


@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm NomesFemininosBot!\nPowered by: \nDev. Laura Sorato. (Estagiário Developer) \nDev. Renan Almeida. (Estagiário Developer)\n")


@dp.message_handler(commands=['start'])
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
async def echo(message: types.Message):
    # escreve arquivo de logs
    segundos = message['date']
    with open('logs.log', 'a') as arquivo:
        arquivo.write(segundos.__str__())

    # abre arquivo de usuários permitidos
    with open('user.txt') as file:
        userList = file.read()
    #print(userList)

    user = userList.split('\n')
    #print(user)

    textomsg = ''
    if message["chat"]["username"]:
        textomsg += message["chat"]["username"]
        with open('logs.log', 'a') as arquivo:
            arquivo.write('\n'+message["chat"]["username"]+'\n\n')
    else:
        await message.answer("Você não possui um Username. Logo, deverá ir em suas configurações e nomeá-lo.")

    # pesquisa nome no dicionário
    if textomsg in user:
        entradas = ['oi', 'olá', 'oie', 'roi', 'hey', 'eai', 'eae', 'salve', 'hello', 'ei', 'hi', 'oii', 'oiee']
        full
        txt = ''
        ex = message.text.upper()
        for n in full:
            if ex in n['nome']:
                txt += f'<b>Nome e Variações:</b> \n<i>{n["nome"]}</i>\n'
                if n['genero']:
                    txt += f'\n<b>Gênero:</b> \n<i>{n["genero"]}</i>\n'
                if n['freqFem']:
                    txt += f'\n<b>Frequência Fememinina:</b> <i>\n{n["freqFem"]}</i>\n'
                if n['freqMasc']:
                    txt += f'\n<b>Frequência Masculina:</b> <i>\n{n["freqMasc"]}</i>\n'
                if n['freqTot']:
                    txt += f'\n<b>Frequência Total:</b> <i>\n{n["freqTot"]}</i>\n'
                if n['ratio']:
                    txt += f'\n<b>Razão:</b> <i>\n{n["ratio"]}</i>\n'
        # print(txt)

        if txt != '':
            await message.answer(txt, parse_mode=types.ParseMode.HTML)
        elif message.text.lower() in (entradas):
            await message.answer('Olá ' + message['chat']['first_name'] + ', eu sou o Bot de consulta de nomes femininos, criado para encontrar as informações gerais do nome.\n'
                                 'Você deve me fornecer um nome para pesquisa.')
        elif message.text.isdigit():
            await message.answer("Por favor informe um <b>nome</b> para consulta.", parse_mode=types.ParseMode.HTML)
        else:
            erro = "Desculpe, não encontrei em meus dados. Por favor informe um <b>novo nome</b>."
            await message.answer(erro, parse_mode=types.ParseMode.HTML)
    else:
        await message.answer("Olá, eu sou o Bot de consulta de nomes femininos, criado para encontrar as informações gerais do nome.\n"
                             "No momento você não possui permissão para acessar as informações internas.\n"
                             "Entre em contato com os desenvolvedores.\n"
                             "Para mais informações dos meu criadores digite '/info'")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# print([x for x in alarmes if x['numero'] == '2001'][0]['titulo'])
