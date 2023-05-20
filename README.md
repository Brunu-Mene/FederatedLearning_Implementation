# Trabalho T1 – Implementação de Aprendizado Federado
## Integrantes: Bruno Menegaz, Gustavo Dutra, Leonardo Albergaria
---
## **Instruções para Compilação e Execução**

Para realizar a instalação basta clonar o repositório para um diretório local e realizar a instalação do python e das bibliotecas grpc, tensorflow, imutils, sklearn*m *pillow e cv2 caso elas não estejam na sua máquina.

Como cada cliente roda em um processo distinto, é necessário dividir previamente a base de dados. Para isso, ao executar o programa *getSplitData*, são criadas pastas com dados para cada cliente. Dessa forma, cada cliente utilizará uma parte dos dados da base Mnist para realizar o treinamento. O repositório contém os dados separados para 3 clientes, então caso haja necessidade de usar uma quantidade diferente de clientes, deve ser executado o seguinte comando (5 clientes neste exemplo):

```
$ python3 getSplitData.py 5
```

Em sequência, deve-se iniciar o servidor. É necessário passar como argumentos *clientsRound, **minClients, **maxRounds* e *accuracyTarget*. Em Linux, a linha de comando ficará da seguinte forma, para 2 clientes por round, mínimo de 2 clients, máximo de 10 rounds e accuracy target de 1.0:

```
$ python3 server.py 2 2 10 1.0
```

Por fim, devem ser iniciados os clientes (utilizando um novo terminal para cada cliente). É necessário passar como argumento o ID do cliente, vale destacar que devemos obedecer a estrutura de diretórios criados em /mnist_data, dessa forma o respectivo ID a ser passado deve se referir a uma pasta criada. A linha de comando do cliente de ID 1 que acessará os dados do diretório /mnist_data/client_1, ficará da seguinte forma:

```
$ python3 client.py 1
```

---
## **Link para o vídeo no Drive**

> https://drive.google.com/file/d/1FsVUoKMTNmcZCnra4a8NeBoQpfEOSrgd/view

---
## **Implementação**
Explicar como funciona o server e o client, explicar funções principais do .proto, plotar os graficos

### **Server**

**Funcionalidades**: 
 - Registro de clientes
 - Treinamento federado
 - Agregação de pesos
 - Validação do modelo global
 - Validação do modelo global

**Biblitecas utilizadas**:
 - grpc
 - threading
 - concurrent.futures
 - queue
 - time
 - sys

**Funcionamento**:

O servidor é responsável por coordenar o treinamento federado. Ele recebe os parâmetros necessários, incluindo o número de rounds desejado para o treinamento. No início de cada round, o servidor verifica se o número mínimo de clientes foi alcançado. Caso contrário, ele aguarda a conexão dos clientes necessários antes de prosseguir.

Em seguida, o servidor sincroniza a disponibilidade para registrar novos clientes, utilizando a flag available_for_register, e inicia uma nova rodada de treinamento. Ele incrementa o número da rodada e envia essa informação para todos os clientes registrados. O servidor cria uma lista de clientes alvo selecionando aleatoriamente a partir dos clientes registrados, usando a função aux.createRandomClientList(). Essa função auxilias entre outras foram utilizadas para facilitar o processo.

Após isso, o servidor inicia o treinamento em paralelo em cada cliente alvo. Ele cria uma lista de threads para chamar o método __callClientLearning para cada cliente alvo, passando o endereço IP do cliente e uma fila (q) para armazenar os resultados do treinamento. Uma vez que todas as threads foram iniciadas, o servidor aguarda até que todas sejam concluídas.

Em seguida, o servidor captura a lista de pesos resultantes do treinamento de cada cliente, bem como o tamanho da amostra de cada cliente, armazenando-os nas listas weights_clients_list e sample_size_list, respectivamente. Após isso, o servidor calcula a média ponderada dos pesos agregando-os através do método __FedAvg. Essa média ponderada representa o modelo global resultante do treinamento.

O servidor então chama o método __callModelValidation para validar o modelo global. Esse método envia o modelo global para cada cliente e coleta as métricas de precisão retornadas por cada cliente. A precisão global média é calculada somando todas as métricas de precisão e dividindo pelo número de clientes. Em seguida, essa informação é exibida junto com o número da rodada atual.

Se a precisão global média atingir ou ultrapassar a meta de precisão especificada, o servidor imprime uma mensagem indicando que a meta foi alcançada e encerra o processo de treinamento. Caso contrário, o servidor continua para a próxima rodada até que a meta de precisão seja atingida ou o número máximo de rounds seja alcançado.

### **Client**

**Funcionalidades**: 
 - Registro do cliente
 - Espera por comandos do servidor
 - Treinamento
 - Validação do modelo
 - Encerramento do cliente

**Biblitecas utilizadas**:

**Funcionamento**:

---
## **Resultados**