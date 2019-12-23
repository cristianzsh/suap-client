import json
import requests
import sys
from prettytable import PrettyTable

try:
    with open(".config", "r") as f:
        lines = f.readlines()
        auth = {"username": lines[0].split("=")[1][:-1],
                "password": lines[1].split("=")[1][:-1]}
except:
    print("Arquivo de configuração inexistente!")
    sys.exit(1)

if len(sys.argv) <= 2:
    year = input("Ano letivo: ")
    term = input("Semestre: ")
else:
    year = sys.argv[1]
    term = sys.argv[2]

urls = {"token" : "https://suap.ifrn.edu.br/api/v2/autenticacao/token/",
        "data" : "https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/{}/{}".format(year, term)}

def get_token():
    response = requests.post(urls['token'], data = auth)
    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8"))["token"]

    return None

header = {"Authorization": "JWT {0}".format(get_token())}

def get_info():
    response = requests.get(urls["data"], headers = header)
    if response.status_code == 200:
        return response.content.decode("utf-8")

    return None

try:
    info = json.loads(get_info())
except:
    print("Erro ao obter as informações!")
    sys.exit(1)

table = PrettyTable(["Disciplina", "N1", "F1", "N2", "F2", "MD"])
for i in info:
    table.add_row([i["disciplina"],
        i["nota_etapa_1"]["nota"],
        i["nota_etapa_1"]["faltas"],
        i["nota_etapa_2"]["nota"],
        i["nota_etapa_2"]["faltas"],
        i["media_final_disciplina"]])

print(table)
