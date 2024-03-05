from django.db import connections
from core.utils import dictfetchall
from datetime import datetime

from core.usecases.opcoes import Opcoes

class Perguntas():

    def listall(id=None):

        try:
            with connections["defaul"].cursor() as cursor:

                sql = f""" select * from avalie.Perguntas """
                cursor.execute(sql)
                data = dictfetchall(cursor)

                return data
            
        except Exception as err:

            print("erro...: ", err)
        
        finally:
            cursor.close()

    def create(texto_pergunta=None, tipo_pergunta=None, survey_id=None, opcoes=None):

        try:

            with connections["default"].cursor() as cursor:

                sql = f"""  INSERT INTO avalie.Perguntas
                                (texto_pergunta, 
                                tipo_pergunta, 
                                criado_em, 
                                survey_id)
                            VALUES('{texto_pergunta}', 
                                    {tipo_pergunta}, 
                                    now(), 
                                    {survey_id}); """
                # Executar a inserção
                cursor.execute(sql)
                id_gerado = cursor.lastrowid

                # cria opcoes se tiver
                for opcao in opcoes:

                    if opcao:
                        print("criando opcao...: ", opcao)
                        Opcoes.create(texto_opcao=opcao, pergunta_id=id_gerado)

        except Exception as e:
            print(f"Erro ao registrar ação: {str(e)}")

        finally:
            # Fechar o cursor e a conexão
            cursor.close()

    def search_quiz_question(id_pergunta=None):

        """ Retorna as peguntas e opcoes da pesquisa """
        try:

            with connections["default"].cursor() as cursor:

                sql = f""" 
                        SELECT 	p.id, 
                                p.texto_pergunta, 
                                JSON_ARRAYAGG(JSON_OBJECT('option_id', op.option_id, 'texto', op.texto_opcao)) AS texto_opcao,
                                tp.id as id_tipo_pergunta,
                                tp.nome as nome_tipo_pergunta,
                                p.criado_em,
                                p.atualizado_em,
                                p.survey_id
                        FROM Perguntas p
                        LEFT JOIN Opcoes op ON p.id = op.pergunta_id
                        LEFT JOIN Tipo_pergunta tp ON tp.id = p.tipo_pergunta
                        WHERE p.survey_id = {id_pergunta}
                        GROUP BY p.id, p.texto_pergunta
                    """
                cursor.execute(sql)
                data = dictfetchall(cursor)
                return data
                
        except Exception as err:
            print(err)

        finally:
            cursor.close()