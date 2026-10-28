# Datasets do Trabalho M2

Sugestões de datasets para o trabalho da M2, em formato CSV (separador `,`, codificação UTF-8).

---

# 🐶 Dashboard de Raças de Cães

Dashboard interativo desenvolvido em Python com a biblioteca Streamlit para exploração, filtragem e comparação de dados de raças de cães do American Kennel Club (AKC).

## Integrantes: 
*Brenda 
*Danilo

## 🚀 Funcionalidades da Aplicação

1. **Métricas Gerais em Tempo Real:**
   * Total de raças cadastradas na base de dados.
   * Média geral do nível de energia das raças.
   * Identificação da raça mais popular com base no ranking de 2020.

2. **Pesquisa e Filtros Dinâmicos:**
   * Campo de busca interativa por nome da raça.
   * Filtro avançado por tipo de pelo.

3. **Comparador de Raças Lado a Lado:**
   * Ferramenta interativa que permite selecionar duas raças e comparar diretamente as suas características (tipo de pelo, comprimento, nível de energia, treinabilidade e popularidade) em formato de tabela lado a lado.

---

## 📂 Estrutura do Projeto
* `app.py`: Código principal responsável pela interface gráfica, métricas, filtros e pela tabela comparativa no Streamlit.
* `dados.py`: Módulo responsável pela leitura segura do ficheiro CSV, tratamento de dados, conversões e cálculos estatísticos.
* `racas-de-caes.csv`: Base de dados oficial contendo as características das raças.

---

   ## Executar

Abra um terminal nesta pasta. Crie um ambiente virtual:
sh
python -m venv .venv


No Linux/macOS, ative com source .venv/bin/activate. No Windows PowerShell, use .venv\Scripts\Activate.ps1.

Depois execute:

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py

## 7. Raças de cães: `racas-de-caes.csv`

- **Fonte original:** [American Kennel Club](https://www.akc.org/dog-breeds/), coletado por [KKakey](https://github.com/kkakey/dog_traits_AKC)
- **Obtido via:** [TidyTuesday 2022-02-01](https://github.com/rfordatascience/tidytuesday/tree/main/data/2022/2022-02-01)

| Coluna | Exemplos de valores |
|---|---|
| `raca` | `Retrievers (Labrador)`, `French Bulldogs` |
| `tipo_pelo` | `Double`, `Smooth`, `Wiry`, `Curly` |
| `comprimento_pelo` | `Short`, `Medium`, `Long` |
| `afeto_familia`, `bom_com_criancas`, `bom_com_outros_caes`, `queda_pelo`, `energia`, `latidos`, `treinabilidade` | de `1` (pouco) a `5` (muito) |
| `popularidade_2020` | `1` = raça mais registrada nos EUA em 2020 |
| `link` | página da raça no site da AKC |
| `imagem` | ilustração da raça (URL) |

