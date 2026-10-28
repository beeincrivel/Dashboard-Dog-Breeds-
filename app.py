"""Dashboard de Raças de Cães: app Streamlit."""

import streamlit as st
import dados

def montar_tabela(racas):
    """Prepara as linhas que aparecem na tabela principal, com nomes de coluna legíveis."""
    tabela = []
    for raca in racas:
        linha = {
            "Raça": raca["raca"],
            "Tipo de Pelo": raca["tipo_pelo"],
            "Comprimento": raca["comprimento_pelo"],
            "Nível de Energia": raca["energia"],
            "Faixa de Energia": dados.classificar_energia(raca["energia"]),
            "Treinabilidade": "⭐" * raca["treinabilidade"],
            "Popularidade (2020)": raca["popularidade"]
        }
        tabela.append(linha)
    return tabela

def buscar_por_nome(racas, busca):
    """Devolve apenas as raças cujo nome contém o texto buscado (case-insensitive)."""
    encontradas = []
    for raca in racas:
        if busca.lower().strip() in raca["raca"].lower().strip():
            encontradas.append(raca)
    return encontradas

def listar_tipos_pelo(racas):
    """Devolve os tipos de pelo únicos, em ordem alfabética."""
    tipos = []
    for raca in racas:
        if raca["tipo_pelo"] and raca["tipo_pelo"] not in tipos:
            tipos.append(raca["tipo_pelo"])
    tipos.sort()
    return tipos

def filtrar_por_tipo_pelo(racas, tipo_pelo):
    """Filtra as raças pelo tipo de pelo selecionado."""
    if tipo_pelo == "Todos":
        return racas
    
    resultado = []
    for raca in racas:
        if raca["tipo_pelo"] == tipo_pelo:
            resultado.append(raca)
    return resultado

def main():
    st.set_page_config(page_title="Dashboard de Raças de Cães", page_icon="🐶", layout="wide")
    st.title("🐶 Dashboard de Raças de Cães")
    st.markdown("Explore dados e características das raças de cães do American Kennel Club.")

    # Carreg
    racas = dados.carregar_racas()

    # --- 3 MÉTRICAS OBRIGATÓRIAS ---
    col1, col2, col3 = st.columns(3)
    
    qtd_racas = len(racas)
    col1.metric("Total de Raças", qtd_racas)

    energia_media = dados.calcular_energia_media(racas)
    col2.metric("Energia Média Geral", f"{energia_media:.1f} / 5")

    mais_popular = dados.encontrar_mais_popular(racas)
    if mais_popular:
        col3.metric("Raça Mais Popular (2020)", mais_popular["raca"])
        col3.caption(f"Ranking #{mais_popular['popularidade']}")

    st.markdown("---")

    # --- SEÇÃO DE COMPARADOR LADO A LADO ---
    st.header("⚖️ Comparador de Raças Lado a Lado")
    st.markdown("Selecione duas raças para comparar as suas características principais em formato de tabela:")

    nomes_racas = [r["raca"] for r in racas]
    nomes_racas.sort()

    if len(nomes_racas) >= 2:
        col_comp1, col_comp2 = st.columns(2)
        raca_1_nome = col_comp1.selectbox("Escolha a 1ª Raça para Comparar", nomes_racas, index=0)
        raca_2_nome = col_comp2.selectbox("Escolha a 2ª Raça para Comparar", nomes_racas, index=min(1, len(nomes_racas) - 1))

        # Obter os dados completos das raças selecionadas
        info_raca1 = next((r for r in racas if r["raca"] == raca_1_nome), None)
        info_raca2 = next((r for r in racas if r["raca"] == raca_2_nome), None)

        if info_raca1 and info_raca2:
            # Montar uma tabela dedicada para a comparação
            tabela_comparacao = [
                {
                    "Característica / Atributo": "Raça",
                    f"{info_raca1['raca']}": info_raca1['raca'],
                    f"{info_raca2['raca']}": info_raca2['raca']
                },
                {
                    "Característica / Atributo": "Tipo de Pelo",
                    f"{info_raca1['raca']}": info_raca1['tipo_pelo'],
                    f"{info_raca2['raca']}": info_raca2['tipo_pelo']
                },
                {
                    "Característica / Atributo": "Comprimento do Pelo",
                    f"{info_raca1['raca']}": info_raca1['comprimento_pelo'],
                    f"{info_raca2['raca']}": info_raca2['comprimento_pelo']
                },
                {
                    "Característica / Atributo": "Nível de Energia (1 a 5)",
                    f"{info_raca1['raca']}": f"{info_raca1['energia']} / 5 ({dados.classificar_energia(info_raca1['energia'])})",
                    f"{info_raca2['raca']}": f"{info_raca2['energia']} / 5 ({dados.classificar_energia(info_raca2['energia'])})"
                },
                {
                    "Característica / Atributo": "Treinabilidade",
                    f"{info_raca1['raca']}": "⭐" * info_raca1['treinabilidade'],
                    f"{info_raca2['raca']}": "⭐" * info_raca2['treinabilidade']
                },
                {
                    "Característica / Atributo": "Popularidade (2020)",
                    f"{info_raca1['raca']}": f"#{info_raca1['popularidade']}" if info_raca1['popularidade'] > 0 else "N/A",
                    f"{info_raca2['raca']}": f"#{info_raca2['popularidade']}" if info_raca2['popularidade'] > 0 else "N/A"
                }
            ]

            st.dataframe(tabela_comparacao, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- BUSCA E FILTROS PRINCIPAIS ---
    st.header("🔍 Pesquisa e Filtro Geral de Raças")
    col_busca, col_filtro = st.columns(2)

    busca = col_busca.text_input("Buscar raça por nome")
    tipo_selecionado = col_filtro.selectbox("Filtrar por Tipo de Pelo", ["Todos"] + listar_tipos_pelo(racas))

    # Aplicar filtros principais da tabela
    racas_filtradas = filtrar_por_tipo_pelo(racas, tipo_selecionado)
    encontradas = buscar_por_nome(racas_filtradas, busca)

    qtd_encontradas = len(encontradas)

    # --- RESULTADOS E TABELA ---
    if qtd_encontradas == 0:
        st.warning("⚠️ Nenhum resultado encontrado para os critérios informados.")
    else:
        st.success(f"Raças encontradas: {qtd_encontradas}")
        st.dataframe(montar_tabela(encontradas), use_container_width=True)

if __name__ == "__main__":
    main()