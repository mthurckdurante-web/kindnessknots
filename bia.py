<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Kindness Knots</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
    :root {
        --rosa1: #ffdce5;
        --rosa2: #ffb7c8;
        --rosa3: #ff8fab;
        --rosa4: #ff6b95;
        --texto: #4a2d33;
    }

    body {
        margin: 0;
        font-family: "Poppins", sans-serif;
        background: var(--rosa1);
        color: var(--texto);
    }

    header {
        background: var(--rosa3);
        padding: 20px;
        text-align: center;
        color: white;
        font-size: 30px;
        font-weight: bold;
    }

    .produtos {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 20px;
        padding: 25px;
    }

    .card {
        background: white;
        padding: 15px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 12px #00000030;
    }

    .card img {
        width: 100%;
        border-radius: 15px;
    }

    button {
        background: var(--rosa4);
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 12px;
        cursor: pointer;
        font-size: 16px;
        margin-top: 10px;
        width: 100%;
    }

    button:hover {
        background: var(--rosa3);
    }

    #carrinhoBtn {
        position: fixed;
        right: 20px;
        bottom: 20px;
        background: var(--rosa4);
        padding: 15px 22px;
        font-size: 18px;
        border-radius: 50px;
        z-index: 999;
    }

    #carrinho {
        background: white;
        padding: 25px;
        border-radius: 20px;
        width: 90%;
        max-width: 450px;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        box-shadow: 0 4px 18px #00000050;
        display: none;
        z-index: 9999;
    }

    input, select {
        width: 100%;
        padding: 10px;
        margin-top: 7px;
        border-radius: 10px;
        border: 1px solid #bbb;
        font-size: 15px;
    }
</style>
</head>

<body>

<header>Kindness Knots</header>

<!-- PRODUTOS -->
<div class="produtos" id="listaProdutos">
    <!-- Exemplo de produto -->
</div>

<button id="carrinhoBtn" onclick="abrirCarrinho()">🛒 Carrinho</button>

<!-- CARRINHO POP-UP -->
<div id="carrinho">
    <h2>Seu Pedido</h2>
    <div id="itensCarrinho"></div>
    <hr>

    <h3>Finalizar Pedido</h3>

    <label>Nome:</label>
    <input id="nome">

    <label>Telefone:</label>
    <input id="telefone">

    <label>Endereço:</label>
    <input id="endereco">

    <label>Método de Entrega:</label>
    <select id="entrega">
        <option value="Uber (Taubaté)">Uber (Taubaté)</option>
        <option value="Correios (outra cidade)">Correios (outra cidade)</option>
    </select>

    <br><br>
    <button onclick="finalizarCompra()">Enviar Pedido</button>
    <button onclick="fecharCarrinho()" style="background:#999;margin-top:10px;">Fechar</button>
</div>

<script>
const produtos = [
    {nome: "Chaveiro Tartaruga", preco: 15, img:"https://i.imgur.com/hiP2AKb.png"},
    {nome: "Chaveiro Coração", preco: 12, img:"https://i.imgur.com/2JYMGbc.png"},
    {nome: "Polvinho Reversível", preco: 25, img:"https://i.imgur.com/fcUuG4L.png"},
];

let carrinho = [];

function carregarProdutos() {
    let area = document.getElementById("listaProdutos");
    produtos.forEach((p, i) => {
        area.innerHTML += `
            <div class="card">
                <img src="${p.img}">
                <h3>${p.nome}</h3>
                <p>R$ ${p.preco},00</p>
                <button onclick="addCarrinho(${i})">Adicionar</button>
            </div>
        `;
    });
}

function addCarrinho(i) {
    let item = produtos[i];
    let existente = carrinho.find(c => c.nome === item.nome);

    if (existente) existente.qtd++;
    else carrinho.push({...item, qtd: 1});

    alert("Adicionado ao carrinho!");
}

function abrirCarrinho() {
    atualizarCarrinho();
    document.getElementById("carrinho").style.display = "block";
}

function fecharCarrinho() {
    document.getElementById("carrinho").style.display = "none";
}

function atualizarCarrinho() {
    let area = document.getElementById("itensCarrinho");
    area.innerHTML = "";

    carrinho.forEach((item, i) => {
        area.innerHTML += `
            <p>
                ${item.nome} — R$${item.preco} x 
                <input type="number" min="1" value="${item.qtd}" 
                style="width:60px" onchange="mudarQtd(${i}, this.value)">
            </p>
        `;
    });
}

function mudarQtd(i, v) {
    carrinho[i].qtd = Number(v);
}

function finalizarCompra() {
    if (carrinho.length === 0) return alert("Carrinho vazio!");

    let nome = document.getElementById("nome").value;
    let tel = document.getElementById("telefone").value;
    let end = document.getElementById("endereco").value;
    let entrega = document.getElementById("entrega").value;

    if (!nome || !tel || !end) return alert("Preencha todos os campos!");

    let resumo = carrinho.map(item => 
        `${item.qtd}x ${item.nome} — R$${item.preco * item.qtd}`
    ).join("%0A");

    let msg =
`Pedido - Kindness Knots
Forma de entrega: ${entrega}
Endereço: ${end}
Nome: ${nome}
Telefone: ${tel}

Itens:
${resumo}`;

    let url = "https://instagram.com/kindnessknots?x=" + encodeURIComponent(msg);

    window.location.href = url;
}

carregarProdutos();
</script>

</body>
</html>
