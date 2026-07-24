const API_URL = 'http://127.0.0.1:8000/api/'; 
let cart = []; 
let currentCategory = 'all';

async function switchCategory(catId, titleText) {
    currentCategory = catId;
    document.getElementById('sectionTitle').innerText = titleText;
    document.querySelectorAll('.cat-btn').forEach(btn => {
        btn.className = 'cat-btn px-5 py-2.5 rounded-xl font-extrabold text-sm bg-zinc-900 text-zinc-300 border border-zinc-800 hover:border-orange-500 transition';
    });
    if(event && event.target) {
        event.target.className = 'cat-btn px-5 py-2.5 rounded-xl font-extrabold text-sm bg-orange-600 text-white shadow-md transition';
    }
    fetchProducts();
}

async function fetchProducts() { 
    try { 
        const res = await fetch(API_URL + 'shop/products/'); 
        let products = await res.json(); 
        
        if (currentCategory !== 'all') {
            products = products.filter(p => p.category === currentCategory);
        }

        const container = document.getElementById('productList'); 
        container.innerHTML = ''; 
        
        if (products.length === 0) {
            container.innerHTML = '<p class=\'col-span-4 text-center text-zinc-500 py-12 font-medium\'>У цьому розділі поки немає товарів</p>';
            return;
        }

        products.forEach(function(product) { 
            const card = document.createElement('div'); 
            card.className = 'product-card overflow-hidden flex flex-col justify-between group'; 
            const imgSrc = product.image ? product.image : 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&auto=format&fit=crop&q=80';
            
            card.innerHTML = '<div class=\'relative h-72 bg-zinc-950 overflow-hidden\'>' +
                '<img src=\'' + imgSrc + '\' class=\'w-full h-full object-cover group-hover:scale-105 transition duration-500\'>' +
                '<span class=\'absolute top-4 left-4 bg-orange-600 text-white text-xs px-3 py-1 rounded-full font-black uppercase tracking-wider\'>POTUZHNO</span>' +
                '</div>' + 
                '<div class=\'p-6 flex flex-col flex-grow justify-between\'>' + 
                '<div>' +
                '<h4 class=\'font-black text-lg mb-2 text-white\'>' + product.name + '</h4>' + 
                '<p class=\'text-zinc-400 text-xs mb-4 line-clamp-2\'>' + (product.description || 'Преміум якість.') + '</p>' +
                '</div>' +
                '<div>' +
                '<div class=\'flex items-center justify-between mb-4\'>' +
                '<span class=\'text-orange-500 font-black text-xl\'>' + product.price + ' грн</span>' + 
                '<span class=\'text-xs bg-emerald-500/10 text-emerald-400 px-2 py-1 rounded font-bold\'>В наявності</span>' +
                '</div>' +
                '<button onclick=\'addToCart(' + product.id + ', \'' + product.name + '\', ' + product.price + ')\' class=\'w-full bg-zinc-800 text-white py-3 rounded-xl font-extrabold hover:bg-orange-600 transition shadow-md\'>Купити</button>' + 
                '</div>' +
                '</div>'; 
            container.appendChild(card); 
        }); 
    } catch (error) { 
        console.error('Помилка завантаження товарів:', error); 
    } 
} 

function loginWithGoogle() {
    const user = { name: 'Олена Потужна', role: 'Адміністратор', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80' };
    document.getElementById('userNameText').innerText = user.name;
    const av = document.getElementById('userAvatar'); av.src = user.avatar; av.classList.remove('hidden');
    const btn = document.getElementById('googleAuthBtn'); btn.innerText = 'Вийти'; btn.setAttribute('onclick', 'logout()');
    alert('Вхід через Google успішний!');
}

function logout() {
    document.getElementById('userNameText').innerText = 'Гість';
    document.getElementById('userAvatar').classList.add('hidden');
    const btn = document.getElementById('googleAuthBtn'); btn.innerHTML = '<i class=\'fa-brands fa-google text-red-400\'></i> Вхід'; btn.setAttribute('onclick', 'loginWithGoogle()');
}

function addToCart(id, name, price) { 
    const item = cart.find(i => i.id === id); 
    if (item) { item.quantity += 1; } else { cart.push({ id, name, price, quantity: 1 }); } 
    updateCartUI(); 
    toggleCart(); 
} 

function updateCartUI() { 
    document.getElementById('cartCount').innerText = cart.reduce((s, i) => s + i.quantity, 0); 
    const box = document.getElementById('cartItems'); box.innerHTML = ''; 
    let total = 0; 
    if(cart.length === 0) { box.innerHTML = '<p class=\'text-zinc-500 text-center py-10\'>Кошик порожній</p>'; } 
    cart.forEach(i => { 
        total += i.price * i.quantity; 
        box.innerHTML += '<div class=\'flex justify-between items-center border-b border-zinc-800 pb-3\'><div><h5 class=\'font-bold text-sm text-white\'>' + i.name + '</h5><p class=\'text-xs text-zinc-500\'>' + i.price + ' грн x ' + i.quantity + '</p></div><span class=\'font-black text-orange-500\'>' + (i.price * i.quantity) + ' грн</span></div>'; 
    }); 
    document.getElementById('cartTotal').innerText = total + ' грн'; 
} 

function toggleCart() { document.getElementById('cartModal').classList.toggle('hidden'); } 

function checkoutOrder() { 
    if (!document.getElementById('customerName').value || !cart.length) { alert('Заповніть дані та додайте товари!'); return; } 
    alert('Замовлення успішно оформлене! Чекайте на відправку.'); 
    cart = []; updateCartUI(); toggleCart(); 
} 

fetchProducts();

