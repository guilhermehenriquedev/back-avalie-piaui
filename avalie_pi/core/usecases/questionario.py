from django.db import connections
from core.utils import dictfetchall

from core.usecases.pesquisas import Pesquisas
from core.usecases.perguntas import Perguntas
from core.usecases.opcoes import Opcoes


class Questionario():

    def create(title=None, description=None, orgao=None, tipo_servico=None, dict_perguntas=None, user_id=None):
        
        try:
            print(f"orgao {orgao} titulo {title} descricao {description} user_id {user_id} tiposervico {tipo_servico}")
            create_pesquisa = Pesquisas.create(orgao_id=orgao,
                                            titulo=title,
                                            descricao=description,
                                            user_id=user_id,
                                            tipo_servico=tipo_servico
                                            )
            print("criado na tabela de PESQUISA --- novo ID...: ", create_pesquisa["new_id"])
            for pergunta in dict_perguntas:
                print("CRIANDO NA TABELA DE PERGUNTA..:", pergunta)
                create_pergunta = Perguntas.create(
                    texto_pergunta=pergunta["texto_pergunta"],
                    tipo_pergunta=pergunta["tipo_pergunta"],
                    opcoes=pergunta["opcoes"],
                    survey_id=create_pesquisa["new_id"]
                )
            
        except Exception as err:
            print("erro", err)

    def get_questionarie(survey_id=None):

        try:
            
            questionario = Pesquisas()

            data = questionario.get_the_search(survey_id=survey_id)

            return data if data else []
        
        except Exception as err:
            print(err)

    def get_all(self):

        try:

            with connections["default"].cursor() as cursor:

                _sql = """ select 	p.survey_id,
                                    o.nome as orgao,
                                    p.titulo,
                                    p.descricao,
                                    p.criado_em,
                                    p.atualizado_em,
                                    ua.username,
                                    p.is_active,
                                    ts.nome as tipo_servico,
                                    p.estado
                            from Pesquisas p 
                            inner join Orgao o on p.orgao_id = o.id 
                            inner join user_auth ua on p.user_id = ua.id 
                            inner join TipoService ts on p.tipo_servico = ts.id  
                        """
                cursor.execute(_sql)
                data = dictfetchall(cursor)

            return data
        
        except Exception as err:
            print(err)

        finally:
            cursor.close()