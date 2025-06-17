import pymysql

try:
    conexao = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='usuarios'
    )
    print("Conexão com o MySQL feita com sucesso usando PyMySQL!")
except pymysql.MySQLError as erro:
    print(f"Erro ao conectar: {erro}")