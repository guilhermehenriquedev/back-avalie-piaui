from django.db import connections
from core.utils import dictfetchall


class CaseServicos():

    def list_all():

        try:

            with connections["default"].cursor() as cursor:

                sql = f""" 
                        SELECT
                            s.id,
                            COALESCE(o.nome, 'NDA') AS orgao,
                            o.id as id_orgao,
                            COALESCE(ts.nome, 'NDA') AS tipo_servico,
                            s.nome,
                            s.descricao,
                            s.ativo
                        FROM
                            Servico s
                        LEFT JOIN
                            Orgao o ON s.idOrgao = o.id
                        LEFT JOIN
                            TipoService ts ON s.id_tipoService = ts.id;

                    """
                cursor.execute(sql)
                data = dictfetchall(cursor)
                return data
                
        except Exception as err:
            print(err)

        finally:
            cursor.close()

    