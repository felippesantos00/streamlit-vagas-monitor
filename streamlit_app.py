import streamlit as st
import requests
import os
st.set_page_config(page_title="Vagas", layout="wide")

st.title("🔎 Vagas disponíveis")

# N8N_ENDPOINT = "http://192.168.15.95:5678/webhook/84fb40e7-05a6-4bc1-ac67-839296772b3a"  # troque aqui


@st.cache_data(ttl=300)
def carregar_vagas():
    # response = requests.get(N8N_ENDPOINT, timeout=30)
    response = requests.get(os.getenv("E",st.secrets["E"]), timeout=30)
    response.raise_for_status()
    return response.json()


try:
    vagas = carregar_vagas()
    st.write("### Vagas encontradas:")
    if not vagas:
        st.warning("Nenhuma vaga encontrada.")
    else:   

        for vaga in vagas:
            with st.container(border=True):
                st.subheader(vaga.get("name", "Sem título"))

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(
                        f"**Empresa:** {vaga.get('careerPageName', 'N/A')}")

                with col2:
                    cidade = vaga.get("city", "")
                    estado = vaga.get("state", "")
                    local = f"{cidade}/{estado}" if cidade or estado else "N/A"
                    st.write(f"**Local:** {local}")

                with col3:
                    remoto = vaga.get("isRemoteWork", "") 
                    normalized = "Sim" if remoto is True else "Não" if remoto is False else ""
                    remoto = normalized
                    st.write(
                        f"**Remoto:** {remoto if remoto != '' else 'N/A'}")

                if vaga.get("description"):
                    with st.expander("Descrição"):
                        st.markdown(str(vaga["description"])[0:200]+"...",
                                    unsafe_allow_html=True)

                if vaga.get("jobUrl"):
                    st.markdown(f"🔗 [Ver vaga]({vaga['jobUrl']})")

                st.caption(
                    f"Publicado em: {vaga.get('publishedDate', 'N/A')}")
        st.markdown("---")
        st.markdown(
            """
            # 🙋 Sobre o Autor
            ## 📫 Contato

            - Email: felipperodrigues00@gmail.com
            - LinkedIn: https://www.linkedin.com/in/felippe-santos-54058111a/
            - Medium: https://medium.com/@felipperodrigues00
            """
        )
except Exception as e:
    st.error("Erro ao carregar vagas")
    st.exception(e)
