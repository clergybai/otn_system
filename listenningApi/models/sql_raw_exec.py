from common.database import tr_session


class SqlRawExec():

    @classmethod
    def exec(cls, sql):
        return tr_session.execute(sql)
