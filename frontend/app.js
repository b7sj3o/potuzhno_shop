// --- ПОТУЖНО Shop Main App JS ---
document.addEventListener("DOMContentLoaded", () => {
    console.log("⚡ ПОТУЖНО Shop Frontend Initialized");
    loadProductsAndInitFilters();
});

async function loadProductsAndInitFilters() {
    try {
        const response = await fetch('/api/shop/products/');
        if (!response.ok) throw new Error("Помилка завантаження API");
        const products = await response.json();
        renderProducts(products);
    } catch (error) {
        console.warn("ℹ️ API каталогу недоступне або використовується шаблонний рендеринг:", error);
    }
}

function renderProducts(products) {
    const listContainer = document.getElementById("productList");
    if (!listContainer) return;
    
    listContainer.innerHTML = "";
    products.forEach(p => {
        const card = document.createElement("div");
        card.className = "bg-zinc-900 border border-zinc-800 rounded-2xl p-4 flex flex-col justify-between";
        card.innerHTML = `
            <div>
                <h3 class="text-lg font-bold text-white mb-2">${p.name}</h3>
                <p class="text-zinc-400 text-sm mb-4">${p.description ? p.description.substring(0, 60) + '...' : ''}</p>
            </div>
            <div class="flex justify-between items-center mt-4">
                <span class="text-orange-500 font-black text-lg">${p.price} грн</span>
                <a href="/products/${p.slug}/" class="bg-orange-600 text-white px-3 py-1.5 rounded-xl text-xs font-bold hover:bg-orange-500 transition">Детальніше</a>
            </div>
        `;
        listContainer.appendChild(card);
    });
}

function toggleCart() {
    const modal = document.getElementById("cartModal");
    if (modal) {
        modal.classList.toggle("hidden");
    }
}

function applyFilters() {
    console.log("Фільтрація застосована");
}
