import streamlit as st
import json
import os
from datetime import datetime

# -------------------------
# ARQUIVO DO BANCO DE DADOS
# -------------------------
DB_FILE = "produtos.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

def carregar_produtos():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def salvar_produtos(produtos):
    with open(DB_FILE, "w") as f:
        json.dump(produtos, f, indent=4)


# -------------------------
# CONFIG DO SITE
# -------------------------
st.set_page_config(page_title="Kindness Knots", layout="wide")

# PALETA DE CORES PASTÉIS (SEM LARANJA)
st.markdown("""
<style>
body { background-color: #F4F1F5; }
header { background-color: #F4F1F5 !important; }

h1, h2, h3, h4, h5, h6 {
    color: #7C6C8A;
}

.product-card {
    background-color: #FFFFFF;
    border-radius: 15px;
    padding: 18px;
    box-shadow: 0 0 10px rgba(0,0,0,0.07);
    margin-bottom: 20px;
}

.stButton > button {
    background-color: #C9D7E8 !important;
    color: black !important;
    border-radius: 10px !important;
    padding: 6px 14px;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #6C778C;
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# VERIFICAÇÃO DO LINK SECRETO DE ADMIN
# -------------------------
is_admin = st.query_params.get("admin") == "1"

produtos = carregar_produtos()

# -------------------------
# CABEÇALHO
# -------------------------
st.title("🌸 Kindness Knots — Feito com carinho")


# =========================
#       ÁREA ADMIN
# Só aparece com ?admin=1
# =========================
if is_admin:

    st.sidebar.title("🔐 Painel da Moderadora (Acesso Secreto)")
    st.sidebar.success("Você entrou pelo link especial!")

    st.header("📦 Adicionar Produto")

    nome = st.text_input("Nome do produto")
    preco = st.number_input("Preço (R$)", min_value=0.0, step=0.5)
    quantidade = st.number_input("Quantidade disponível", min_value=0, step=1)

    categoria = st.selectbox(
        "Categoria",
        ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"]
    )

    foto = st.file_uploader("Foto do produto", type=["png", "jpg", "jpeg"])

    if st.button("Adicionar Produto"):
        if nome and preco and quantidade >= 0 and foto:
            bytes_foto = foto.read()

            produtos.append({
                "id": len(produtos) + 1,
                "nome": nome,
                "preco": preco,
                "quantidade": quantidade,
                "categoria": categoria,
                "foto": bytes_foto.hex()
            })

            salvar_produtos(produtos)
            st.success("Produto adicionado com sucesso!")
        else:
            st.error("Preencha todos os campos corretamente.")

    st.header("🗑 Remover Produto")

    nomes = [p["nome"] for p in produtos]
    if nomes:
        escolha = st.selectbox("Escolha o produto", nomes)
        if st.button("Remover"):
            produtos = [p for p in produtos if p["nome"] != escolha]
            salvar_produtos(produtos)
            st.success("Produto removido!")
    else:
        st.info("Nenhum produto cadastrado ainda.")



# =========================
#   ÁREA PÚBLICA DO SITE
# =========================
else:

    st.subheader("✨ Escolha uma categoria para ver os produtos artesanais")

    categoria_escolhida = st.selectbox(
        "Categorias:",
        ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"]
    )

    produtos_categoria = [
        p for p in produtos if p["categoria"] == categoria_escolhida
    ]

    if not produtos_categoria:
        st.warning("Ainda não há produtos nessa categoria 💗")
    else:
        for p in produtos_categoria:

            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(bytes.fromhex(p["foto"]), width=180)

            with col2:
                st.subheader(p["nome"])
                st.write(f"Preço: **R$ {p['preco']}**")
                st.write(f"Disponíveis: {p['quantidade']}")

                if st.button(f"Encomendar {p['nome']}", key=p["id"]):
                    st.success("✨ Encomenda iniciada!")

                    st.write("### 📄 Resumo da Encomenda")
                    st.write(f"**Produto:** {p['nome']}")
                    st.write(f"**Preço:** R$ {p['preco']}")
                    st.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

                    st.write("---")
                    st.write("💬 **Para finalizar a compra:**")
                    st.markdown("Instagram: [@KindnessKnots](https://instagram.com/) 💗")

            st.markdown('</div>', unsafe_allow_html=True)
