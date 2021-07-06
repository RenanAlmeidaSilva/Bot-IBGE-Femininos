import json

# abre o arquivo grupos.csv
nomes = ''
with open('grupos.csv', 'rb') as f:
    nomes = f.read().decode()


# divide nomes do grupos.csv em um dicionário com todos os nomes
full = []
femininos = []
nomesList = nomes.split('\n')

for linha in nomesList:
    # remove primeira linha do grupo.csv
    if linha not in ['name,classification,frequency_female,frequency_male,frequency_total,ratio,names\r']:

            # divide os nomes por linha e "splita" os dados dos nomes
            # name, classification, frequency_female, frequency_male, frequency_total, ratio, names
            if len(linha) > 0:
                ll = linha.split(',')
                if ll[1] != 'M':    # pula nomes masculinos
                    dicionario = dict(
                        nome=ll[0] and ll[6].split('|')[1:-1],
                        genero=ll[1],
                        freqFem=ll[2],
                        freqMasc=ll[3],
                        freqTot=ll[4],
                        ratio=ll[5],
                        # variacoes=ll[6].split("\r")[0].split('|')
                    )

                    full.append(dicionario)


"""
# acessando valor específico no dicionário
# print([x for x in nomesList if x['nome'] == 'ALINE'][0]['ratio']) # TypeError: string indices must be integers
# print(dicionario.get('nome')[0])

txt = ''
ex = "LAURA"    # nome aleatório para retorno de dados
for n in full:
    if ex in n['nome']:
        txt += f'nome: {n["nome"]}'
        if n['genero']:
            txt += f'\ngenero: {n["genero"]}'
        if n['freqFem']:
            txt += f'\nfreqFem: {n["freqFem"]}\n'
        if n['freqMasc']:
            txt += f'freqMasc: {n["freqMasc"]}\n'
        if n['freqTot']:
            txt += f'freqTot: {n["freqTot"]}\n'
        if n['ratio']:
            txt += f'ratio: {n["ratio"]}\n'
print(txt)
"""

"""
# cria arquivo nomesFemininos - Dev. Laura.json de lista dos nomes femininos
full = json.dumps(full, sort_keys=True, indent=4, ensure_ascii=True)
with open('nomesFemininos - Dev. Laura.json', 'w') as file:
    file.write(full)
"""
