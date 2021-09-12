import pandas as pd

def buscar_pacientes():
    escolha_municipio = str(input('Digite o nome do Município para pesquisa: ')).upper()
    try:
        total_casos = df_gerint_poa.query('municipio_residencia in @escolha_municipio')
        print(f'Total de casos do município {escolha_municipio}, é {total_casos.municipio_residencia.count()}')
        print(f'A média de idade dos pacientes do município de {escolha_municipio}, é {total_casos.idade.mean():.2f}.')
        media_idade_genero = total_casos.groupby(by='sexo').size()
        print(f'A média de idade dos pacientes do município de {escolha_municipio}, por {media_idade_genero}')
    except ValueError:
        print('Município não encontrado')

def buscar_hospitais():
    escolha_hospital = str(input('Digite o nome do hospital para pesquisa: ')).upper()
    try:
        total_casos_executante = df_gerint_poa.query('executante in @escolha_hospital')
        total_casos_executante = total_casos_executante.loc[0:,
                                 ['executante', 'idade', 'municipio_residencia', 'solicitante', 'data_autorizacao',
                                  'data_internacao', 'data_alta']]
        print(f'{total_casos_executante}')
    except IndexError:
        raise LookupError('Hospital não encontrado')

def calcular_tempo_internacao():
    escolha_municipio = str(input('Digite o nome do Hospital para pesquisa: ')).upper()
    periodo_internacao = df_gerint_poa.query('executante in @escolha_municipio')
    res = periodo_internacao['data_alta'] - periodo_internacao['data_internacao']
    print(f'O período de dias que os pacientes do {escolha_municipio}, {periodo_internacao["executante"]} ficaram internados foi de: {res}')
    #print(res)

def buscar_maior_tempo_fila():
    res = df_gerint_poa.sort_values(by='horas_na_fila', ascending=False).head(5)
    print(f'{res}')

def menu():
    while True:
        print('Menu de opções.\n'
              '1 - Pesquisar pacientes por município.\n'
              '2 - Consultar intercações ano por município.\n'
              '3 - Consultar Hospitais.\n'
              '4 - Consultar tempo de internação\n'
              '5 - Consultar tempo de espera na fila\n'
              '6 - Finalizar programa.')

        opt = int(input('Selecione a opção desejada: '))
        if opt == 1:
            buscar_pacientes()
        elif opt == 3:
            buscar_hospitais()
        elif opt == 4:
            calcular_tempo_internacao()
        elif opt == 5:
            buscar_maior_tempo_fila()
        elif opt == 6:
            print('Encerrando. . .')
            break
        else:
            print('Opção inválida, escolha a opção novamente.\n')


if __name__ == '__main__':
    df_gerint_poa = pd.read_csv("gerint_solicitacoes_mod.csv", sep=';')
    df_gerint_poa['data_internacao'] = pd.to_datetime(df_gerint_poa['data_internacao'])
    df_gerint_poa['data_autorizacao'] = pd.to_datetime(df_gerint_poa['data_autorizacao'])
    df_gerint_poa['data_alta'] = pd.to_datetime(df_gerint_poa['data_alta'])

    menu()
