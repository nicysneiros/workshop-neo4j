import csv

from py2neo import Graph
from py2neo.data import Node, Relationship


graph = Graph(password="<your_password>")

with open('sample_cota.csv') as sample_cota_file:
    sample_cota_reader = csv.DictReader(sample_cota_file)

    for cota in sample_cota_reader:

        parlamentar = graph.nodes.match(
            "Parlamentar",
            nome=cota['txNomeParlamentar']
        ).first()

        if not parlamentar:
            tx = graph.begin()
            parlamentar = Node(
                "Parlamentar",
                nome=cota['txNomeParlamentar'],
                partido=cota['sgPartido']
            )
            tx.create(parlamentar)
            tx.commit()
            print(f'Criou o no para o parlamentar {cota["txNomeParlamentar"]}')

        empresa = graph.nodes.match(
            "Doador",
            cnpj=cota['txtCNPJCPF']
        ).first()

        if not empresa:
            tx = graph.begin()
            empresa = Node(
                "Doador",
                nome=cota['txtFornecedor'],
                cnpj=cota['txtCNPJCPF']
            )
            tx.create(empresa)
            tx.commit()
            print(f'Criou o no para a empresa {cota["txtFornecedor"]}')

        rel_cota = graph.match(
            nodes=(parlamentar, empresa),
            r_type="COTA"
        ).first()

        if not rel_cota:
            tx = graph.begin()
            rel_cota = Relationship(
                parlamentar, "COTA", empresa,
                valor=float(cota['vlrLiquido'])
            )
            tx.create(rel_cota)
            tx.commit()
            print(f'Criou a relacao de cota entre \
             {cota["txNomeParlamentar"]} e {cota["txtFornecedor"]}')
        else:
            rel_cota['valor'] += float(cota['vlrLiquido'])
            graph.push(rel_cota)
            print(f'Atualizou a relacao de cota entre \
             {cota["txNomeParlamentar"]} e {cota["txtFornecedor"]}')
