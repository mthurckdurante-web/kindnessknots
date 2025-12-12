import streamlit as st
import pandas as pd
import webbrowser

# Carregar produtos
try:
    produtos_df = pd.read_csv("produtos.csv")
except:
    st.warning("Nenhum produto disponível no momento.")
    produtos_df = pd.DataFrame(columns=["nome", "categoria", "preco", "imagem"])

st.title("Kindness Knots - Loja")

# Selecionar categoria
categoria_selecionada = st.selectbox("Escolha a categoria", ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"])
produtos_categoria = produtos_df[produtos_df["categoria"] == categoria_selecionada]

for i, produto in produtos_categoria.iterrows():
    st.subheader(produto["nome"])
    st.image(produto["imagem"], width=200)
    st.write(f"Preço: R${produto['preco']}")
    
    if st.button(f"Comprar {produto['nome']}", key=f"btn_{i}"):
        with st.form(key=f"form_{i}"):
            st.write("Finalize sua compra:")
            nome_cliente = st.text_input("Seu nome")
            telefone = st.text_input("Telefone")
            endereco = st.text_area("Endereço")
            cidade = st.text_input("Cidade")
            
            # Modo de entrega automático
            modo_entrega = "Uber Entrega" if cidade.strip().lower() == "taubate" else "Correios"
            
            submit = st.form_submit_button("Finalizar Compra")
            if submit:
                mensagem = (
                    f"Olá! Gostaria de comprar:\n"
                    f"Produto: {produto['nome']}\n"
                    f"Nome: {nome_cliente}\n"
                    f"Telefone: {telefone}\n"
                    f"Endereço: {endereco}\n"
                    f"Modo de Entrega: {modo_entrega}"
                )
                url = f"https://www.instagram.com/direct/inbox/"
                st.success("Clique no botão abaixo para enviar a mensagem via DM do Instagram.")
                st.markdown(f"[Abrir DM no Instagram]({url})", unsafe_allow_html=True)
