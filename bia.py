# app.py
import streamlit as st
import json
import os
import uuid
from datetime import datetime
import urllib.parse

# -----------------------
# Configurações / arquivos
# -----------------------
DB_FILE = "produtos.json"
IMAGES_DIR = "imgs"

# garante pastas/arquivos
os.makedirs(IMAGES_DIR, exist_ok=True)
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def carregar_produtos():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_produtos(produtos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=2)

def save_uploaded_image(uploaded_file):
    """Salva o arquivo upload em imgs/ com nome único e retorna o caminho relativo."""
    if uploaded_file is None:
        return None
    ext = os.path.splitext(uploaded_file.name)[1]
    fname = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(IMAGES_DIR, fname)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

# -----------------------
# Layout e estilo
# -----------------------
st.set_page_config(page_title="Kindness Knots", layout="wide")

st.markdown("""
<style>
/* Remove header/white top bar and footer */
header[data-testid="stHeader"] {height: 0; padding: 0; margin: 0; display: none;}
footer {visibility: hidden;}

/* Paleta pastel (sem laranja) */
body { background-color: #F4F1F5; }
h1, h2, h3, h4, h5, h6 { color: #7C6C8A; }
.product-card {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}
.stButton>button {
    background-color: #C9D7E8 !important;
    color: #000 !important;
    border-radius: 10px !important;
}
.sidebar .css-1d391kg { /* melhora visual da sidebar em alguns temas */
    background-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# Constants
# -----------------------
CATEGORIES = ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"]
INSTAGRAM_ACCOUNT = "kindnessknots"  # conta para DM

# -----------------------
# Estado inicial
# -----------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {product_id: qty}

produtos = carregar_produtos()

# -----------------------
# Detecta admin via query param ?admin=1
# -----------------------
is_admin = st.experimental_get_query_params().get("admin", ["0"])[0] == "1"

# -----------------------
# Cabeçalho
# -----------------------
st.title("🌸 Kindness Knots — Feito com carinho")

# -----------------------
# Sidebar (menu lateral)
# - se admin: mostra painel admin na sidebar
# - sempre: menu de categorias
# -----------------------
with st.sidebar:
    st.header("Menu")
    # categorias como radio vertical
    categoria_escolhida = st.radio("Categorias", options=CATEGORIES)

    st.markdown("---")
    st.write("🔍 Buscar (nome)")
    busca_text = st.text_input("Digite para buscar", value="")

    st.markdown("---")
    st.write("Carrinho:")
    # resumo do carrinho na sidebar
    if st.session_state.cart:
        total_cart = 0.0
        for pid, qty in st.session_state.cart.items():
            prod = next((p for p in produtos if p["id"] == pid), None)
            if prod:
                st.write(f"{qty}x {prod['nome']} — R$ {prod['preco'] * qty:.2f}")
                total_cart += prod['preco'] * qty
        st.write(f"**Total: R$ {total_cart:.2f}**")
        if st.button("Finalizar compra"):
            st.session_state.show_checkout = True
    else:
        st.info("Carrinho vazio")

    st.markdown("---")
    # admin info in sidebar only if admin
    if is_admin:
        st.success("🔐 Modo moderadora (link secreto)")
        st.markdown("### Painel rápido")
        if st.button("Recarregar produtos"):
            produtos = carregar_produtos()
            st.experimental_rerun()

# -----------------------
# Admin area (página principal) -> só aparece quando is_admin True
# -----------------------
if is_admin:
    st.header("📦 Painel da Moderadora — Gerenciar Produtos")
    with st.expander("Adicionar novo produto", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do produto", key="admin_name")
            preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f", key="admin_price")
            quantidade = st.number_input("Quantidade", min_value=0, step=1, key="admin_qty")
            categoria = st.selectbox("Categoria", CATEGORIES, key="admin_cat")
        with col2:
            descricao = st.text_area("Descrição (opcional)", key="admin_desc")
            imagem_file = st.file_uploader("Foto (png/jpg)", type=["png","jpg","jpeg"], key="admin_img")
        if st.button("Adicionar produto", key="btn_add"):
            if not nome:
                st.error("O produto precisa de um nome.")
            else:
                img_path = save_uploaded_image(imagem_file) if imagem_file else None
                novo = {
                    "id": str(uuid.uuid4()),
                    "nome": nome,
                    "preco": float(preco),
                    "quantidade": int(quantidade),
                    "categoria": categoria,
                    "descricao": descricao or "",
                    "img": img_path
                }
                produtos.append(novo)
                salvar_produtos(produtos)
                st.success("Produto adicionado!")
                st.experimental_rerun()

    st.markdown("---")
    st.subheader("Produtos cadastrados")
    if not produtos:
        st.info("Nenhum produto ainda.")
    else:
        # list with edit/delete controls
        for p in produtos:
            with st.container():
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1,3,1])
                with c1:
                    if p.get("img") and os.path.exists(p["img"]):
                        st.image(p["img"], width=120)
                    else:
                        st.image("https://via.placeholder.com/120", width=120)
                with c2:
                    st.markdown(f"**{p['nome']}**")
                    st.write(f"Categoria: {p['categoria']}")
                    st.write(f"Preço: R$ {p['preco']:.2f}")
                    st.write(f"Estoque: {p['quantidade']}")
                    if p.get("descricao"):
                        st.caption(p.get("descricao"))
                with c3:
                    if st.button("Editar", key=f"edit_{p['id']}"):
                        # abrir modal-like with expander fields (simple approach: use session_state to hold edit target)
                        st.session_state.edit_id = p["id"]
                        st.experimental_rerun()
                    if st.button("Excluir", key=f"del_{p['id']}"):
                        produtos = [x for x in produtos if x["id"] != p["id"]]
                        salvar_produtos(produtos)
                        st.success("Produto excluído.")
                        st.experimental_rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # edição simples fora da list
        if "edit_id" in st.session_state:
            edit_id = st.session_state.get("edit_id")
            prod = next((x for x in produtos if x["id"] == edit_id), None)
            if prod:
                st.markdown("---")
                st.subheader("Editar produto")
                e_col1, e_col2 = st.columns(2)
                with e_col1:
                    new_name = st.text_input("Nome", value=prod["nome"], key="e_name")
                    new_price = st.number_input("Preço (R$)", value=prod["preco"], format="%.2f", key="e_price")
                    new_qty = st.number_input("Quantidade", value=prod["quantidade"], min_value=0, step=1, key="e_qty")
                    new_cat = st.selectbox("Categoria", CATEGORIES, index=CATEGORIES.index(prod["categoria"]), key="e_cat")
                with e_col2:
                    new_desc = st.text_area("Descrição", value=prod.get("descricao",""), key="e_desc")
                    new_img = st.file_uploader("Substituir imagem (opcional)", type=["png","jpg","jpeg"], key="e_img")
                if st.button("Salvar alterações", key="e_save"):
                    prod["nome"] = new_name
                    prod["preco"] = float(new_price)
                    prod["quantidade"] = int(new_qty)
                    prod["categoria"] = new_cat
                    prod["descricao"] = new_desc
                    if new_img:
                        prod["img"] = save_uploaded_image(new_img)
                    salvar_produtos(produtos)
                    st.success("Produto atualizado.")
                    del st.session_state["edit_id"]
                    st.experimental_rerun()
                if st.button("Cancelar edição", key="e_cancel"):
                    del st.session_state["edit_id"]
                    st.experimental_rerun()

# -----------------------
# Public view (list products by selected category + search)
# -----------------------
if not is_admin:
    st.markdown("### ✨ Escolha uma categoria para ver os produtos artesanais")

    # filtro por busca
    all_products = carregar_produtos()
    # aplicar categoria e busca
    filtered = [p for p in all_products if p["categoria"] == categoria_escolhida]
    if busca_text:
        filtered = [p for p in filtered if busca_text.lower() in p["nome"].lower()]

    if not filtered:
        st.warning("Ainda não há produtos nessa categoria 💗")
    else:
        # expoe products grid
        cols = st.columns(3)
        for i, p in enumerate(filtered):
            col = cols[i % 3]
            with col:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                if p.get("img") and os.path.exists(p["img"]):
                    st.image(p["img"], use_column_width=True)
                else:
                    st.image("https://via.placeholder.com/300x200", use_column_width=True)
                st.subheader(p["nome"])
                st.write(f"R$ {p['preco']:.2f}")
                st.write(f"Disponíveis: {p['quantidade']}")
                qty = st.number_input("Qtd", min_value=1, max_value=p["quantidade"] if p["quantidade"]>0 else 1, value=1, key=f"qty_{p['id']}")
                if st.button("Adicionar ao carrinho", key=f"add_{p['id']}"):
                    # adiciona ao carrinho (somando)
                    cart = st.session_state.cart
                    if p["id"] in cart:
                        cart[p["id"]] += qty
                    else:
                        cart[p["id"]] = qty
                    st.session_state.cart = cart
                    st.success(f"{qty}x {p['nome']} adicionado ao carrinho")
                st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# Checkout modal-like (usando show_checkout flag na session_state)
# -----------------------
if st.session_state.get("show_checkout"):
    st.markdown("---")
    st.header("🏁 Finalizar pedido")
    cart = st.session_state.get("cart", {})
    if not cart:
        st.info("Seu carrinho está vazio.")
        st.session_state.show_checkout = False
    else:
        # mostrar itens
        st.subheader("Itens")
        total = 0.0
        for pid, qty in cart.items():
            prod = next((p for p in carregar_produtos() if p["id"] == pid), None)
            if prod:
                st.write(f"- {qty}x {prod['nome']} — R$ {prod['preco']:.2f} (subtotal R$ {prod['preco']*qty:.2f})")
                total += prod['preco'] * qty

        st.markdown(f"**Total: R$ {total:.2f}**")
        st.markdown("---")
        st.subheader("Dados para entrega")

        # dados do cliente
        nome_cliente = st.text_input("Nome completo")
        telefone = st.text_input("Telefone (com DDD)")
        endereco = st.text_area("Endereço completo (rua, número, cidade, CEP)")
        # forma de entrega: se Taubaté -> Uber Entrega, caso contrário Correios
        forma_entrega = st.selectbox("Forma de entrega", ["Uber Entrega (Taubaté)", "Correios (Outras cidades)"])

        st.markdown("Ao confirmar, você será redirecionado para enviar uma mensagem direta no Instagram para finalizar o pagamento e combinar entrega.")
        if st.button("📩 Confirmar e enviar pedido via Instagram"):
            # valida campos
            if not nome_cliente or not telefone or not endereco:
                st.error("Preencha nome, telefone e endereço antes de continuar.")
            else:
                # montar mensagem
                linhas = []
                linhas.append("Pedido - Kindness Knots")
                linhas.append(f"Forma de entrega: {forma_entrega}")
                linhas.append(f"Endereço: {endereco}")
                linhas.append(f"Nome da pessoa: {nome_cliente}")
                linhas.append(f"Telefone: {telefone}")
                linhas.append("")
                linhas.append("Itens:")
                for pid, qty in cart.items():
                    prod = next((p for p in carregar_produtos() if p["id"] == pid), None)
                    if prod:
                        linhas.append(f"- {qty}x {prod['nome']} — R$ {prod['preco']:.2f}")

                linhas.append(f"Total: R$ {total:.2f}")
                texto = "\n".join(linhas)

                # codificar para URL
                texto_cod = urllib.parse.quote_plus(texto)

                # montar link para DM (tentativa via direct new). Se não funcionar em alguns navegadores, o usuário será direcionado para o perfil.
                dm_link = f"https://www.instagram.com/direct/new/?text={texto_cod}"
                perfil_link = f"https://www.instagram.com/{INSTAGRAM_ACCOUNT}"

                # exibir link e instrução
                st.success("Quase pronto — abrindo o Instagram...")
                st.markdown(f"[Abrir DM no Instagram]({dm_link})")
                st.markdown(f"Ou abrir perfil: [@{INSTAGRAM_ACCOUNT}]({perfil_link})")
                # opcional: esvaziar carrinho
                st.session_state.cart = {}
                st.session_state.show_checkout = False

# -----------------------
# botão para abrir checkout também no corpo (caso não use sidebar)
# -----------------------
if not st.session_state.get("show_checkout") and not is_admin:
    if st.button("Ver carrinho / Finalizar pedido"):
        st.session_state.show_checkout = True
        st.experimental_rerun()

