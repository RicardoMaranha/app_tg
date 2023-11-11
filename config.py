

SECRET_KEY = 'Cecilia-260320'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'Cecilia-260320',
        servidor = 'localhost',
        database = 'banco_tg'
    )

