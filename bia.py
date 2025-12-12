import streamlit as st
from PIL import Image
import pandas as pd
import os
import json

# ------------------------------
# CONFIGURAÇÕES DO SITE
# ------------------------------
st.set_page_config(page_title="Loja da Vendedora", layout="wide")

st.markdown("""
<style>
body {
    background-color: #f7f5f2;
}
</style>
""", unsafe_allow_html=True)

PALETA = {
    "fundo": "#f7f5f2",
    "card": "#ffffff",
    "primaria": "#b8c8d1",
    "secundaria": "#d8c7dd",
    "detalhe": "#c7e2d5"
}

# ------------------------------
# CARREGAR DADOS (com persistência)
# ------------------------------
DATA_FILE = "produtos.json"

def carregar_produtos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_produtos(produtos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

if "produtos" not in st.session_state:
    st.session_state.produtos = carregar_produtos()

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

CATEGORIAS = ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"]

# ------------------------------
# SIDEBAR COM FILTROS
# ------------------------------
st.sidebar.title("Filtros")

busca = st.sidebar.text_input("Buscar produto pelo nome:")
categoria_filtro = st.sidebar.selectbox("Filtrar por categoria:", ["Todas"] + CATEGORIAS)

if st.sidebar.button("Limpar filtros"):
    busca = ""
    categoria_filtro = "Todas"

# ------------------------------
# MENU SUPERIOR
# ------------------------------
pagina = st.selectbox("Menu", ["Produtos", "Carrinho", "Admin (Vendedora)"])

# ------------------------------
# EXIBIÇÃO DOS PRODUTOS
# ------------------------------
def exibir_produtos(lista):
    cols = st.columns(3)

    for i, produto in enumerate(lista):
        with cols[i % 3]:
            st.markdown(f"### {produto['nome']}")
            try:
                st.image(produto["img"], width=200)
            except:
                st.image("https://via.placeholder.com/200")

            st.write(f"Preço: R$ {produto['preco']:.2f}")
            st.write(f"Estoque: {produto['estoque']}")

            if st.button(f"Adicionar ao carrinho - {produto['nome']}"):
                st.session_state.carrinho.append(produto)
                st.success("Adicionado ao carrinho!")

# ------------------------------
# PÁGINA DE PRODUTOS
# ------------------------------
if pagina == "Produtos":
    st.title("🛍️ Produtos Disponíveis")

    produtos_filtrados = st.session_state.produtos

    if busca:
        produtos_filtrados = [p for p in produtos_filtrados if busca.lower() in p["nome"].lower()]

    if categoria_filtro != "Todas":
        produtos_filtrados = [p for p in produtos_filtrados if p["categoria"] == categoria_filtro]

    abas = st.tabs(CATEGORIAS)

    for i, categoria in enumerate(CATEGORIAS):
        with abas[i]:
            st.subheader(categoria)
            lista = [p for p in produtos_filtrados if p["categoria"] == categoria]
            exibir_produtos(lista)

# ------------------------------
# PÁGINA DO CARRINHO
# ------------------------------
if pagina == "Carrinho":
    st.title("🧺 Seu Carrinho")

    if len(st.session_state.carrinho) == 0:
        st.info("Seu carrinho está vazio.")
    else:
        total = sum(p["preco"] for p in st.session_state.carrinho)

        for item in st.session_state.carrinho:
            st.write(f"- {item['nome']} — R$ {item['preco']:.2f}")

        st.markdown(f"## Total: R$ {total:.2f}")

        st.success("Sua encomenda foi registrada! Entre em contato no Instagram para combinar pagamento:")
        st.markdown("### 👉 [Instagram da Vendedora](https://instagram.com/sua_conta_aqui)")

        if st.button("Limpar carrinho"):
            st.session_state.carrinho = []
            st.experimental_rerun()

# ------------------------------
# ADMIN (VENDEDORA)
# ------------------------------
if pagina == "Admin (Vendedora)":
    st.title("🔐 Área da Moderadora")

    senha = st.text_input("Senha da moderadora:", type="password")

    if senha == "1234":  # Troque essa senha!
        st.success("Acesso permitido!")

        st.subheader("Adicionar novo produto")

        nome = st.text_input("Nome do produto:")
        preco = st.number_input("Preço:", min_value=0.0)
        estoque = st.number_input("Estoque:", min_value=0)
        categoria = st.selectbox("Categoria:", CATEGORIAS)
        imagem_file = st.file_uploader("Foto do produto (PNG ou JPG)", type=["png", "jpg", "jpeg"])

        if st.button("Adicionar"):
            # Criar pasta automaticamente
            os.makedirs("imgs", exist_ok=True)

            # Salvar imagem enviada
            if imagem_file is not None:
                img_path = f"imgs/{imagem_file.name}"
                with open(img_path, "wb") as f:
                    f.write(imagem_file.getbuffer())
            else:
                img_path = "https://via.placeholder.com/200"

            novo_produto = {
                "nome": nome,
                "preco": preco,
                "estoque": estoque,
                "categoria": categoria,
                "img": img_path
            }

            st.session_state.produtos.append(novo_produto)
            salvar_produtos(st.session_state.produtos)

            st.success("Produto adicionado com sucesso!")

    else:
        st.warning("Digite a senha correta para editar produtos.")
