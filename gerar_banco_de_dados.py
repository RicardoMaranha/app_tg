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
        `id_fornecedor` int NOT NULL AUTO_INCREMENT,
        `nome` varchar(100) NOT NULL,
        `cnpj` varchar(18) UNIQUE NOT NULL,
        `cep` varchar(10),
        `cidade` varchar(100),
        `estado` varchar(50),
        `rua` varchar(255),
        `numero` varchar(20),
        `telefone` varchar(15),
        `email` varchar(50),
        PRIMARY KEY (`id_fornecedor`, `cnpj`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(50) NOT NULL,
      `nickname` varchar(50) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Clientes'] = ('''
      CREATE TABLE `clientes`(
      `id_cliente` int NOT NULL AUTO_INCREMENT,
      `nome` varchar(100) NOT NULL,
      `documento` varchar(18) UNIQUE NOT NULL,
      `cep` varchar(10),
      `cidade` varchar(100),
      `estado` varchar(50),
      `rua` varchar(255),
      `numero` varchar(20),
      `telefone` varchar(15),
      `email` varchar(50),
      PRIMARY KEY (`id_cliente`, `documento`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


"""
TABLES['Ficha'] = ('''
      CREATE TABLE `pedidos` (
      `id_pedito` INT NOT NULL AUTO_INCREMENT,
      `nome_cliente` varchar(100),
      `documento_cliente` varchar(18),
      `data_pedido` date NOT NULL,               
      FOREIGN KEY (`nome_cliente`,`documento_cliente`) REFERENCES Clientes(`nome`,`documento`)
      PRIMARY KEY (`pedido_id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')
"""

TABLES['Item'] = ('''
      CREATE TABLE `item` (
      `id_item` int NOT NULL AUTO_INCREMENT,
      `referencia` varchar(50) NOT NULL,
      `descricao` varchar(255),
      PRIMARY KEY (`id_item`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Tamanho'] = ('''
      CREATE TABLE `tamanho`(
      `id_tamanho` int NOT NULL AUTO_INCREMENT,
      `tamanho` varchar(50) NOT NULL,
      PRIMARY KEY (`id_tamanho`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['EstoqueProduto'] = ('''
      CREATE TABLE `estoqueproduto`(
      `id_item` int NOT NULL,
      `tamanho` int NOT NULL,
      `quantidade` int NOT NULL,
      PRIMARY KEY (`id_item`,`tamanho`),
      FOREIGN KEY (`id_item`) REFERENCES `item` (`id_item`),
      FOREIGN KEY (`tamanho`) REFERENCES `tamanho` (`id_tamanho`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Pedidos'] = ('''
      CREATE TABLE `pedidos` (
    `id_pedido` int NOT NULL AUTO_INCREMENT,
    `id_cliente` int NOT NULL,
    `id_item` int NOT NULL,
    `tamanho` int NOT NULL,
    `quantidade` int NOT NULL,
    PRIMARY KEY (`id_pedido`),  -- Correção: definindo id_pedido como chave primária
    FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`),
    FOREIGN KEY (`id_item`) REFERENCES `item` (`id_item`),
    FOREIGN KEY (`tamanho`) REFERENCES `tamanho` (`id_tamanho`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['MateriaPrima'] = ('''
      CREATE TABLE `materiaprima` (
    `id_materiaprima` int NOT NULL AUTO_INCREMENT,
    `referencia_material` varchar(255) NOT NULL,
    `nome_material` varchar(100) NOT NULL,
    PRIMARY KEY (`id_materiaprima`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['EstoqueMateriaPrima'] = ('''
      CREATE TABLE `estoquemateriaprima` (
    `id_estoque` int NOT NULL AUTO_INCREMENT,
    `materiaprima` int NOT NULL,
    `quantidade` int NOT NULL,
    `tipo` varchar(50),
    `preco` float,
    `data_entrada` varchar(10) NOT NULL,
    `data_validade` varchar(10),
    `fornecedor` int,
    `descricao` varchar(255),
    PRIMARY KEY (`id_estoque`),
    FOREIGN KEY (`materiaprima`) REFERENCES `materiaprima`(`id_materiaprima`),
    FOREIGN KEY (`fornecedor`) REFERENCES `fornecedores`(`id_fornecedor`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['ProdutoMateriaPrima'] = ('''
      CREATE TABLE `produtomateriaprima` (
    `id_item` int,
    `id_materiaprima` int,
    `quantidade` float NOT NULL,
    PRIMARY KEY (`id_item`, `id_materiaprima`),
    FOREIGN KEY (`id_item`) REFERENCES `item` (`id_item`),
    FOREIGN KEY (`id_materiaprima`) REFERENCES `materiaprima` (`id_materiaprima`)
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
      ("Ricardo", "RicardoM", "123456"),
      ("Rhayssa", "RhayssaA", "123456"),
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from banco_tg.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo Clientes
clientes_sql = 'INSERT INTO clientes (documento, nome, cep, cidade, estado, rua, numero, telefone, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
clientes = [
      ('0000111/0001', 'Batman ', '14407-216', 'Franca', 'SP', 'Rua Abel Vergani Filho', '1465', '1633333333','batman@gmail.com'),
      ('0000333/0002', 'Robin ', '14408-136', 'Franca', 'SP', 'Rua Domingos', '730', '1634341616','robin@gmail.com'),
      
]
cursor.executemany(clientes_sql, clientes)

cursor.execute('select * from banco_tg.clientes')
print(' -------------  Clientes:  -------------')
for cliente in cursor.fetchall():
    print(cliente[1])

# inserindo fornecedores
fornecedores_sql = 'INSERT INTO fornecedores (cnpj, nome, cep, cidade, estado, rua, numero, telefone, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
fornecedores = [
      ('0000111/0001', 'Ricardo SA', '14407-216', 'Franca', 'SP', 'Rua Abel Vergani Filho', '1465', '1633333333',
       'ricardo@gmail.com'),
      ('0000333/0002', 'Cecilia SA', '14408-136', 'Franca', 'SP', 'Rua Domingos', '730', '1634341616',
       'cecilia@gmail.com'),

]
cursor.executemany(fornecedores_sql, fornecedores)

cursor.execute('select * from banco_tg.fornecedores')
print(' -------------  fornecedores:  -------------')
for fornecedor in cursor.fetchall():
      print(fornecedor[1])

# inserindo Itens
item_sql = 'INSERT INTO item (referencia, descricao) VALUES (%s, %s)'
itens = [
      ("Prada", "Calçado Feminino de Borracha"),
      ("Lady", "Calçado Feminino de Borracha"),
      ("All Star", "Calçado masculino de borracha"),
]
cursor.executemany(item_sql, itens)

cursor.execute('select * from banco_tg.item')
print(' -------------  Itens:  -------------')
for iten in cursor.fetchall():
    print(iten[1])


# inserindo Tamanhos
tamanho_sql = 'INSERT INTO tamanho (tamanho) VALUES (%s)'
tamanho = [
      ("30",),
      ("32",),
      ("34",),
      ("36",),
      ("38",),
      ("40",),
      ("42",),
      ("44",),
      ("46",),
]
cursor.executemany(tamanho_sql, tamanho)

cursor.execute('select * from banco_tg.tamanho')
print(' -------------  Tamanho:  -------------')
for taman in cursor.fetchall():
    print(taman[1])

'''

'''
# inserindo Produto Estoque
produtoestoque_sql = 'INSERT INTO estoqueproduto (id_item, tamanho, quantidade) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE quantidade = quantidade + VALUES(quantidade)'
produtoestoque = [
      (1, 1, 5),
      (1, 2, 10),
      (1, 3, 15),
      (1, 4, 15),
      (1, 5, 10),
      (1, 6, 5),
      (1, 7, 5),
      (2, 1, 5),
      (2, 2, 10),
      (2, 3, 15),
      (2, 4, 15),
      (2, 5, 10),
      (2, 6, 5),
      (2, 7, 5),
]

for id_item, tamanho, quantidade in produtoestoque:
    cursor.execute(produtoestoque_sql, (id_item, tamanho, quantidade))

cursor.execute('select * from banco_tg.estoqueproduto')
print(' -------------  Estoque de Produto:  -------------')
for prodestoque in cursor.fetchall():
      print(f'Item: {prodestoque[0]}, Tamanho: {prodestoque[1]}, Quantidade: {prodestoque[2]}')


# inserindo MateriaPrima
materiaprima_sql = 'INSERT INTO materiaprima (referencia_material, nome_material) VALUES (%s, %s)'
materiaprima = [
      ('bo123', 'Borracha'),
      ('si222', 'Silicone'),
      ('re321', 'Reagente'),
]
cursor.executemany(materiaprima_sql, materiaprima)

cursor.execute('select * from banco_tg.materiaprima')
print(' -------------  Materia Prima:  -------------')
for material in cursor.fetchall():
      print(material[1])


# inserindo estoque materia prima
estomaterial_sql = 'INSERT INTO estoquemateriaprima (materiaprima, quantidade, tipo, preco, data_entrada, data_validade, fornecedor, descricao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE quantidade = quantidade + VALUES (quantidade)'
estomaterial = [
      (1, 1000,'placa', 9.90, '2023-11-11', '2024-11-11', 1 ,'Borracha de alta qualide, para solados'),
      (2, 1000, 'unidade', 2.99, '2023-11-11', '2024-11-11', 2, 'Silicone liquido'),
]
cursor.executemany(estomaterial_sql, estomaterial)

cursor.execute('select * from banco_tg.estoquemateriaprima')
print(' -------------  Estoque Materia Prima:  -------------')
for estmaterial in cursor.fetchall():
      print(f'id_materiaprima: {estmaterial[0]},Materia_Prima: {estmaterial[1]}, quantidade: {estmaterial[2]} Tipo: {estmaterial[3]}, Preço: R$ {estmaterial[4]}, data_de_entrada: {estmaterial[5]}, data_de_validade: {estmaterial[6]}, fornecedor: {estmaterial[7]}, descrção: {estmaterial[8]} ')





# inserindo ProdutoMateriaPrima
produtomateriaprima_sql = ('INSERT INTO produtomateriaprima (id_item, id_materiaprima, quantidade) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE quantidade = quantidade + VALUES(quantidade)')
produtomateriaprima = [
      (1, 1, 2),
      (1, 2, 2),
      (2, 1, 2),
      (2, 2, 2),
]
cursor.executemany(produtomateriaprima_sql, produtomateriaprima)

cursor.execute('select * from banco_tg.estoquemateriaprima')
print(' -------------  prodmaterial:  -------------')
for prodmateria in cursor.fetchall():
      print(f'Item:{prodmateria[0]}, Material:{prodmateria[1]}, Quantidade: {prodmateria[2]}')

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
