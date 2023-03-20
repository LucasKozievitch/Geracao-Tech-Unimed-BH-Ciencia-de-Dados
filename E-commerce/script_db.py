##Script para consultas(Queries).

#Realizando a conexão com o Banco de Dados.
#importação das bibliotecas para conexão 1
import mysql.connector
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Testando a conexão, nesse caso crieu um usuário sem senha para teste.
con = mysql.connector.connect(host='localhost',database='ecommerce',user='julio',password='')
if con.is_connected():
    db_info = con.get_server_info()
    print("Conectado ao servidor MySQL versão ",db_info)
    cursor = con.cursor()
    cursor.execute("select database();")
    linha = cursor.fetchone()
    print("Conectado ao banco de dados ",linha)
if con.is_connected():
    cursor.close()
    con.close()
    print("Conexão ao MySQL foi encerrada")

# Exibindo as tabelas do banco de dados.
con = mysql.connector.connect(host='localhost',database='ecommerce',user='julio',password='')
cursor = con.cursor()
cursor.execute('SHOW TABLES')
for i in cursor:
  print(i)

# Consultando uma tabela.
cursor = con.cursor()
cursor.execute('SELECT * FROM clients')
result = cursor.fetchall()
for i in result:
    print(i)


## 1) - Exiba a tabela clients.
# Convertendo as consulta para o tipo pandas dataset - apenas para facilitar a visualização.
pd.read_sql('SELECT * FROM clients',con=con)


## 2) - Informe a quantidade de clientes da tabela 'clients'.
query ="SELECT COUNT(*) AS 'QTD_clientes' FROM clients;"
pd.read_sql(query,con)


## 3) - Exibir todos os clientes que possuem um pedido.
query ="SELECT * FROM clients c, orders o WHERE c.idClient = o.idOrderClient;"
pd.read_sql(query,con)


## 4) - Exibir o nome, sobrenome, id e status da ordem dos clientes que possuem alguma pedido.
query ="SELECT Fname,Lname,idOrder,orderStatus FROM clients c, orders o WHERE c.idClient = idOrderClient;"
pd.read_sql(query,con)


## 5) - Exibir o nome e sobrenome concatenado, a id e o status da ordem.
query ="SELECT CONCAT(Fname, ' ',Lname) AS Cliente,\
idOrder AS Request, orderStatus AS Status FROM clients c,\
orders o WHERE c.idClient = idOrderClient;"
pd.read_sql(query,con)


## 6) - Inserir a ordem do cliente Osvaldo Cruz com id 11, com status da ordem em default, descrição 'site', sendvalue null e paymentcash como 1.
add ="INSERT INTO orders (idOrderClient,OrderStatus,OrderDescription,SendValue,PaymentCash) VALUES (11,DEFAULT,'site',NULL,1);"
meucursor = con.cursor()
meucursor.execute(add)

con.commit()

print("Uma linha foi inserida, ID:", meucursor.lastrowid)


## 7) - Confira se a ordem do cliente Osvaldo foi inserida.
query ="SELECT CONCAT(Fname, ' ',Lname) AS Cliente, idOrder AS Request,\
orderStatus AS Status FROM clients c, orders o WHERE c.idClient = idOrderClient;"
pd.read_sql(query,con)


## 8) - Altere o status da ordem do cliente Osvaldo que possui a requisição núm:17 e 18 para 'Cancelado'.
change = "UPDATE orders SET orderStatus = 'Cancelado' WHERE idOrder IN (17,18) AND idOrderClient = 11;"
meucursor = con.cursor()
meucursor.execute(change)

con.commit()

print("Ordem foi alterada com sucesso, ID:", meucursor.lastrowid)


## 9) - Confira se a ordem do cliente Osvaldo foi alterada conforme solicitado.
query = "SELECT Fname, idOrderClient,orderStatus idOrder FROM clients, \
orders WHERE idOrder IN (17,18) AND idOrderClient = idClient;"
pd.read_sql(query,con)


## 10) - Informe a quantidade de pedidos por clientes.
query ="SELECT COUNT(*) AS 'Qtd Pedidos',CONCAT(Fname, ' ', Lname) AS Cliente,\
orderStatus AS Status FROM clients c, orders o WHERE c.idClient = idOrderClient GROUP BY c.idClient;"
pd.read_sql(query,con)


## 11) - Informe a quantidade de ordens com status cancelado por clientes ordenado por nome de forma descentende.
query ="SELECT idClient AS 'id', CONCAT(Fname, ' ',Lname) AS 'cliente',\
OrderDescription AS 'descrição', OrderStatus AS 'status', COUNT(*) AS 'qtd' FROM Orders,\
Clients WHERE OrderStatus = 'Cancelado' AND IdClient = IdOrderClient GROUP BY IdOrderClient ORDER BY Fname DESC;"
pd.read_sql(query,con)


##12) - Informe a quantidade de produtos por categoria e por localização com avaliação maior ou igual a 4 ordenado por quantidade descendente.
query ="SELECT StorageLocation, Category, Avaliação, SUM(Quantity) AS 'qtd'FROM productstorage,\
products GROUP BY Category, StorageLocation HAVING (Avaliação >= 4) ORDER BY Quantity DESC;"
pd.read_sql(query,con)