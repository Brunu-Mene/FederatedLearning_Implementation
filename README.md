# Trabalho T1 – Implementação de Aprendizado Federado
## Integrantes: Bruno Menegaz, Gustavo Dutra, Leonardo Albergaria
---
## Instruções para Compilação e Execução

Para realizar a instalação basta clonar o repositório para um diretório local e realizar a instalação do python e das bibliotecas *grpc*, *tensorflow*, *imutils*, *sklearn*m *pillow* e *cv2* caso elas não estejam na sua máquina.

Como cada cliente roda em um processo distinto, é necessário dividir previamente a base de dados. Para isso, ao executar o programa **getSplitData**, são criadas pastas com dados para cada cliente. Dessa forma, cada cliente utilizará uma parte dos dados da base Mnist para realizar o treinamento. O repositório contém os dados separados para 3 clientes, então caso haja necessidade de usar uma quantidade diferente de clientes, deve ser executado o seguinte comando (5 clientes neste exemplo):

```
$ python3 getSplitData.py 5
```

Em sequência, deve-se iniciar o servidor. É necessário passar como argumentos **clientsRound**, **minClients**, **maxRounds** e **accuracyTarget**. Em Linux, a linha de comando ficará da seguinte forma, para 2 clientes por round, mínimo de 2 clients, máximo de 10 rounds e accuracy target de 1.0:

```
$ python3 server.py 2 2 10 1.0
```

Por fim, devem ser iniciados os clientes (utilizando um novo terminal para cada cliente). É necessário passar como argumento o ID do cliente, vale destacar que devemos obedecer a estrutura de diretórios criados em */mnist_data*, dessa forma o respectivo ID a ser passado deve se referir a uma pasta criada. A linha de comando do cliente de ID 1 que acessará os dados do diretório */mnist_data/client_1*, ficará da seguinte forma:

```
$ python3 client.py 1
```

---
## Link para o vídeo no Drive

> https://drive.google.com/file/d/1FsVUoKMTNmcZCnra4a8NeBoQpfEOSrgd/view

---
## Implementação
Explicar como funciona o server e o client, explicar funções principais do .proto, plotar os graficos


### Server

### Client
