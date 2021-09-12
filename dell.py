import pandas as pd

def search_patient():
    choose_district = str(input('Digite o nome do Município para pesquisa: ')).upper()
    try:
        total_cases = df_gerint_poa.query('municipio_residencia in @choose_district')
        print(f'Total de casos do município {choose_district}, é {total_cases.municipio_residencia.count()}')
        print(f'A média de idade dos pacientes do município de {choose_district}, é {total_cases.idade.mean():.2f}.')
        avarage_age_genre = total_cases.groupby(by='sexo').size()
        print(f'A média de idade dos pacientes do município de {choose_district}, por {avarage_age_genre}')
    except ValueError:
        print('Município não encontrado')

def search_hospital():
    choose_hospital = str(input('Digite o nome do hospital para pesquisa: ')).upper()
    try:
        total_cases_hospital = df_gerint_poa.query('executante in @choose_hospital')
        total_cases_hospital = total_cases_hospital.loc[0:,
                                 ['executante', 'idade', 'municipio_residencia', 'solicitante', 'data_autorizacao',
                                  'data_internacao', 'data_alta']]
        print(f'{total_cases_hospital}')
    except IndexError:
        raise LookupError('Hospital não encontrado')

#HOSPITAL SAO LUCAS DA PUCRS
def calculate_time_hospitalization():
    choose_hospital = str(input('Digite o nome do Hospital para pesquisa: ')).upper()
    hospitalization_period = df_gerint_poa.query('executante in @choose_hospital')
    hospitalization_period['dias_internacao'] = hospitalization_period['data_alta'] - hospitalization_period['data_internacao']
    search_result = hospitalization_period.loc[0:, ['id_usuario', 'executante', 'solicitante', 'dias_internacao']]
    print(f'Abaixo o período de dias ques os pacientes estiveram internados:\n{search_result}')

def search_longer_waitlist_time():
    waitlist = df_gerint_poa.sort_values(by='horas_na_fila', ascending=False).head(5)
    print(f'Os cinco casos com maiores tempos de espera na fila foram:\n{waitlist}')

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
            search_patient()
        elif opt == 2:
            print('Em construção!')
        elif opt == 3:
            search_hospital()
        elif opt == 4:
            calculate_time_hospitalization()
        elif opt == 5:
            search_longer_waitlist_time()
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
