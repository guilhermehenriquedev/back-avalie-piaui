from django.db import connections
from core.utils import dictfetchall

from core.usecases.pesquisas import Pesquisas

class CaseAvaliacao():
        
    def get_assessment(hash=None):
        
        try:
            with connections["default"].cursor() as cursor:

                _sql = f""" select 
                            av.id,
                            av.hash,
                            sco.id as 'id_servico',
                            sco.nome as 'nome_servico',
                            o.id as 'id_orgao',
                            o.nome as 'nome_orgao',
                            av.cpf,
                            av.protocolo,
                            av.idPesquisa,
                            av.criado_em,
                            av.respondido_em,
                            av.nome,
                            av.telefone,
                            av.email
                        from Avaliacao as av
                        inner join Servico sco on av.idService = sco.id 
                        inner join Orgao o on av.idOrgao = o.id 
                        where av.hash = '{hash}' """

                cursor.execute(_sql)
                data_avaliacao = dictfetchall(cursor)

            id_pesquisa = data_avaliacao[0]['idPesquisa']

            get_pesquisa = Pesquisas.get_the_search(survey_id=id_pesquisa)

            data_avaliacao[0]['questionario'] = get_pesquisa
            
            return data_avaliacao if data_avaliacao else []
            
        except Exception as err:
            print(err)

        finally:
            cursor.close()

    def list(id=None):

        try:

            with connections["default"].cursor() as cursor:

                sql = f""" 
                    SELECT av.id,
                            av.hash,
                            s.nome as servico,
                            o.nome as orgao,
                            av.cpf,
                            av.protocolo,
                            av.idPesquisa,
                            av.criado_em, 
                            av.respondido_em
                    from Avaliacao av 
                    inner join Servico s on av.idService = s.id
                    inner join Orgao o on av.idOrgao = o.id 
                    """
                cursor.execute(sql)
                data = dictfetchall(cursor)
                return data
                
        except Exception as err:
            print(err)

        finally:
            cursor.close()

    # def send_event_assessment():
    #     procurar o webhook do evento

    #     post.request(webhook)