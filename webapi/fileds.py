import sqlalchemy.types as types


class CommaList(types.TypeDecorator):
    '''
    Comma splitted string list.
    '''

    impl = types.Unicode

    def process_bind_param(self, value, dialect):
        if not value:
            return ''
        return ','.join(value)

    def process_result_value(self, value, dialect):
        if not value:
            return []
        return value.split(',')
