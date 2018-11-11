# workshop-neo4j
Workshop sobre Neo4J apresentado durante o CodaBR


## Como rodar os scripts
Para rodar os scripts `load_codas_data.py` e `load_doacao_data.py` é preciso ter [Python 3](https://www.python.org/downloads/) instalado no seu computador. Depois da instalação, siga os passos:

1. Clone o repositório ou baixe os arquivos compactados
2. Crie um novo ambiente virtual `virtualenv env` e ative o ambiente `source env/bin/activate`
3. Instale os requerimentos do projeto `pip install -r requirements.txt`
4. Verifique se o seu Banco de Dados em Grafo Neo4J está rodando
5. Substitua `<your_password>` pela sua senha de acesso ao banco
6. Rode os scripts para carregar os dados de exemplo:
```
> python load_doacao_data.py
> python load_cotas_data.py
```