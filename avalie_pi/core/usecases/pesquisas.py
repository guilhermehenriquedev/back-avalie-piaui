from django.db import connections
from core.utils import dictfetchall
from datetime import datetime

from core.usecases.perguntas import Perguntas

class Pesquisas():

    def listall():
        
        try:
            with connections["defaul"].cursor() as cursor:

                sql = f""" select * from avalie.Pesquisas """
                cursor.execute(sql)
                data = dictfetchall(cursor)

                return data
            
        except Exception as err:

            print("erro...: ", err)
        
        finally:
            cursor.close()

    def create(orgao_id=None, titulo=None, descricao=None, user_id=None, tipo_servico=None):

        try:

            with connections["default"].cursor() as cursor:

                sql = f"""  INSERT INTO avalie.Pesquisas
                                (orgao_id, 
                                titulo, 
                                descricao, 
                                criado_em,
                                user_id, 
                                is_active, 
                                tipo_servico, 
                                estado)
                            VALUES( 
                                {orgao_id}, 
                                '{titulo}', 
                                '{descricao}', 
                                now(),
                                {user_id}, 
                                0, 
                                '{tipo_servico}', 
                                'em analise') """
                # Executar a inserção
                cursor.execute(sql)
                id_gerado = cursor.lastrowid

            return {"new_id": id_gerado}

        except Exception as e:
            print(f"Erro ao registrar ação: {str(e)}")

        finally:
            # Fechar o cursor e a conexão
            cursor.close()

    def get_the_search(survey_id=None):
        """ Busca a pergunta da pesquisa """
        try:

            with connections["default"].cursor() as cursor:

                sql = f""" select 	p.survey_id,
                                    o.id as id_orgao,
                                    o.nome as nome_orgao,
                                    p.titulo,
                                    p.descricao,
                                    p.criado_em,
                                    p.atualizado_em,
                                    p.is_active,
                                    ts.nome,
                                    p.estado,
                                    ts.nome as tipo_servico
                            from Pesquisas p 
                            inner join Orgao o on p.orgao_id = o.id 
                            inner join TipoService ts on p.tipo_servico = ts.id  
                            where p.survey_id = {survey_id} """

                cursor.execute(sql)
                data = dictfetchall(cursor)

            perguntas_da_pesquisa = Perguntas.search_quiz_question(id_pergunta=survey_id)
            data[0]["perguntas"] = perguntas_da_pesquisa

            return data
        
        except Exception as err:
            print(err)

        finally:
            cursor.close()


