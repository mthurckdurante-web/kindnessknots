import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

# -------------------------------
# Configuração Firebase
# -------------------------------
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://kindnessknots-c6b86-default-rtdb.firebaseio.com/"
})

st.set_page_config(page_title="Kindness Knots", layout="wide")

# -------------------------------
# Inicializar carrinho
# -------------------------------
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# -------------------------------
# Carregar produtos do Firebase
# -------------------------------
ref = db.reference("produtos")
produtos_data = ref.get()  # retorna dicionário

if produtos_data:
    produtos_df = pd.DataFrame.from_dict(produtos_data, orient="index")
else:
    produtos_df = pd.DataFrame(columns=["nome","categoria","preco","imagem"])

# -------------------------------
# Sidebar categorias
# -------------------------------
st.sidebar.title("Categorias")
categorias = ["Todos", "Chaveiros", "Broches", "Pelúcias", "Amigurumis"]
categoria_selecionada = st.sidebar.radio("Escolha a categoria:", categorias)

# -------------------------------
# Sidebar carrinho
# -------------------------------
st.sidebar.header("Carrinho 🛒")
if st.session_state.carrinho:
    total = sum([item["preco"] for item in st.session_state.carrinho])
    for item in st.session_state.carrinho:
        st.sidebar.write(f"{item['nome']} - R${item['preco']}")
    st.sidebar.write(f"**Total: R${total:.2f}**")
    if st.sidebar.button("Finalizar Compra"):
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
    cols = st.columns([1,2])
    with cols[0]:
        st.image(produto["imagem"], width=150)
    with cols[1]:
        st.subheader(produto["nome"])
        st.write(f"Categoria: {produto['categoria']}")
        st.write(f"Preço: R${produto['preco']}")
        if st.button("Adicionar ao carrinho", key=f"add_{i}"):
            st.session_state.carrinho.append(produto)
            st.success(f"{produto['nome']} adicionado ao carrinho!")
