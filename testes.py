# https://pt.stackoverflow.com/questions/268693/separar-dados-de-um-arquivo-txt
# https://panda.ime.usp.br/pensepy/static/pensepy/10-Arquivos/files.html
# https://qastack.com.br/programming/620367/how-to-jump-to-a-particular-line-in-a-huge-text-file

""" USANDO O splitlines(",")
https://pt.stackoverflow.com/questions/226182/quebra-de-linha-em-um-arquivo-txt
name,classification,frequency_female,frequency_male,frequency_total,ratio,names

nomes = ''
with open('grupos.csv', 'rb') as f:
    nomes = f.read().decode()
full = []
femininos = []
txt = ''
nomesList = nomes.splitlines()
for linha in nomesList:
    if linha not in ['name,classification,frequency_female,frequency_male,frequency_total,ratio,names\r']:
        if linha.find(',M,') <= 0:
            if txt:
                full.append(txt)
                txt = ''
            txt += linha + '\n'
for x in full:
    if x.find(',F,'):
        nome = x.split('F')[0]
    femininos.append(dict(nome=nome))
    print(nome)
"""



"""BOT"""
import logging
import json

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1844881714:AAHUgvk1ZLPx7jIXb_1ktoTEpBS3VccvaE4'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
with open('alarmes.json', 'r') as f:
    alarmes = json.load(f)


@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm Alarmes828DBot!\nPowered by: \nDev. Laura Sorato. (Estagiário Developer) \nDev. Renan Almeida. (Estagiário Developer)\n")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
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
                'first_name'] + ', eu sou o Bot para o alarme 828D, criado para encontrar as informações do seu erro.\n'
                                'Você deve me fornecer um valor para pesquisa.')
        else:
            await message.answer("Olá, eu sou o Bot para o alarme 828D, criado para encontrar as informações do seu erro.\n"
                                 "No momento você não possui permissão para acessar as informações internas.\n"
                                 "Entre em contato com os desenvolvedores.\n"
                                 "Para mais informações dos meu criadores digite '/info'")
    else:
        await message.answer('Olá ' + message['chat'][
            'first_name'] + ', no momento não encontrei seu username. Você deve verifica-lo nas configurações do Telegram.')


@dp.message_handler()
async def echo(message: types.Message):

    segundos = message['date']
    with open('logs.log', 'a') as arquivo:
        arquivo.write(segundos.__str__())

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
        await message.answer("Você não possui um Username. Logo, deverá ir em suas configurações e nomea-lo.")

    if textomsg in user:
        entradas = ['oi', 'olá', 'ola', 'oie', 'roi', 'hey', 'eai', 'eae', 'salve', 'hello', 'ei', 'hi', 'oii', 'oiee']
        alarmes
        txt = ''
        for alarme in alarmes:
            if alarme['numero'] == message.text:
                if alarme['titulo']:
                    txt += f'TÍTULO: {alarme["titulo"]}\n'
                if alarme['definicoes']:
                    txt += f'\nDEFINIÇÕES:\n{alarme["definicoes"]}\n'
                if alarme['reacoes']:
                    txt += f'\nREAÇÕES:\n{alarme["reacoes"]}\n'
                if alarme['correcoes']:
                    txt += f'CORREÇÕES:\n{alarme["correcoes"]}\n'
                if alarme['programa']:
                    txt += f'CONTINUAÇÃO DO PROGRAMA:{alarme["programa"]}\n'
                if alarme['parametro']:
                    txt += f'PARÂMETRO:\n{alarme["parametro"]}\n'
                if alarme['valormsg']:
                    txt += f'VALOR DE MENSAGEM:\n{alarme["valormsg"]}\n'
                if alarme['objeto']:
                    txt += f'OBJETO:\n{alarme["objeto"]}\n'
                if alarme['reconhecimento']:
                    txt += f'RECONHECIMENTO:\n{alarme["reconhecimento"]}\n'
                if alarme['causa']:
                    txt += f'CAUSA:\n{alarme["causa"]}\n'
        if txt != '':
            await message.answer(txt)
        elif message.text.lower() in (entradas):
            await message.answer('Olá ' + message['chat']['first_name'] + ', eu sou o Bot para o alarme 828D, criado para encontrar as informações do seu erro.\n'
                                 'Você deve me fornecer um valor para pesquisa.')
        else:
            erro = "Você deve fornecer um valor válido."
            await message.answer(erro)
    else:
        await message.answer("Olá, eu sou o Bot para o alarme 828D, criado para encontrar as informações do seu erro.\n"
                             "No momento você não possui permissão para acessar as informações internas.\n"
                             "Entre em contato com os desenvolvedores.\n"
                             "Para mais informações dos meu criadores digite '/info'")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


# print([x for x in alarmes if x['numero'] == '2001'][0]['titulo'])
