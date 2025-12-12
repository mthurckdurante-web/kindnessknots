<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Kindness Knots</title>
<style>
:root{
  --bg: #F4F1F5;
  --card:#FFFFFF;
  --muted:#9AA5A8;
  --accent:#C9D7E8;
  --accent-2:#EDE6F6;
  --text:#4A2D33;
}
*{box-sizing:border-box}
body{margin:0;font-family:Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;background:var(--bg);color:var(--text)}
header{background:transparent;padding:18px 20px;text-align:center}
.container{max-width:1100px;margin:18px auto;padding:0 16px}
.layout{display:flex;gap:20px}
.sidebar{width:260px;padding:18px;background:transparent}
.main{flex:1}
.section-title{font-weight:600;color:#6C778C;margin-bottom:12px}
.card{background:var(--card);border-radius:12px;padding:14px;box-shadow:0 6px 18px rgba(0,0,0,0.06);margin-bottom:16px}
.prod-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
img.prod{width:100%;border-radius:8px;height:180px;object-fit:cover}
.btn{background:var(--accent);border:none;padding:10px 12px;border-radius:10px;cursor:pointer}
.btn-ghost{background:transparent;border:1px solid #ddd;padding:8px;border-radius:8px;cursor:pointer}
.cart-float{position:fixed;right:18px;bottom:18px;background:var(--accent);padding:12px 16px;border-radius:999px;box-shadow:0 6px 18px rgba(0,0,0,0.12);cursor:pointer}
.modal{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);background:white;padding:20px;border-radius:12px;box-shadow:0 12px 40px rgba(0,0,0,0.2);z-index:9999;max-width:480px;width:94%;display:none}
.modal.open{display:block}
.input,textarea,select{width:100%;padding:10px;border-radius:8px;border:1px solid #ddd;margin-top:8px}
.small{font-size:14px;color:#666;margin-top:8px}
.footer{padding:24px;text-align:center;color:#777}
</style>
</head>
<body>
<header>
  <h1>🌸 Kindness Knots</h1>
  <div class="small">Feito com carinho — artesanato, chaveiros, broches, pelúcias e amigurumis</div>
</header>

<div class="container">
  <div class="layout">
    <aside class="sidebar">
      <div class="card">
        <div class="section-title">Categorias</div>
        <div id="categories"></div>
      </div>

      <div class="card" style="margin-top:12px">
        <div class="section-title">Buscar</div>
        <input id="search" class="input" placeholder="Digite o nome do produto..." />
      </div>

      <div class="card" style="margin-top:12px">
        <div class="section-title">Carrinho</div>
        <div id="mini-cart">Nenhum item</div>
        <div style="margin-top:10px">
          <button class="btn" id="open-checkout">Ver / Finalizar</button>
        </div>
      </div>

      <div style="height:16px"></div>
      <div class="small">Moderadora? <a href="./admin.html" target="_blank">Painel</a> (link secreto/privado)</div>
    </aside>

    <main class="main">
      <div id="products-container" class="prod-grid"></div>
    </main>
  </div>
</div>

<button class="cart-float" id="cart-open">🛒 Carrinho</button>

<!-- Modal de checkout -->
<div id="checkout-modal" class="modal" role="dialog" aria-modal="true">
  <h3>Finalizar pedido</h3>
  <div id="checkout-items" style="max-height:180px;overflow:auto;margin-bottom:10px"></div>
  <div><strong>Total: R$ <span id="checkout-total">0.00</span></strong></div>
  <hr>
  <label>Forma de entrega</label>
  <select id="delivery" class="input">
    <option>Uber Entrega (Taubaté)</option>
    <option>Correios (Outras cidades)</option>
  </select>
  <label>Endereço</label>
  <textarea id="address" class="input" rows="2"></textarea>
  <label>Nome completo</label>
  <input id="customer-name" class="input" />
  <label>Telefone (com DDD)</label>
  <input id="customer-phone" class="input" />
  <div style="margin-top:12px;display:flex;gap:8px">
    <button class="btn" id="confirm-order">📩 Enviar pedido pelo Instagram</button>
    <button class="btn-ghost" id="checkout-close">Cancelar</button>
  </div>
</div>

<div id="toast" style="position:fixed;left:50%;transform:translateX(-50%);bottom:24px;background:#222;color:#fff;padding:10px 14px;border-radius:8px;display:none"></div>

<footer class="footer">© Kindness Knots</footer>

<script>
/* ---------- utilidades ---------- */
const INSTAGRAM_ACCOUNT = "kindnessknots";
function showToast(t){const e=document.getElementById('toast');e.innerText=t;e.style.display='block';setTimeout(()=>e.style.display='none',2500);}
function uid(){return '_' + Math.random().toString(36).substr(2,9);}

/* ---------- produtos: carregar de localStorage ---------- */
const STORAGE_KEY = 'kk_products_v1';

function defaultProducts(){
  return [
    {id:uid(), nome:"Chaveiro Tartaruga", preco:15.00, quantidade:10, categoria:"Chaveiros", img:"https://i.imgur.com/hiP2AKb.png"},
    {id:uid(), nome:"Broche Gatinho", preco:12.00, quantidade:8, categoria:"Broches", img:"https://i.imgur.com/2JYMGbc.png"},
    {id:uid(), nome:"Pelúcia Ursinho", preco:45.00, quantidade:3, categoria:"Pelúcias", img:"https://i.imgur.com/fcUuG4L.png"}
  ];
}

function loadProducts(){
  const raw = localStorage.getItem(STORAGE_KEY);
  if(!raw) return defaultProducts();
  try{ return JSON.parse(raw);}catch(e){return defaultProducts();}
}

function saveProducts(list){ localStorage.setItem(STORAGE_KEY, JSON.stringify(list)); }

/* ---------- UI e lógica de catálogo ---------- */
let products = loadProducts();
let categories = ["Chaveiros","Broches","Pelúcias","Amigurumis"];
let currentCategory = categories[0];

const productsContainer = document.getElementById('products-container');
const categoriesDiv = document.getElementById('categories');
const searchInput = document.getElementById('search');

function renderCategories(){
  categoriesDiv.innerHTML = '';
  categories.forEach(cat=>{
    const b = document.createElement('button');
    b.className='btn-ghost';
    b.style.width='100%';
    b.style.textAlign='left';
    b.style.marginBottom='8px';
    b.innerText= (cat==='Chaveiros'?'🔑 ':'') + (cat==='Broches'?'🌸 ':'') + (cat==='Pelúcias'?'🧸 ':'') + (cat==='Amigurumis'?'🧶 ':'') + cat;
    b.onclick = ()=>{ currentCategory=cat; renderProducts(); }
    categoriesDiv.appendChild(b);
  });
}

function filteredProducts(){
  const q = searchInput.value.trim().toLowerCase();
  return products.filter(p => p.categoria === currentCategory && (!q || p.nome.toLowerCase().includes(q)));
}

function renderProducts(){
  productsContainer.innerHTML = '';
  const list = filteredProducts();
  if(list.length===0){
    productsContainer.innerHTML = '<div class="card">Nenhum produto nessa categoria.</div>';
    return;
  }
  list.forEach(p=>{
    const el = document.createElement('div');
    el.className='card';
    el.innerHTML = `
      <img class="prod" src="${p.img}" alt="${p.nome}" />
      <h4>${p.nome}</h4>
      <div class="small">R$ ${Number(p.preco).toFixed(2)}</div>
      <div style="margin-top:8px;display:flex;gap:8px;align-items:center">
        <input id="qty_${p.id}" type="number" min="1" max="${Math.max(1,p.quantidade)}" value="1" style="width:70px;padding:6px;border-radius:8px;border:1px solid #ddd" />
        <button class="btn" data-id="${p.id}">Adicionar ao carrinho</button>
      </div>
    `;
    productsContainer.appendChild(el);
  });
  // attach listeners
  document.querySelectorAll('.btn[data-id]').forEach(btn=>{
    btn.onclick = ()=> {
      const id = btn.getAttribute('data-id');
      const q = Number(document.getElementById('qty_'+id).value || 1);
      addToCart(id,q);
    }
  });
  updateMiniCart();
}

/* ---------- carrinho ---------- */
const CART_KEY = 'kk_cart_v1';
let cart = JSON.parse(localStorage.getItem(CART_KEY)||'{}'); // {id:qty}

function addToCart(id,qty){
  cart[id] = (cart[id]||0) + qty;
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  showToast('Adicionado ao carrinho');
  updateMiniCart();
}

function updateMiniCart(){
  const el = document.getElementById('mini-cart');
  const ids = Object.keys(cart);
  if(ids.length===0){ el.innerHTML='Nenhum item'; return; }
  let html='';
  let total=0;
  ids.forEach(id=>{
    const prod = products.find(p=>p.id===id);
    if(!prod) return;
    const q = cart[id];
    total += prod.preco*q;
    html += `<div>${q}x ${prod.nome} — R$ ${(prod.preco*q).toFixed(2)}</div>`;
  });
  html += `<div style="margin-top:8px"><strong>Total: R$ ${total.toFixed(2)}</strong></div>`;
  el.innerHTML = html;
}

/* ---------- checkout ---------- */
const cartOpenBtn = document.getElementById('cart-open');
const checkoutModal = document.getElementById('checkout-modal');
const checkoutItems = document.getElementById('checkout-items');
const checkoutTotal = document.getElementById('checkout-total');

function openCheckout(){
  renderCheckoutItems();
  checkoutModal.classList.add('open');
}
function closeCheckout(){ checkoutModal.classList.remove('open'); }

cartOpenBtn.onclick = ()=> openCheckout();
document.getElementById('open-checkout').onclick = ()=> openCheckout();
document.getElementById('checkout-close').onclick = ()=> closeCheckout();

function renderCheckoutItems(){
  checkoutItems.innerHTML = '';
  let total=0;
  const ids = Object.keys(cart);
  if(ids.length===0){
    checkoutItems.innerHTML = '<div>Nenhum item no carrinho.</div>';
  } else {
    ids.forEach(id=>{
      const p = products.find(x=>x.id===id);
      if(!p) return;
      const q = cart[id];
      total += p.preco*q;
      const d = document.createElement('div');
      d.innerHTML = `${q}x ${p.nome} — R$ ${(p.preco*q).toFixed(2)} <button style="margin-left:8px" data-rem="${id}">Remover</button>`;
      checkoutItems.appendChild(d);
    });
    // attach remover
    checkoutItems.querySelectorAll('button[data-rem]').forEach(bt=>{
      bt.onclick = ()=> { delete cart[bt.getAttribute('data-rem')]; localStorage.setItem(CART_KEY, JSON.stringify(cart)); renderCheckoutItems(); updateMiniCart();}
    });
  }
  checkoutTotal.innerText = total.toFixed(2);
}

/* ---------- confirm order -> redirect to Instagram DM (prefilled) ---------- */
document.getElementById('confirm-order').onclick = ()=>{
  const name = document.getElementById('customer-name').value.trim();
  const phone = document.getElementById('customer-phone').value.trim();
  const address = document.getElementById('address').value.trim();
  const delivery = document.getElementById('delivery').value;

  if(!name || !phone || !address){ showToast('Preencha nome, telefone e endereço'); return; }
  const ids = Object.keys(cart);
  if(ids.length===0){ showToast('Carrinho vazio'); return; }

  let lines = [];
  lines.push('Pedido - Kindness Knots');
  lines.push('Forma de entrega: ' + delivery);
  lines.push('Endereço: ' + address);
  lines.push('Nome da pessoa: ' + name);
  lines.push('Telefone: ' + phone);
  lines.push('');
  lines.push('Itens:');
  let total=0;
  ids.forEach(id=>{
    const p = products.find(x=>x.id===id);
    const q = cart[id];
    if(p){ lines.push(`- ${q}x ${p.nome} — R$ ${p.preco.toFixed(2)}`); total += p.preco*q; }
  });
  lines.push(`Total: R$ ${total.toFixed(2)}`);

  const text = lines.join('\n');
  const encoded = encodeURIComponent(text);

  // Try DM new link (may require login); fallback to profile link
  const dm = `https://www.instagram.com/direct/new/?text=${encoded}`;
  const profile = `https://www.instagram.com/${INSTAGRAM_ACCOUNT}/?utm_source=kk`;

  // open dm in new tab
  window.open(dm, '_blank');
  // also open profile as fallback after short delay
  setTimeout(()=>window.open(profile, '_blank'), 800);

  // clear cart
  cart = {};
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  updateMiniCart();
  closeCheckout();
  showToast('Redirecionando para o Instagram...');
}

/* ---------- admin sync helpers: if localStorage is updated by admin.html, reflect here ---------- */
window.addEventListener('storage', (e)=>{
  if(e.key === STORAGE_KEY){
    products = loadProducts();
    renderProducts();
    updateMiniCart();
  }
});

/* ---------- init ---------- */
renderCategories();
renderProducts();
updateMiniCart();
</script>

</body>
</html>
