import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Kindness Knots", layout="wide")

# -------------------------------
# Pastas e CSV
# -------------------------------
PRODUTOS_CSV = "produtos.csv"
IMAGENS_FOLDER = "imagens"

# -------------------------------
# Inicializar carrinho
# -------------------------------
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# -------------------------------
# Função para carregar produtos
# -------------------------------
@st.cache_data(ttl=5)  # Atualiza a cada 5 segundos
def carregar_produtos():
    try:
        return pd.read_csv(PRODUTOS_CSV)
    except:
        return pd.DataFrame(columns=["nome","categoria","preco","imagem"])

produtos_df = carregar_produtos()

# -------------------------------
# Sidebar - Categorias
# -------------------------------
st.sidebar.title("Categorias")
categorias = ["Todos", "Chaveiros", "Broches", "Pelúcias", "Amigurumis"]
categoria_selecionada = st.sidebar.radio("Escolha a categoria:", categorias)

# -------------------------------
# Sidebar - Carrinho
# -------------------------------
st.sidebar.header("Carrinho 🛒")
if st.session_state.carrinho:
    total = 0
    for item in st.session_state.carrinho:
        st.sidebar.write(f"{item['nome']} - R${item['preco']}")
        total += item['preco']
    st.sidebar.write(f"**Total: R${total:.2f}**")
    if st.sidebar.button("Finalizar Compra"):
        st.sidebar.write("Clique no link abaixo para finalizar no Instagram:")
        st.sidebar.markdown("[Abrir DM Instagram](https://www.instagram.com/kindnessknots/)")
else:
    st.sidebar.write("Carrinho vazio.")

# -------------------------------
# Filtrar produtos
# -------------------------------
if categoria_selecionada != "Todos":
    produtos_df = produtos_df[produtos_df["categoria"] == categoria_selecionada]

# -------------------------------
# Exibir produtos
# -------------------------------
st.title("Kindness Knots - Loja")

for i, produto in produtos_df.iterrows():
    cols = st.columns([1, 2])
    with cols[0]:
        if os.path.exists(produto["imagem"]):
            st.image(produto["imagem"], width=150)
        else:
            st.write("Imagem não encontrada")
    with cols[1]:
        st.subheader(produto["nome"])
        st.write(f"Categoria: {produto['categoria']}")
        st.write(f"Preço: R${produto['preco']}")
        if st.button("Adicionar ao carrinho", key=f"add_{i}"):
            st.session_state.carrinho.append(produto)
            st.success(f"{produto['nome']} adicionado ao carrinho!")
