"""Dashboard de Raças de Cães: app Streamlit."""

import streamlit as st
import dados

def montar_tabela(racas):
    """Prepara as linhas que aparecem na tabela principal, com nomes de coluna legíveis."""
    tabela = []
    for raca in racas:
        raca_exibicao = raca.copy()
        raca_exibicao["treinabilidade"] = "⭐" * raca_exibicao["treinabilidade"]
        linha = {
            "Raça": raca["raca"],
            "Tipo de Pelo": raca["tipo_pelo"],
            "Comprimento": raca["comprimento_pelo"],
            "Nível de Energia": raca["energia"],
            "Faixa de Energia": dados.classificar_energia(raca["energia"]),
            "Treinabilidade": raca_exibicao["treinabilidade"],
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

    racas = dados.carregar_racas()
    if not racas:
        st.error("Não foi possível carregar as raças. Verifique o arquivo racas-de-caes.csv.")
        st.stop()

    aba_catalogo, aba_comparador, aba_favoritos = st.tabs(
        ["🐶 Catálogo", "⚖️ Comparador", "⭐ Favoritos"]
    )

    with aba_catalogo:
        col1, col2, col3 = st.columns(3)
        
        qtd_racas = len(racas)
        col1.metric("Total de Raças", qtd_racas)

        energia_media = dados.calcular_energia_media(racas)
        col2.metric("Energia Média Geral", f"{energia_media:.1f} / 5")

        menor_energia, maior_energia = dados.obter_extremos_energia(racas)

        st.caption(
            f"Faixa de energia das raças: {menor_energia} a {maior_energia} / 5"
        )

        mais_popular = dados.encontrar_mais_popular(racas)
        if mais_popular:
            col3.metric("Raça Mais Popular (2020)", mais_popular["raca"])
            col3.caption(f"Ranking #{mais_popular['popularidade']}")

        st.markdown("---")

    with aba_comparador:
        st.header("⚖️ Comparador de Raças Lado a Lado")
        st.markdown("Selecione duas raças para comparar as suas características principais em formato de tabela:")

        nomes_racas = [r["raca"] for r in racas]
        nomes_racas.sort()

        if len(nomes_racas) >= 2:
            col_comp1, col_comp2 = st.columns(2)
            raca_1_nome = col_comp1.selectbox("Escolha a 1ª Raça para Comparar", nomes_racas, index=0)
            opcoes_segunda_raca = [nome for nome in nomes_racas if nome != raca_1_nome]
            raca_2_nome = col_comp2.selectbox("Escolha a 2ª Raça para Comparar", opcoes_segunda_raca)


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

    with aba_catalogo:
        st.header("🔍 Pesquisa e Filtro Geral de Raças")
        col_busca, col_filtro = st.columns(2)

        busca = col_busca.text_input("Buscar raça por nome")
        tipo_selecionado = col_filtro.selectbox("Filtrar por Tipo de Pelo", ["Todos"] + listar_tipos_pelo(racas))
        ordenacao = st.selectbox(
            "Ordenar resultados por",
            ["Popularidade (2020)", "Nome (A-Z)"]
        )
        racas_filtradas = filtrar_por_tipo_pelo(racas, tipo_selecionado)
        encontradas = buscar_por_nome(racas_filtradas, busca)
        if ordenacao == "Nome (A-Z)":
            encontradas = sorted(
                encontradas,
                key=lambda raca: raca["raca"].lower()
            )
        else:
            encontradas = sorted(
                encontradas,
                key=lambda raca: (
                    raca["popularidade"] <= 0,
                    raca["popularidade"]
                )
            )

        qtd_encontradas = len(encontradas)
        if qtd_encontradas == 0:
            st.warning("⚠️ Nenhum resultado encontrado para os critérios informados.")
        else:
            st.success(f"Raças encontradas: {qtd_encontradas}")
            st.dataframe(montar_tabela(encontradas), use_container_width=True)

        st.markdown("---")

    with aba_favoritos:
        st.header("⭐ Minhas Raças Favoritas")

        nome_favorito = st.selectbox(
            "Selecione uma raça para favoritar",
            nomes_racas
        )

        if st.button("Adicionar aos Favoritos"):
            raca_escolhida = next(
                r for r in racas if r["raca"] == nome_favorito
            )

            if dados.salvar_favorito(raca_escolhida):
                st.success(f"{nome_favorito} adicionada aos favoritos!")
            else:
                st.warning("Esta raça já está nos favoritos.")

        favoritos = dados.carregar_favoritos()

        if favoritos:
            st.subheader("Raças Salvas")
            st.dataframe(
                list(favoritos.values()),
                hide_index=True,
                use_container_width=True
            )
            tipos_pendentes = dados.tipos_pelo_sem_favoritos(racas, favoritos)

            with st.expander(
                f"Tipos de pelo ainda sem favoritos: {len(tipos_pendentes)}"
            ):
                if tipos_pendentes:
                    st.write(", ".join(sorted(tipos_pendentes)))
                else:
                    st.success("Todos os tipos de pelo estão representados!")
            st.subheader("✏️ Editar Favorito")

            nome_edicao = st.selectbox(
                "Selecione a raça para editar",
                sorted(favoritos.keys())
            )

            favorito = favoritos[nome_edicao]

            opcoes_status = [
                "Quero conhecer",
                "Tenho interesse",
                "Já conheço"
            ]

            status = st.selectbox(
                "Status",
                opcoes_status,
                index=opcoes_status.index(favorito["status"]),
                key=f"status_{nome_edicao}"
            )

            comentario = st.text_input(
                "Comentário",
                value=favorito["comentario"],
                key=f"comentario_{nome_edicao}"
            )

            if st.button("Salvar alterações"):
                if dados.atualizar_favorito(nome_edicao, status, comentario):
                    st.rerun()
                else:
                    st.error("Favorito não encontrado.")
            st.markdown("---")

            confirmar = st.checkbox(
                "Confirmo que desejo excluir esta raça dos favoritos",
                key=f"confirmar_{nome_edicao}"
            )

            if st.button("🗑️ Excluir favorito", disabled=not confirmar):
                if dados.remover_favorito(nome_edicao):
                    st.rerun()
                else:
                    st.error("Favorito não encontrado.")
        else:
            st.info("Nenhuma raça favorita cadastrada.")

if __name__ == "__main__":
    main()