

secret_key = 'cecilia'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '123456',
        servidor = 'localhost',
        database = 'banco_tg'
    )

