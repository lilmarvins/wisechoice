class Config(object):
    DATABASE_URI= 'sqlite:///:memory'
    ADMIN_ID= '1w456'



class ProductionConfig(Config):
    DATABASE_URI= 'mysql://user@localhost/foo'
    ADMIN_ID= 'asdfgh455^&(AG&*'
    SECRET_KEY= 'productiont'


class DevelopmentConfig(Config):
    DATABASE_URI= 'mysql://demo@localhost/foo'
    ADMIN_ID= 'thisisadmin'
    SECRET_KEY= 'marvinddevelopment'