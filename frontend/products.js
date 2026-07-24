async function loadProducts(filter = 'all') {
    try {
        const res = await httpGetProducts();
        let products = await res.json();

        if (filter !== 'all') {
            products = products.filter(p => {
                let cat = p.category;
                if (typeof cat === 'object' && cat !== null) {
                    cat = cat.name || cat.slug || JSON.stringify(cat);
                }
                let gen = p.gender;
                if (typeof gen === 'object' && gen !== null) {
                    gen = gen.name || gen.slug || JSON.stringify(gen);
                }
                const catStr = String(cat || '').toLowerCase();
                const genStr = String(gen || '').toLowerCase();
                const f = filter.toLowerCase();
                return catStr.includes(f) || genStr.includes(f);
            });
        }

        const container = document.getElementById('productList');
        if (!container) return;

        container.innerHTML = products.map(p => `
            <div class="bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden shadow-xl flex flex-col justify-between">
                <div>
                    <img src="${p.image || 'https://via.placeholder.com/300'}" alt="${p.name}" class="w-full h-48 object-cover">
                    <div class="p-5">
                        <h3 class="text-lg font-bold text-white mb-2">${p.name}</h3>
                        <p class="text-zinc-400 text-sm mb-4">${p.description || 'Якісний товар від Потужно Shop'}</p>
                    </div>
                </div>
                <div class="p-5 pt-0 flex items-center justify-between">
                    <span class="text-xl font-black text-orange-500">${p.price} грн</span>
                    <button onclick='addToCart(${p.id})' class="bg-orange-600 hover:bg-orange-500 text-white px-4 py-2 rounded-xl text-xs font-black transition">В кошик</button>
                </div>
            </div>
        `).join('');
    } catch (e) {
        console.error('Помилка завантаження товарів:', e);
    }
}

async function httpGetProducts() {
    return await fetch('http://127.0.0.1:8000/api/shop/products/');
}