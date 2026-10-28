"""Leitura e processamento dos dados do projeto de Raças de Cães."""

import csv
from pathlib import Path

# Garante que o Python encontre o CSV na mesma pasta deste script (evita FileNotFoundError)
PASTA = Path(__file__).parent
CAMINHO_CAES = PASTA / "racas-de-caes.csv"


def ler_racas():
    """Lê o CSV de raças de cães e devolve uma lista de dicionários."""
    racas = []
    try:
        with open(CAMINHO_CAES, "r", encoding="utf-8") as ficheiro:
            leitor = csv.DictReader(ficheiro)
            for linha in leitor:
                racas.append(linha)
    except FileNotFoundError:
        print("⚠️ O ficheiro racas-de-caes.csv não foi encontrado na pasta.")
    except Exception as error:
        print("⚠️ Ocorreu um erro na leitura do ficheiro:", error)

    return racas


def converter_inteiro(valor):
    """Converte texto numérico para inteiro de forma segura."""
    try:
        return int(valor)
    except (ValueError, TypeError):
        return 0


def preparar_racas(linhas):
    """Converte os campos numéricos das raças lidas do CSV."""
    racas = []
    for linha in linhas:
        raca = {
            "raca": linha.get("raca", ""),
            "tipo_pelo": linha.get("tipo_pelo", ""),
            "comprimento_pelo": linha.get("comprimento_pelo", ""),
            "energia": converter_inteiro(linha.get("energia", 0)),
            "treinabilidade": converter_inteiro(linha.get("treinabilidade", 0)),
            "popularidade": converter_inteiro(linha.get("popularidade_2020", 0)),
            "link": linha.get("link", "")
        }
        racas.append(raca)
    return racas


def carregar_racas():
    """Lê o CSV e devolve a lista de raças tratadas e prontas para o app."""
    return preparar_racas(ler_racas())


def classificar_energia(energia):
    """Classifica o nível de energia da raça em faixas explicativas."""
    if energia <= 2:
        return "Baixa (Calmo)"
    elif energia == 3:
        return "Média (Moderado)"
    else:
        return "Alta (Energético)"


def calcular_energia_media(racas):
    """Calcula a média do nível de energia de todas as raças."""
    if not racas:
        return 0.0
    soma = sum(raca["energia"] for raca in racas)
    return soma / len(racas)


def encontrar_mais_popular(racas):
    """Encontra a raça com menor número de ranking de popularidade (mais bem colocada)."""
    validas = [r for r in racas if r["popularidade"] > 0]
    if not validas:
        return None
    
    mais_popular = validas[0]
    for raca in validas:
        if raca["popularidade"] < mais_popular["popularidade"]:
            mais_popular = raca
    return mais_popular


if __name__ == "__main__":
    # Teste isolado no terminal: execute 'python dados.py'
    lista_racas = carregar_racas()
    print(f"✅ {len(lista_racas)} raças de cães carregadas com sucesso!")
    if lista_racas:
        print("Exemplo da primeira raça:", lista_racas[0])