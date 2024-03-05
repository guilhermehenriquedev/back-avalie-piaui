from django.db import connections
from core.utils import dictfetchall
from core.models import Respostas

class CaseRespostas():

    def list_all():

        try:

            with connections["default"].cursor() as cursor:

                sql = f""" 
                    select 	r.response_id,
                            r.cpf,
                            r.id_avaliacao,
                            p.titulo as titulo_pesquisa,
                            pgnt.texto_pergunta,
                            r.texto_resposta,
                            r.criado_em,
                            r.atualizado_em
                    from Respostas r 
                    inner join Pesquisas p on r.survey_id = p.survey_id 
                    inner join Perguntas pgnt on r.question_id = pgnt.id 
                    """
                cursor.execute(sql)
                data = dictfetchall(cursor)
                return data
                
        except Exception as err:
            print(err)

        finally:
            cursor.close()