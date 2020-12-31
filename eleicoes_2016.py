import matplotlib.pyplot as plt
from random import randint


def pegar_dicionario_partidos():
    caminho_arquivo = 'partidos.csv'
    with open(caminho_arquivo) as arq:
        dados = list(map(lambda string: string.strip('\n').split(','), arq.readlines()[1:]))
    return {
        dado[0]: dado[1]
        for dado in dados
    }


def pega_dados(cidade_usuario):
    caminho_arquivo = 'eleicoes-municipais-2016.csv'
    with open(caminho_arquivo) as arq:
        dados = list(map(lambda string: string.strip('\n').split(','), arq.readlines()[1:]))
    dados_cidade_usuario = list(filter(lambda lista: lista[1] == cidade_usuario, dados))
    return [{
        'numero_turno': int(dado[0]),
        'nome_municipio': dado[1],
        'sigla_partido': dado[2],
        'descricao_cargo': dado[3],
        'nome': dado[4],
        'total_votos': int(dado[5])} for dado in dados_cidade_usuario]


def separar_dados(data):
    vereadores = [dado for dado in data if dado['descricao_cargo'] == 'VEREADOR']
    prefeitos = [dado for dado in data if dado['descricao_cargo'] == 'PREFEITO']
    return vereadores, prefeitos


def soma_votos_prefeito(nome, resultados_urna):
    soma = 0
    for resultado in resultados_urna:
        if nome == resultado['nome']:
            soma += resultado['total_votos']
    return soma


def obter_dicionario_prefeitos(urnas_prefeitos):
    dados_prefeitos = list(set([(urna['nome'], urna['sigla_partido']) for urna in urnas_prefeitos]))
    dicionario_prefeitos = {dados_prefeito: 0 for dados_prefeito in dados_prefeitos}
    for key in dicionario_prefeitos.keys():
        dicionario_prefeitos[key] = soma_votos_prefeito(key[0], urnas_prefeitos)
    return dicionario_prefeitos


def mostrar_cabecalho_resultado(tipo, tipo_urna):
    title = f'Resultados das eleições de {tipo} para a cidade de {tipo_urna[0]["nome_municipio"]}'.upper()
    qtde_tracos = int(2 * len(title))
    print('=' * qtde_tracos)
    print(title.center(qtde_tracos))
    print('=' * qtde_tracos)
    return qtde_tracos


def tabela_resultado_eleicoes(dicionario_partidos, tupla_prefeitos, urnas_prefeitos):
    qtde_tracos = mostrar_cabecalho_resultado('prefeito', urnas_prefeitos)
    tamanho_caracter_maior_partido = max([len(dicionario_partidos[candidato[2]]) for candidato in tupla_prefeitos])
    tamanho_caracter_maior_candidato = max([len(candidato[1]) for candidato in tupla_prefeitos])
    title_table = (
        'COLOCAÇÃO'.center(len('COLOCAÇÃO') + 10),
        'PARTIDO'.center(tamanho_caracter_maior_partido),
        'CANDIDATO'.center(tamanho_caracter_maior_candidato),
        'TOTAL DE VOTOS'.center(len('TOTAL DE VOTOS') + 15)
    )
    print(f'{title_table[0]} | {title_table[1]} | {title_table[2]} | {title_table[3]}'.center(qtde_tracos))
    print('-' * qtde_tracos)
    cont = 1
    for candidato in tupla_prefeitos:
        print(f'{(str(cont) + "°").center(len(title_table[0]))} | '
              f'{dicionario_partidos[candidato[2]].title().center(len(title_table[1]))} | '
              f'{candidato[1].title().center(len(title_table[2]))} | '
              f'{str(candidato[0]).center(len(title_table[3]))}'.center(qtde_tracos))
        cont += 1


def gera_lista_randomica_cores(qtde_cores):
    canal_cores = [(c + 2) / 10 for c in range(9)]
    a, b = 0, 8
    return [tuple(canal_cores[randint(a, b)] for _ in range(4)) for _ in range(qtde_cores)]


def grafico_resultado_eleicoes(eixo_x, numero_votos, xlabel, ylabel, title):
    lista_cores = gera_lista_randomica_cores(len(eixo_x))
    plt.bar(eixo_x, numero_votos, color=lista_cores)
    plt.xticks(eixo_x)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def resultados_eleicoes_prefeito(urnas_prefeitos, dicionario_partidos):
    dicionario_prefeitos = obter_dicionario_prefeitos(urnas_prefeitos)
    tupla_prefeitos = tuple(
        sorted(((value, key[0], key[1]) for key, value in dicionario_prefeitos.items()), reverse=True))
    eixo_x = [f'{tupla[1]} | {tupla[2]}' for tupla in tupla_prefeitos]
    numero_votos = [tupla[0] for tupla in tupla_prefeitos]
    tabela_resultado_eleicoes(dicionario_partidos, tupla_prefeitos, urnas_prefeitos)
    grafico_resultado_eleicoes(eixo_x, numero_votos, xlabel="Candidato | Partido", ylabel="Quantidade de votos",
                               title='Resultado das eleições de prefeito')


def soma_votos_geral(dicionarios_vereadores):
    return sum(dicionario['total_votos'] for dicionario in dicionarios_vereadores)


def calculo_partidos(urnas_vereadores, quociente_eleitoral_geral, dicionario_partidos):
    partidos_consultados = set(dicionario_partidos[urna['sigla_partido']] for urna in urnas_vereadores)
    dicionario_partidos_consultados = {
        partido: {
            'total_votos': 0,
        } for partido in partidos_consultados
    }
    for urna in urnas_vereadores:
        dicionario_partidos_consultados[dicionario_partidos[urna['sigla_partido']]]['total_votos'] += urna[
            'total_votos']
    for key_partido in dicionario_partidos_consultados.keys():
        dicionario_partidos_consultados[key_partido]['quociente_partidario'] = \
            dicionario_partidos_consultados[key_partido]['total_votos'] // quociente_eleitoral_geral
        dicionario_partidos_consultados[key_partido]['media'] = dicionario_partidos_consultados[key_partido][
                                                                    'total_votos'] // (dicionario_partidos_consultados[
                                                                                           key_partido][
                                                                                           'quociente_partidario'] + 1)
    return dicionario_partidos_consultados


def construir_lista_dict_partidos(dicionario_partidos_consultados):
    return list(sorted([(value['quociente_partidario'], value['media'], value['total_votos'], key) for key, value in
                        dicionario_partidos_consultados.items()], reverse=True))


def listar_quociente_partidario(lista_dados_partidos_consultados, qtde_tracos):
    tamanho_caracter_maior_partido = max([len(tupla[3]) for tupla in lista_dados_partidos_consultados])
    title_table = (
        'COLOCAÇÃO'.center(len('COLOCAÇÃO') + 10),
        'PARTIDO'.center(tamanho_caracter_maior_partido),
        'QUOCIENTE PARTIDÁRIO'.center(len('QUOCIENTE PARTIDÁRIO')),
        'TOTAL DE VOTOS'.center(len('TOTAL DE VOTOS')),
    )
    print('RESULTADO DA DISTRIBUIÇÃO DE VAGAS PELO QUOCIENTE PARTIDÁRIO'.center(qtde_tracos))
    print('-' * qtde_tracos)
    print(f'{title_table[0]} | {title_table[1]} | {title_table[2]} | {title_table[3]} |')
    cont = 1
    for tupla in lista_dados_partidos_consultados:
        print(f'{(str(cont) + "°").center(len(title_table[0]))} | '
              f'{str(tupla[3]).center(tamanho_caracter_maior_partido)} | '
              f'{str(tupla[0]).center(len(title_table[2]))} | '
              f'{str(tupla[2]).center(len(title_table[3]))} |')
        cont += 1
    print('=' * qtde_tracos)


def tabelar_vereadores_eleitos(ranking_candidatos, qtde_tracos):
    print('RANKING DE VEREADORES ELEITOS'.center(qtde_tracos))
    print('-' * qtde_tracos)
    tamanho_caracter_maior_partido = max([len(tupla[1]) for tupla in ranking_candidatos])
    tamanho_caracter_maior_nome = max([len(tupla[2]) for tupla in ranking_candidatos])
    title_table = (
        'COLOCAÇÃO'.center(len('COLOCAÇÃO') + 10),
        'NOME DO CANDIDATO'.center(tamanho_caracter_maior_nome),
        'PARTIDO'.center(tamanho_caracter_maior_partido),
        'TOTAL DE VOTOS DO CANDIDATO'.center(len('TOTAL DE VOTOS DO CANDIDATO')),
    )
    print(f'{title_table[0]} | {title_table[1]} | {title_table[2]} | {title_table[3]} |')
    cont = 1
    for vereador in ranking_candidatos:
        print(f'{(str(cont) + "°").center(len(title_table[0]))} | '
              f'{vereador[2].center(len(title_table[1]))} | '
              f'{vereador[1].center(len(title_table[2]))} | '
              f'{str(vereador[0]).center(len(title_table[3]))} |')
        cont += 1


def calculo_pessoas(dicionario_vereadores, dicionario_partidos):
    dict = {
        (urna['nome'], dicionario_partidos[urna['sigla_partido']]): 0
        for urna in dicionario_vereadores
    }
    for key in dict:
        for urna in dicionario_vereadores:
            if key[0] == urna['nome'] and key[1] == dicionario_partidos[urna['sigla_partido']]:
                dict[key] += urna['total_votos']
    return dict


def construir_lista_dict_pessoas(dicionario_pessoas_consultadas):
    return list(
        sorted([(value, key[1], key[0]) for key, value in dicionario_pessoas_consultadas.items()], reverse=True))


def obter_resultados_finais_de_vereadores(lista_dados_pessoas_consultadas, lista_dados_partidos_consultados,
                                          total_vagas):
    ranking_candidatos = []
    dicionario_eleitos_partidos = {tupla[-1]: 0 for tupla in lista_dados_partidos_consultados}
    for tupla_resultado_quociente_partidario in lista_dados_partidos_consultados:
        if total_vagas == 0:
            break
        qtde_passaram = tupla_resultado_quociente_partidario[0]
        while qtde_passaram > 0:
            adicionou_ranking = False
            for candidato in lista_dados_pessoas_consultadas:
                if candidato[1] == tupla_resultado_quociente_partidario[-1]:
                    removido = lista_dados_pessoas_consultadas.pop(lista_dados_pessoas_consultadas.index(candidato))
                    dicionario_eleitos_partidos[removido[1]] += 1
                    ranking_candidatos.append(removido)
                    adicionou_ranking = True
                    total_vagas -= 1
                    qtde_passaram -= 1
                    if total_vagas == 0 or qtde_passaram == 0:
                        break
            if not adicionou_ranking:
                break
    lista_medias_partidos = list(
        sorted([(tupla[1], tupla[-1]) for tupla in lista_dados_partidos_consultados], reverse=True))
    while total_vagas > 0:
        for media_partido in lista_medias_partidos:
            for dados_pessoa in lista_dados_pessoas_consultadas:
                if dados_pessoa[1] == media_partido[1]:
                    removido = lista_dados_pessoas_consultadas.pop(lista_dados_pessoas_consultadas.index(dados_pessoa))
                    dicionario_eleitos_partidos[removido[1]] += 1
                    ranking_candidatos.append(removido)
                    total_vagas -= 1
                    break
            if total_vagas == 0:
                break
        if len(lista_dados_pessoas_consultadas) == 0:
            break
    return ranking_candidatos, dicionario_eleitos_partidos


def montar_grafico_partidos_ranking(dicionario_partidos_ranking, dicionario_partidos):
    reverse_dict = {value: key for key, value in dicionario_partidos.items()}
    eixo_x = [reverse_dict[key] for key in dicionario_partidos_ranking.keys() if dicionario_partidos_ranking[key] > 0]
    eixo_y = [value for value in dicionario_partidos_ranking.values() if value > 0]
    grafico_resultado_eleicoes(eixo_x, eixo_y, xlabel='Partido', ylabel='Quantidade de vagas ocupadas',
                               title='Quantidade de vagas ocupadas por partido')


def listar_vereadores_eleitos(lista_dados_pessoas_consultadas, lista_dados_partidos_consultados, total_vagas,
                              qtde_tracos, dicionario_partidos):
    ranking_candidatos, dicionario_partidos_ranking = obter_resultados_finais_de_vereadores(
        lista_dados_pessoas_consultadas, lista_dados_partidos_consultados, total_vagas)
    tabelar_vereadores_eleitos(ranking_candidatos, qtde_tracos)
    montar_grafico_partidos_ranking(dicionario_partidos_ranking, dicionario_partidos)


def resultados_eleicoes_vereador(dicionario_vereadores, dicionario_partidos, total_vagas):
    qtde_tracos = mostrar_cabecalho_resultado('vereadores', dicionario_vereadores)
    quociente_eleitoral_geral = soma_votos_geral(dicionario_vereadores) // total_vagas
    print(f'Quociente eleitoral geral: {quociente_eleitoral_geral}')
    print('-' * qtde_tracos)
    dicionario_partidos_consultados = calculo_partidos(dicionario_vereadores, quociente_eleitoral_geral,
                                                       dicionario_partidos)
    dicionario_pessoas_consultadas = calculo_pessoas(dicionario_vereadores, dicionario_partidos)
    lista_dados_partidos_consultados = construir_lista_dict_partidos(dicionario_partidos_consultados)
    lista_dados_pessoas_consultadas = construir_lista_dict_pessoas(dicionario_pessoas_consultadas)
    listar_quociente_partidario(lista_dados_partidos_consultados, qtde_tracos)
    listar_vereadores_eleitos(lista_dados_pessoas_consultadas, lista_dados_partidos_consultados, total_vagas,
                              qtde_tracos, dicionario_partidos)


def main():
    # cidade = input('Informe a cidade desejada: ').strip().upper()
    # total_vagas = int(input(f'Informe a quantidade de vagas de {cidade}: ').strip())
    cidade = 'PORTO ALEGRE'
    total_vagas = 36
    data = pega_dados(cidade)
    vereadores, prefeitos = separar_dados(data)
    dicionario_partidos = pegar_dicionario_partidos()
    resultados_eleicoes_prefeito(prefeitos, dicionario_partidos)
    resultados_eleicoes_vereador(vereadores, dicionario_partidos, total_vagas)


main()
