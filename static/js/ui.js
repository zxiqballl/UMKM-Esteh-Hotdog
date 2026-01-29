document.addEventListener('DOMContentLoaded',()=>{
    window.cart = JSON.parse(localStorage.getItem('cart')||'[]');
    renderCart();
});

function addToCart(p){
    const existing = window.cart.find(i=>i.id==p.id);
    if(existing) existing.qty++;
    else window.cart.push({...p, qty:1});
    localStorage.setItem('cart',JSON.stringify(window.cart));
    renderCart();
    showToast('Produk ditambahkan ke keranjang');
}

function renderCart(){
    const el = document.getElementById('cart-items');
    const totalEl = document.getElementById('cart-total');
    if(!el) return;
    el.innerHTML = '';
    if(window.cart.length===0){ el.innerHTML = '<div class="muted">Keranjang kosong</div>'; totalEl.textContent='Rp 0'; return; }
    let total=0;
    window.cart.forEach(item=>{
        const row = document.createElement('div'); row.className='cart-row';
        const left = document.createElement('div'); left.innerHTML=`<div style="font-weight:600">${item.name}</div><div class='muted'>Rp ${item.price}</div>`;
        const right = document.createElement('div');
        right.innerHTML = `<div style='display:flex;gap:8px;align-items:center'>
            <button class='btn btn-ghost' onclick='changeQty(${item.id}, -1)'>-</button>
            <div>${item.qty}</div>
            <button class='btn btn-ghost' onclick='changeQty(${item.id}, 1)'>+</button>
            <button class='btn btn-danger' onclick='removeFromCart(${item.id})'>Hapus</button>
        </div>`;
        row.appendChild(left); row.appendChild(right); el.appendChild(row);
        total += (Number(item.price)||0) * item.qty;
    });
    totalEl.textContent = 'Rp ' + total;
}

function changeQty(id, delta){
    const it = window.cart.find(i=>i.id==id); if(!it) return;
    it.qty += delta; if(it.qty<=0) window.cart = window.cart.filter(i=>i.id!=id);
    localStorage.setItem('cart',JSON.stringify(window.cart)); renderCart();
}

function removeFromCart(id){ window.cart = window.cart.filter(i=>i.id!=id); localStorage.setItem('cart',JSON.stringify(window.cart)); renderCart(); }

function clearCart(){ window.cart=[]; localStorage.setItem('cart',JSON.stringify(window.cart)); renderCart(); showToast('Keranjang dibersihkan'); }

function checkout(){
    if(!window.cart || window.cart.length===0){ showToast('Keranjang kosong', 'danger'); return; }
    // Placeholder: implement server checkout in backend integration
    showToast('Transaksi selesai', 'success');
    clearCart();
}

function searchProducts(q){
    q = q.trim().toLowerCase();
    document.querySelectorAll('#products .product').forEach(card=>{
        const title = card.querySelector('.title').textContent.toLowerCase();
        card.style.display = title.includes(q)?'block':'none';
    });
}

function filterStock(q){
    q = q.trim().toLowerCase();
    document.querySelectorAll('#stok-table tr').forEach(row=>{
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(q)?'table-row':'none';
    });
}

function editStock(item){
    const name = prompt('Nama produk', item.name);
    const qty = prompt('Jumlah stok', item.qty);
    // Real app should POST this change to server
    showToast('Fitur edit stok sementara (simpan di server)', 'muted');
}

function showAddStock(){
    const name = prompt('Nama produk baru'); if(!name) return;
    const sku = prompt('SKU produk'); const qty = prompt('Jumlah awal', '0');
    showToast('Tambah stok: ' + name, 'success');
}

function showToast(message, type='primary'){
    const t = document.createElement('div');
    t.textContent = message; t.style.position='fixed'; t.style.right='20px'; t.style.bottom='20px'; t.style.padding='10px 14px'; t.style.borderRadius='8px';
    t.style.background = type==='danger'? 'rgba(239,68,68,0.9)' : type==='success'? 'rgba(16,185,129,0.9)' : 'rgba(6,182,212,0.95)';
    t.style.color='white'; t.style.boxShadow='0 6px 18px rgba(2,6,23,0.12)'; t.style.zIndex=9999;
    document.body.appendChild(t);
    setTimeout(()=>{ t.style.opacity='0'; setTimeout(()=>t.remove(),400); },2000);
}
