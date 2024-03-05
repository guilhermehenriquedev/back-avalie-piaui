from datetime import datetime
from django.db import connections


def registrar_acao(table=None, id_user=None, response_status=None, response_data=None, action=None, local_code=None, ip_user=None):
    ''' Função para registrar uma ação na tabela de auditoria '''

    try:

        with connections["default"].cursor() as cursor:

            # Preparar os valores para inserção na tabela de auditoria
            data_hora = datetime.now()
            sql = f"""INSERT INTO {table} (id_user, 
                                            data, 
                                            response_status, 
                                            response_data, 
                                            action, 
                                            local_code, 
                                            ip_user) VALUES ({id_user}, 
                                                            '{data_hora}', 
                                                            '{response_status}', 
                                                            '{response_data}', 
                                                            '{action}', 
                                                            '{local_code}', 
                                                            '{ip_user}')"""
            # Executar a inserção
            cursor.execute(sql)

        print("Ação registrada com sucesso!")

    except Exception as e:
        print(f"Erro ao registrar ação: {str(e)}")

    finally:
        # Fechar o cursor e a conexão
        cursor.close()
