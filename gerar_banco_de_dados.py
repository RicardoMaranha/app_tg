import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='123456'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `banco_tg`;")

cursor.execute("CREATE DATABASE `banco_tg`;")

cursor.execute("USE `banco_tg`;")

# criando tabelas
TABLES = {}
TABLES['Fornecedores'] = ('''
        CREATE TABLE `fornecedores` (
        `id_fornecedor` int(11) NOT NULL AUTO_INCREMENT,
        `nome` varchar(100) NOT NULL,
        `cnpj` varchar(18) UNIQUE NOT NULL,
        `cep` varchar(10),
        `cidade` varchar(100),
        `estado` varchar(50),
        `rua` varchar(255),
        `numero` varchar(20),
        `telefone` varchar(15),
        `email` varchar(50),
        PRIMARY KEY (`id_fornecedor`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(50) NOT NULL,
      `nickname` varchar(50) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Bruno Divino", "BD", "alohomora"),
      ("Camila Ferreira", "Mila", "paozinho"),
      ("Ricardo", "Rickmaranha", "Cecilia")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from banco_tg.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
fornecedores_sql = 'INSERT INTO fornecedores (cnpj, nome, cep, cidade, estado, rua, numero, telefone, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
fornecedores = [
      ('0000111/0001', 'Ricardo SA', '14407-216', 'Franca', 'SP', 'Rua Abel Vergani Filho', '1465', '1633333333','ricardo@gmail.com'),
      ('0000333/0002', 'Cecilia SA', '14408-136', 'Franca', 'SP', 'Rua Domingos', '730', '1634341616','cecilia@gmail.com'),
      
]
cursor.executemany(fornecedores_sql, fornecedores)

cursor.execute('select * from banco_tg.fornecedores')
print(' -------------  fornecedores:  -------------')
for fornecedor in cursor.fetchall():
    print(fornecedor[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()