async function loadProducts(filter = 'all') {
    try {
        const res = await httpGetProducts();
        let products = await res.json();
        
        if (filter !== 'all') {
            products = products.filter(p => {
                const cat = (p.category || '').toLowerCase();
                const gen = (p.gender || '').toLowerCase();
                const f = filter.toLowerCase();
                return cat === f || gen === f;
            });
        }
        
        const container = document.getElementById('productList');
        if (!container) return;
        
        if (products.length === 0) {
            container.innerHTML = '<p class="col-span-full text-center text-zinc-500 py-10">Товарів не знайдено</p>';
            return;
        }

        container.innerHTML = products.map(p => 
            <div class="bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden shadow-lg hover:border-orange-500 transition flex flex-col justify-between">
                <div>
                    <img src="" class="w-full h-64 object-cover" onerror="this.src='https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&auto=format&fit=crop&q=80'">
                    <div class="p-5">
                        <h3 class="text-lg font-black text-white"></h3>
                        <p class="text-zinc-400 text-xs mt-1 line-clamp-2"></p>
                    </div>
                </div>
                <div class="p-5 pt-0 flex items-center justify-between">
                    <span class="text-xl font-black text-orange-500"> грн</span>
                    <button onclick='addToCart()' class="bg-orange-600 hover:bg-orange-500 text-white px-4 py-2 rounded-xl text-xs font-black transition">В кошик</button>
                </div>
            </div>
        ).join('');
    } catch (e) {
        console.error('Помилка завантаження товарів:', e);
    }
}

async function httpGetProducts() {
    return await fetch('http://127.0.0.1:8000/api/shop/products/');
}