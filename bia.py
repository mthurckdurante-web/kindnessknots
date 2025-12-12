import streamlit as st
import pandas as pd
import urllib.parse

# Inicializar carrinho
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# Carregar produtos
try:
    produtos_df = pd.read_csv("produtos.csv")
except:
    st.warning("Nenhum produto disponível no momento.")
    produtos_df = pd.DataFrame(columns=["nome", "categoria", "preco", "imagem"])

st.title("Kindness Knots - Loja")

# -------------------------------
# Barra lateral: navegação
# -------------------------------
st.sidebar.header("Seções")
secao = st.sidebar.radio("Escolha a seção", ["Chaveiros", "Broches", "Pelúcias", "Amigurumis", "Carrinho"])

# -------------------------------
# Mostrar produtos de acordo com a seção
# -------------------------------
if secao != "Carrinho":
    st.subheader(secao)
    produtos_categoria = produtos_df[produtos_df["categoria"] == secao]
    
    for i, produto in produtos_categoria.iterrows():
        st.image(produto["imagem"], width=200)
        st.write(f"**{produto['nome']}**")
        st.write(f"Preço: R${produto['preco']}")
        
        if st.button(f"Adicionar ao carrinho - {produto['nome']}", key=f"add_{i}"):
            st.session_state.carrinho.append(produto.to_dict())
            st.success(f"{produto['nome']} adicionado ao carrinho!")

# -------------------------------
# Carrinho de compras
# -------------------------------
if secao == "Carrinho":
    st.subheader("🛒 Seu Carrinho")
    if len(st.session_state.carrinho) == 0:
        st.info("Seu carrinho está vazio.")
    else:
        total = 0
        for i, item in enumerate(st.session_state.carrinho):
            st.write(f"**{item['nome']}** - R${item['preco']}")
            total += float(item['preco'])
        
        st.markdown(f"**Total: R${total:.2f}**")
        
        # Finalizar compra
        if st.button("Finalizar Compra"):
            with st.form(key="form_carrinho"):
                st.write("Preencha seus dados para a compra:")
                nome_cliente = st.text_input("Nome")
                telefone = st.text_input("Telefone")
                endereco = st.text_area("Endereço")
                cidade = st.text_input("Cidade")
                
                # Modo de entrega automático
                modo_entrega = "Uber Entrega" if cidade.strip().lower() == "taubate" else "Correios"
                
                submit = st.form_submit_button("Enviar pedido para Instagram DM")
                
                if submit:
                    # Montar mensagem
                    mensagem = f"Olá! Gostaria de comprar:\n"
                    for item in st.session_state.carrinho:
                        mensagem += f"- {item['nome']} (R${item['preco']})\n"
                    mensagem += (
                        f"Nome: {nome_cliente}\n"
                        f"Telefone: {telefone}\n"
                        f"Endereço: {endereco}\n"
                        f"Modo de Entrega: {modo_entrega}"
                    )
                    mensagem_url = urllib.parse.quote(mensagem)
                    instagram_user = "kindnessknots"
                    url = f"https://www.instagram.com/{instagram_user}/"
                    
                    st.success("Clique no botão abaixo para enviar sua mensagem via DM do Instagram:")
                    st.markdown(f"[Abrir Instagram]({url})", unsafe_allow_html=True)
                    st.info("Copie a mensagem abaixo e envie pelo DM:")
                    st.code(mensagem)
