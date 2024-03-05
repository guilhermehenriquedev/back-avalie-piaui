from django.db import connections
from core.utils import dictfetchall
from datetime import datetime


class Opcoes():

    def create(texto_opcao=None, pergunta_id=None):

        try:
            with connections["default"].cursor() as cursor:
                print("texto opcao...: ", texto_opcao)
                sql = f""" INSERT INTO avalie.Opcoes
                                (texto_opcao, criado_em, pergunta_id)
                            VALUES('{texto_opcao}', now(), {pergunta_id}); """
                # Executar a inserção
                cursor.execute(sql)
                id_gerado = cursor.lastrowid

            return {"new_id": id_gerado}

        except Exception as e:
            print(f"Erro ao registrar ação: {str(e)}")

        finally:
            # Fechar o cursor e a conexão
            cursor.close()