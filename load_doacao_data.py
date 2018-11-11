import csv

from py2neo import Graph
from py2neo.data import Node, Relationship


graph = Graph(password="<your_password>")

with open('sample_doacao.csv') as sample_doacao_file:
    sample_doacao_reader = csv.DictReader(sample_doacao_file)

    for doacao in sample_doacao_reader:

        candidato = graph.nodes.match(
            "Parlamentar",
            nome=doacao['Nome candidato']
        ).first()

        if not candidato:
            tx = graph.begin()
            candidato = Node(
                "Parlamentar",
                nome=doacao['Nome candidato'],
                partido=doacao['Sigla Partido']
            )
            tx.create(candidato)
            tx.commit()
            print(f'Criou o no para o candidato {doacao["Nome candidato"]}')

        doador = graph.nodes.match(
            "Doador",
            cnpj=doacao['CPF/CNPJ do doador']
        ).first()

        if not doador:
            tx = graph.begin()
            doador = Node(
                "Doador",
                nome=doacao['Nome do doador'],
                cnpj=doacao['CPF/CNPJ do doador']
            )
            tx.create(doador)
            tx.commit()
            print(f'Criou o no para o doador {doacao["Nome do doador"]}')

        rel_doacao = graph.match(
            nodes=(doador, candidato),
            r_type="DOACAO"
        ).first()

        if not rel_doacao:
            tx = graph.begin()
            rel_doacao = Relationship(
                doador, "DOACAO", candidato,
                valor=float(doacao['Valor receita'])
            )
            tx.create(rel_doacao)
            tx.commit()
            print(f'Criou a relacao de doacao entre \
             {doacao["Nome do doador"]} e {doacao["Nome candidato"]}')
        else:
            rel_doacao['valor'] += float(doacao['Valor receita'])
            graph.push(rel_doacao)
            print(f'Atualizou a relacao de doacao entre \
             {doacao["Nome do doador"]} e {doacao["Nome candidato"]}')
