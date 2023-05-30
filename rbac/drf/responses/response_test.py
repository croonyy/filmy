from rbac.drf import schemas

from drf_yasg.openapi import Schema, Response


def response_test():
    return {
        400: Response(description='操作失败',
                      # examples={'json': {'code': -1, 'msg': '失败原因'}},
                      schema=schemas.yasgSchemas.testSchema
                      ),
        200: Response(description='操作成功',
                      examples={'json': {'code': 0, 'msg': '成功'}},
                      schema=schemas.yasgSchemas.testSchema
                      )
    }
