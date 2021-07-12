import logging
import json
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor


# Configure logging
logging.basicConfig(level=logging.DEBUG)


API_TOKEN = 'API'    # chave do bot


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
with open('nomesFemininos.json', 'r') as f:
    full = json.load(f)


# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    apresentacao = State()      # storage as 'Form:apresentacao'
    nome = State()              # storage as 'Form:nome'
    opcao = State()             # storage as 'Form:opcao'


@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm NomesFemininosBot!\nPowered by: \nDev. Laura Sorato. (Estagiário Developer) \nDev. Renan Almeida. (Estagiário Developer)\n")


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
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
            # entrada para a conversa
            # Set state
            await Form.apresentacao.set()
            await message.reply("Antes de começar, siga as regras para encontrar o nome:\n"
                                "1 - O nome não deve conter números;\n"
                                "2 - Escreva um nome aprovado pelo IBGE;\n"
                                "3 - O nome não deve conter caracteres especiais como pontos ou traços.\n")

            # Configure ReplyKeyboardMarkup
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add("Sim", "Não")
            await message.reply("Podemos começar?", reply_markup=markup)

        else:
            await message.answer("No momento você não possui permissão para acessar as informações internas.\n"
                "Entre em contato com os desenvolvedores.\n"
                "Para mais informações dos meu criadores digite '/info'")
    else:
        await message.answer('Olá ' + message['chat'][
            'first_name'] + ', no momento não encontrei seu username. Você deve verificá-lo nas configurações do Telegram.')


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    # permite cancelar a ação
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.apresentacao)
async def process_name(message: types.Message, state: FSMContext):
    # processa username
    async with state.proxy() as data:
        data['apresentacao'] = message.text.lower()

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        # interrompendo ação
        if data['apresentacao'] != "sim":
            await state.finish()
        else:
            await Form.next()
            await message.reply("Qual nome você gostaria de pesquisar?", reply_markup=markup)


# confere o nome
@dp.message_handler(lambda message: message.text.isdigit(), state=Form.nome)
async def process_nome_invalid(message: types.Message):
    return await message.reply("Você deve fornecer um nome.\n"
                               "Qual nome você gostaria de pesquisar?")


@dp.message_handler(lambda message: message.text, state=Form.nome)
async def process_nome(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(nome=(message.text.upper()))

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Nome e Variações", "Gênero")
    markup.add("Frequência Feminina", "Frequência Masculina")
    markup.add("Frequência Total", "Razão")

    await message.reply("Qual informação você gostaria de saber?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Nome e Variações", "Gênero", "Frequência Feminina", "Frequência Masculina", "Frequência Total", "Razão"], state=Form.opcao)
async def process_opcao_invalid(message: types.Message):
    return await message.reply("Escolha mal sucedida, por favor utilize o teclado.")


@dp.message_handler(state=Form.opcao)
async def process_opcao(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info'] = message.text
        segundos = message['date']
        with open('logs.log', 'a') as arquivo:
            arquivo.write(segundos.__str__())

        with open('user.txt') as file:
            userList = file.read()
        user = userList.split('\n')

        textomsg = ''
        if message["chat"]["username"]:
            textomsg += message["chat"]["username"]
            with open('logs.log', 'a') as arquivo:
                arquivo.write('\n' + message["chat"]["username"] + '\n\n')
        else:
            await message.answer("Você não possui um Username. Logo, deverá ir em suas configurações e nomea-lo.")

        # pesquisa nome no dicionário
        if textomsg in user:
            full
            txt = ''
            data['opcao'] = message.text
            for n in full:
                if data['nome'] in n['nome']:
                    if data['opcao'] == "Nome e Variações":
                        if n['nome']:
                            txt += f'<b>Nome e Variações:</b> <i>\n{n["nome"]}</i>\n'
                    if data['opcao'] == "Gênero":
                        if n['genero']:
                            txt += f'<b>\nGênero:</b> <i>\n{n["genero"]}</i>\n'
                    if data['opcao'] == "Frequência Feminina":
                        if n['freqFem']:
                            txt += f'<b>\nFrequência Feminina:</b> <i>\n{n["freqFem"]}</i>\n'
                    if data['opcao'] == "Frequência Masculina":
                        if n['freqMasc']:
                            txt += f'<b>\nFrequência Masculina:</b> <i>\n{n["freqMasc"]}</i>\n'
                    if data['opcao'] == "Frequência Total":
                        if n['freqTot']:
                            txt += f'<b>\nFrequência Total:</b> <i>\n{n["freqTot"]}</i>\n'
                    if data['opcao'] == "Razão":
                        if n['ratio']:
                            txt += f'<b>\nRazão:</b> <i>\n{n["ratio"]}</i>\n'

            if txt != "":
                await bot.send_message(message.chat.id, txt, parse_mode=ParseMode.HTML)

            elif message.text.isdigit() == False:
                await message.answer("Nome não encontrado.")

            # Remove keyboard
            markup = types.ReplyKeyboardRemove()
            await bot.send_message(message.chat.id,
                                   md.text(
                                       md.bold("Nome: "), md.italic(data['nome']),
                                       md.bold("Opção selecionada: "), md.italic(data['opcao']),
                                       sep='\n'), reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

        # And send message
        # await bot.send_message(message.chat.id, f"Nome: {data['nome']} \nOpção selecionada: {data['opcao']}")

    # Finish conversation
    await state.finish()


# echo para qualquer mensagem no início do bot
@dp.message_handler()
async def echo(message: types.Message):
    # adiciona botão start
    entradas = ['oi', 'olá', 'oie', 'roi', 'hey', 'eai', 'eae', 'salve', 'hello', 'ei', 'hi', 'oii', 'oiee']

    if message.text.lower() in entradas:
        await message.answer('Olá ' + message['chat'][
            'first_name'] + ', eu sou o Bot de consulta de nomes femininos, criado para encontrar as informações gerais do nome.\n')

    if message.text != '':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("/start")
        await message.reply("Podemos começar?", reply_markup=markup)


# final
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
