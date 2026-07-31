const API_URL = 'http://127.0.0.1:8000/api/';
﻿document.addEventListener('DOMContentLoaded', () => {
    loadProducts('all');
    updateCartCount();
});

function switchCategory(filter, title) {
    const titleEl = document.getElementById('sectionTitle');
    if (titleEl) titleEl.innerText = title;
    loadProducts(filter);
}
async function fetchUserOrders() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert('Будь ласка, увійдіть в систему, щоб переглянути замовлення!');
        return;
    }
    try {
        const res = await fetch(API_URL + 'orders/', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (res.ok) {
            const orders = await res.json();
            console.log('Замовлення користувача:', orders);
            alert('Завантажено замовлень: ' + orders.length);
        } else {
            alert('Помилка завантаження замовлень');
        }
    } catch (e) {
        console.error(e);
    }
}

async function showProductDetail(productId) {
    try {
        const res = await fetch(API_URL + 'shop/products/' + productId + '/');
        const product = await res.json();
        const detailSection = document.getElementById('product-detail-section');
        const catalogSection = document.getElementById('catalog-section');
        
        detailSection.innerHTML = `
            <button onclick="showCatalog()" class="mb-6 inline-flex items-center text-gray-600 hover:text-black font-semibold transition">
                <i class="fa-solid fa-arrow-left mr-2"></i> Назад до каталогу
            </button>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-10 bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
                <div class="aspect-square bg-gray-50 rounded-xl overflow-hidden flex items-center justify-center">
                    <img src="${product.image || 'https://placehold.co/600x600?text=' + encodeURIComponent(product.name)}" class="w-full h-full object-cover">
                </div>
                <div class="flex flex-col justify-between">
                    <div>
                        <span class="text-xs uppercase tracking-widest text-gray-400 font-bold">Деталі товару</span>
                        <h1 class="text-3xl font-extrabold text-gray-900 mt-1 mb-3">${product.name}</h1>
                        <p class="text-3xl text-black font-extrabold mb-6">${product.price} грн</p>
                        
                        <div class="mb-6">
                            <label class="block text-sm font-semibold text-gray-700 uppercase tracking-wider mb-2">Оберіть розмір:</label>
                            <div class="flex gap-2">
                                <button type="button" data-size="S" onclick="selectSizeBtn(this)" class="px-4 py-2 border rounded-lg hover:border-black font-medium transition">S</button>
                                <button type="button" data-size="M" onclick="selectSizeBtn(this)" class="px-4 py-2 border rounded-lg hover:border-black font-medium transition bg-black text-white">M</button>
                                <button type="button" data-size="L" onclick="selectSizeBtn(this)" class="px-4 py-2 border rounded-lg hover:border-black font-medium transition">L</button>
                                <button type="button" data-size="XL" onclick="selectSizeBtn(this)" class="px-4 py-2 border rounded-lg hover:border-black font-medium transition">XL</button>
                            </div>
                        </div>

                        <div class="border-t border-gray-100 pt-4 mb-6">
                            <h3 class="font-semibold text-gray-900 mb-2">Опис:</h3>
                            <p class="text-gray-600 leading-relaxed">${product.description || 'Якісний одяг від ПОТУЖНО Shop. Преміальні матеріали та оверсайз крій.'}</p>
                        </div>
                    </div>

                    <button onclick="addSelectedSizeToCart(${product.id})" class="bg-black text-white py-4 rounded-xl font-bold uppercase tracking-wider hover:bg-gray-800 transition shadow-lg w-full flex items-center justify-center gap-2">
                        <i class="fa-solid fa-cart-shopping"></i> Додати у кошик
                    </button>
                </div>
            </div>
        `;
        
        catalogSection.classList.add('hidden');
        detailSection.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (e) {
        console.error('Помилка завантаження деталей товару:', e);
    }
}

function showCatalog() {
    document.getElementById('product-detail-section').classList.add('hidden');
    document.getElementById('catalog-section').classList.remove('hidden');
}

let rawProductsList = [];

async function loadProductsAndInitFilters() {
    try {
        const res = await fetch(API_URL + 'shop/products/');
        rawProductsList = await res.json();
        applyFilters();
    } catch (e) {
        console.error('Помилка завантаження товарів:', e);
    }
}

function applyFilters() {
    const searchVal = (document.getElementById('search-input')?.value || '').toLowerCase();
    const sortVal = document.getElementById('sort-select')?.value || 'default';

    let filtered = rawProductsList.filter(p => p.name.toLowerCase().includes(searchVal));

    if (sortVal === 'price-asc') {
        filtered.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
    } else if (sortVal === 'price-desc') {
        filtered.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
    } else if (sortVal === 'name-asc') {
        filtered.sort((a, b) => a.name.localeCompare(b.name));
    }

    renderProductsGrid(filtered);
}

function renderProductsGrid(products) {
    const list = document.getElementById('product-list');
    if (!list) return;

    if (products.length === 0) {
        list.innerHTML = '<div class="col-span-full text-center py-12 text-gray-500 font-medium">Товарів за вашим запитом не знайдено</div>';
        return;
    }

    list.innerHTML = products.map(p => `
        <div class="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 flex flex-col justify-between hover:shadow-md transition group">
            <div>
                <div class="aspect-square bg-gray-50 rounded-xl overflow-hidden mb-4 cursor-pointer" onclick="showProductDetail(${p.id})">
                    <img src="${p.image || 'https://placehold.co/400x400?text=' + encodeURIComponent(p.name)}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                </div>
                <h3 class="font-bold text-gray-900 text-lg mb-1 cursor-pointer hover:text-blue-600 transition" onclick="showProductDetail(${p.id})">${p.name}</h3>
                <p class="text-xl font-extrabold text-black mb-3">${p.price} грн</p>
            </div>
            <button onclick="showProductDetail(${p.id})" class="bg-gray-100 text-black px-4 py-2.5 rounded-xl font-semibold hover:bg-black hover:text-white transition w-full text-sm">
                Деталі та розміри
            </button>
        </div>
    `).join('');
}

// Замінюємо початковий виклик
window.addEventListener('DOMContentLoaded', () => {
    loadProductsAndInitFilters();
});

function getWishlist() {
    return JSON.parse(localStorage.getItem('potuzhno_wishlist') || '[]');
}

function saveWishlist(list) {
    localStorage.setItem('potuzhno_wishlist', JSON.stringify(list));
    updateWishlistBadge();
}

function toggleWishlist(productId) {
    let wishlist = getWishlist();
    const index = wishlist.indexOf(productId);
    if (index === -1) {
        wishlist.push(productId);
    } else {
        wishlist.splice(index, 1);
    }
    saveWishlist(wishlist);
    applyFilters();
}

function updateWishlistBadge() {
    const badge = document.getElementById('wishlist-count');
    if (badge) {
        badge.innerText = getWishlist().length;
    }
}

function openWishlistModal() {
    const modal = document.getElementById('wishlist-modal');
    const container = document.getElementById('wishlist-items-container');
    const wishlist = getWishlist();

    const items = rawProductsList.filter(p => wishlist.includes(p.id));

    if (items.length === 0) {
        container.innerHTML = '<p class="col-span-full text-center py-8 text-gray-500">У вашому списку обраного поки порожньо ❤️</p>';
    } else {
        container.innerHTML = items.map(p => `
            <div class="border rounded-xl p-3 flex gap-3 items-center justify-between bg-gray-50">
                <img src="${p.image || 'https://placehold.co/100x100?text=' + encodeURIComponent(p.name)}" class="w-16 h-16 object-cover rounded-lg">
                <div class="flex-1 min-w-0">
                    <h4 class="font-bold text-sm text-gray-900 truncate">${p.name}</h4>
                    <p class="text-sm font-extrabold text-black">${p.price} грн</p>
                </div>
                <div class="flex gap-2">
                    <button onclick="showProductDetail(${p.id}); closeWishlistModal();" class="text-xs bg-black text-white px-3 py-2 rounded-lg hover:bg-gray-800">Переглянути</button>
                    <button onclick="toggleWishlist(${p.id}); openWishlistModal();" class="text-xs text-red-500 hover:text-red-700 p-2"><i class="fa-solid fa-trash"></i></button>
                </div>
            </div>
        `).join('');
    }

    modal.classList.remove('hidden');
}

function closeWishlistModal() {
    document.getElementById('wishlist-modal').classList.add('hidden');
}

// Оновлюємо відображення сердечка в картках товарів
const originalRenderGrid = renderProductsGrid;
renderProductsGrid = function(products) {
    const wishlist = getWishlist();
    const list = document.getElementById('product-list');
    if (!list) return;

    if (products.length === 0) {
        list.innerHTML = '<div class="col-span-full text-center py-12 text-gray-500 font-medium">Товарів за вашим запитом не знайдено</div>';
        return;
    }

    list.innerHTML = products.map(p => {
        const isFav = wishlist.includes(p.id);
        return `
        <div class="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 flex flex-col justify-between hover:shadow-md transition group relative">
            <button onclick="toggleWishlist(${p.id})" class="absolute top-6 right-6 z-10 w-9 h-9 rounded-full bg-white/80 backdrop-blur-md flex items-center justify-center text-gray-400 hover:text-red-500 transition shadow-sm">
                <i class="fa-${isFav ? 'solid text-red-500' : 'regular'} fa-heart text-lg"></i>
            </button>
            <div>
                <div class="aspect-square bg-gray-50 rounded-xl overflow-hidden mb-4 cursor-pointer" onclick="showProductDetail(${p.id})">
                    <img src="${p.image || 'https://placehold.co/400x400?text=' + encodeURIComponent(p.name)}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                </div>
                <h3 class="font-bold text-gray-900 text-lg mb-1 cursor-pointer hover:text-blue-600 transition" onclick="showProductDetail(${p.id})">${p.name}</h3>
                <p class="text-xl font-extrabold text-black mb-3">${p.price} грн</p>
            </div>
            <button onclick="showProductDetail(${p.id})" class="bg-gray-100 text-black px-4 py-2.5 rounded-xl font-semibold hover:bg-black hover:text-white transition w-full text-sm">
                Деталі та розміри
            </button>
        </div>
    `}).join('');
};

document.addEventListener('DOMContentLoaded', () => {
    updateWishlistBadge();
});

async function openAccountModal() {
    const modal = document.getElementById('account-modal');
    const container = document.getElementById('account-content');
    const token = localStorage.getItem('access_token');

    modal.classList.remove('hidden');

    if (!token) {
        container.innerHTML = `
            <div class="text-center py-8">
                <i class="fa-solid fa-lock text-4xl text-gray-300 mb-3 block"></i>
                <p class="text-gray-600 mb-4 font-medium">Ви не авторизовані. Будь ласка, увійдіть в систему.</p>
                <button onclick="closeAccountModal();" class="bg-black text-white px-6 py-2.5 rounded-xl font-bold hover:bg-gray-800 transition">
                    Зрозуміло
                </button>
            </div>
        `;
        return;
    }

    container.innerHTML = '<p class="text-center py-8 text-gray-500">Завантаження історії замовлень...</p>';

    try {
        const res = await fetch(API_URL + 'orders/', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        
        if (!res.ok) throw new Error('Помилка доступу');
        const orders = await res.json();

        let ordersHtml = '';
        if (orders.length === 0) {
            ordersHtml = '<p class="text-gray-500 py-4 text-center">У вас поки немає оформлених замовлень.</p>';
        } else {
            ordersHtml = orders.map(o => `
                <div class="border rounded-xl p-4 bg-gray-50 mb-3">
                    <div class="flex justify-between items-center mb-2 border-b pb-2">
                        <span class="font-extrabold text-sm text-gray-900">Замовлення #${o.id}</span>
                        <span class="text-xs bg-black text-white px-2.5 py-1 rounded-full uppercase font-bold tracking-wider">${o.status || 'В обробці'}</span>
                    </div>
                    <div class="text-xs text-gray-600 space-y-1">
                        <p><strong>Отримувач:</strong> ${o.first_name || ''} ${o.last_name || ''}</p>
                        <p><strong>Телефон:</strong> ${o.phone || 'Н/Д'}</p>
                        <p><strong>Доставка:</strong> м. ${o.city || 'Н/Д'}, Відділення #${o.warehouse || '1'}</p>
                        <p class="text-sm font-bold text-black mt-2">Сума: ${o.total_price || 0} грн</p>
                    </div>
                </div>
            `).join('');
        }

        container.innerHTML = `
            <div class="flex justify-between items-center bg-gray-100 p-4 rounded-xl mb-4">
                <div>
                    <p class="font-bold text-gray-900">Авторизований сеанс (JWT)</p>
                    <p class="text-xs text-gray-500">Токен збережено в LocalStorage</p>
                </div>
                <button onclick="logoutUser()" class="text-xs bg-red-100 text-red-600 px-3 py-2 rounded-lg font-bold hover:bg-red-200 transition">
                    Вийти
                </button>
            </div>
            <div>
                <h3 class="font-bold text-lg mb-3 text-gray-900 flex items-center gap-2">
                    <i class="fa-solid fa-box text-black"></i> Історія замовлень (${orders.length})
                </h3>
                ${ordersHtml}
            </div>
        `;
    } catch (e) {
        container.innerHTML = `
            <div class="text-center py-6 text-red-500">
                <p class="font-bold mb-2">Сесія застаріла або виникла помилка авторизації.</p>
                <button onclick="logoutUser()" class="text-xs bg-black text-white px-4 py-2 rounded-lg font-bold">Очистити токен та вийти</button>
            </div>
        `;
    }
}

function closeAccountModal() {
    document.getElementById('account-modal').classList.add('hidden');
}

function logoutUser() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    closeAccountModal();
    alert('Ви успішно вийшли з акаунту');
    location.reload();
}

function selectSizeBtn(btnElement) {
    const allBtns = document.querySelectorAll('#product-detail-section button[data-size]');
    allBtns.forEach(b => {
        b.classList.remove('bg-black', 'text-white');
        b.classList.add('border-gray-200');
    });
    btnElement.classList.add('bg-black', 'text-white');
    btnElement.classList.remove('border-gray-200');
}

function addSelectedSizeToCart(productId) {
    const activeSizeBtn = document.querySelector('#product-detail-section button[data-size].bg-black');
    const selectedSize = activeSizeBtn ? activeSizeBtn.dataset.size : 'M';
    addToCart(productId, selectedSize);
}


function checkoutOrder() {
    const cart = JSON.parse(localStorage.getItem('potuzhno_cart') || '[]');
    if (!cart || cart.length === 0) {
        alert('Ваш кошик порожній!');
        return;
    }
    
    const checkoutModal = document.getElementById('checkout-modal');
    if (checkoutModal) {
        if (typeof closeCartModal === 'function') closeCartModal();
        checkoutModal.classList.remove('hidden');
    } else {
        alert('Замовлення успішно оформлено! Дякуємо за покупку в ПОТУЖНО Shop 🔥');
        localStorage.removeItem('potuzhno_cart');
        if (typeof updateCartUI === 'function') updateCartUI();
        if (typeof closeCartModal === 'function') closeCartModal();
        location.reload();
    }
}


let currentCategory = 'all';
let currentSize = 'all';

function setCategoryFilter(cat, btn) {
    currentCategory = cat;
    document.querySelectorAll('.cat-btn').forEach(b => {
        b.classList.remove('bg-orange-500', 'text-white', 'shadow-md');
        b.classList.add('bg-neutral-800', 'text-neutral-300');
    });
    btn.classList.add('bg-orange-500', 'text-white', 'shadow-md');
    btn.classList.remove('bg-neutral-800', 'text-neutral-300');
    applyFilters();
}

function setSizeFilter(size, btn) {
    currentSize = size;
    document.querySelectorAll('.size-filter-btn').forEach(b => {
        b.classList.remove('bg-white', 'text-black');
        b.classList.add('bg-neutral-800', 'text-neutral-300');
    });
    btn.classList.add('bg-white', 'text-black');
    btn.classList.remove('bg-neutral-800', 'text-neutral-300');
    applyFilters();
}

function applyFilters() {
    const searchVal = (document.getElementById('search-input')?.value || '').toLowerCase();
    const sortVal = document.getElementById('sort-select')?.value || 'default';

    let filtered = rawProductsList.filter(p => {
        const name = (p.name || '').toLowerCase();
        const desc = (p.description || '').toLowerCase();
        const category = (p.category_name || p.category?.name || '').toLowerCase();

        const matchesSearch = name.includes(searchVal) || desc.includes(searchVal);

        let matchesCategory = true;
        if (currentCategory !== 'all') {
            matchesCategory = name.includes(currentCategory) || desc.includes(currentCategory) || category.includes(currentCategory);
        }

        let matchesSize = true;
        if (currentSize !== 'all') {
            matchesSize = desc.includes(currentSize) || name.includes(currentSize) || true;
        }

        return matchesSearch && matchesCategory && matchesSize;
    });

    if (sortVal === 'price-asc') {
        filtered.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
    } else if (sortVal === 'price-desc') {
        filtered.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
    } else if (sortVal === 'name-asc') {
        filtered.sort((a, b) => a.name.localeCompare(b.name));
    }

    renderProductsGrid(filtered);
}



let activeCategory = 'all';

function filterCategory(catKey, btnElement) {
    activeCategory = catKey;

    // 1. Оновлення активної кнопки (підсвічування помаранчевим)
    const buttons = document.querySelectorAll('.cat-btn, [onclick*="filterCategory"]');
    buttons.forEach(b => {
        b.classList.remove('bg-orange-500', 'text-white', 'shadow-md');
        b.classList.add('bg-neutral-800', 'text-neutral-300');
    });

    if (btnElement) {
        btnElement.classList.remove('bg-neutral-800', 'text-neutral-300');
        btnElement.classList.add('bg-orange-500', 'text-white', 'shadow-md');
    }

    // Оновлення заголовку над каталогом
    const titleEl = document.querySelector('#catalog-section h2, .catalog-title');
    if (titleEl) {
        const titleMap = {
            'all': 'Всі товари каталогу',
            'clothing': 'Одяг',
            'shoes': 'Взуття',
            'accessories': 'Аксесуари',
            'men': 'Чоловіча колекція',
            'women': 'Жіноча колекція',
            'kids': 'Дитяча колекція'
        };
        if (titleMap[catKey]) titleEl.innerText = titleMap[catKey];
    }

    applyFilters();
}

function applyFilters() {
    const searchInput = document.getElementById('search-input');
    const searchVal = (searchInput ? searchInput.value : '').toLowerCase();
    const sortVal = document.getElementById('sort-select')?.value || 'default';

    if (!Array.isArray(rawProductsList)) return;

    let filtered = rawProductsList.filter(p => {
        const name = (p.name || '').toLowerCase();
        const desc = (p.description || '').toLowerCase();
        const catName = (p.category_name || p.category?.name || p.category || '').toString().toLowerCase();

        // 1. Пошуковий запит
        const matchesSearch = !searchVal || name.includes(searchVal) || desc.includes(searchVal) || catName.includes(searchVal);

        // 2. Розумне групування за категоріями
        let matchesCategory = true;
        if (activeCategory === 'clothing' || activeCategory === 'одяг') {
            matchesCategory = catName.includes('одяг') || name.includes('світшот') || name.includes('штани') || name.includes('худі') || name.includes('футболка') || name.includes('куртка') || desc.includes('одяг') || desc.includes('якість');
        } else if (activeCategory === 'shoes' || activeCategory === 'взуття') {
            matchesCategory = catName.includes('взуття') || name.includes('кросівки') || name.includes('кеди') || name.includes('air') || name.includes('tech') || desc.includes('взуття');
        } else if (activeCategory === 'accessories' || activeCategory === 'аксесуари') {
            matchesCategory = catName.includes('аксесуар') || name.includes('сумка') || name.includes('кепка') || name.includes('шапка') || name.includes('рюкзак') || desc.includes('аксесуар');
        } else if (activeCategory === 'men' || activeCategory === 'women' || activeCategory === 'kids') {
            matchesCategory = true; // Показує всі товари під колекції
        } else if (activeCategory !== 'all') {
            matchesCategory = catName.includes(activeCategory) || name.includes(activeCategory) || desc.includes(activeCategory);
        }

        return matchesSearch && matchesCategory;
    });

    if (sortVal === 'price-asc') {
        filtered.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
    } else if (sortVal === 'price-desc') {
        filtered.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
    } else if (sortVal === 'name-asc') {
        filtered.sort((a, b) => a.name.localeCompare(b.name));
    }

    renderProductsGrid(filtered);
}



let currentCatKey = 'all';

function handleCatClick(catKey, btnEl) {
    currentCatKey = catKey;

    // Підсвічування активної кнопки
    const allCatBtns = document.querySelectorAll('button[onclick*="handleCatClick"]');
    allCatBtns.forEach(b => {
        b.classList.remove('bg-orange-500', 'text-white', 'shadow-md', 'bg-gradient-to-r', 'from-orange-500', 'to-amber-500');
        b.classList.add('bg-neutral-800', 'text-neutral-300');
    });

    if (btnEl) {
        btnEl.classList.remove('bg-neutral-800', 'text-neutral-300');
        btnEl.classList.add('bg-orange-500', 'text-white', 'shadow-md');
    }

    // Зміна заголовка
    const catalogTitle = document.querySelector('h1, h2, .catalog-title');
    const titleMap = {
        'all': 'Всі товари каталогу',
        'clothing': 'Одяг',
        'shoes': 'Взуття',
        'accessories': 'Аксесуари',
        'men': 'Чоловіча колекція',
        'women': 'Жіноча колекція',
        'kids': 'Дитяча колекція'
    };
    if (catalogTitle && titleMap[catKey]) {
        catalogTitle.textContent = titleMap[catKey];
    }

    applyFilters();
}

function applyFilters() {
    const searchVal = (document.getElementById('search-input')?.value || '').toLowerCase().trim();
    const sortVal = document.getElementById('sort-select')?.value || 'default';

    if (!Array.isArray(rawProductsList)) return;

    let filtered = rawProductsList.filter(p => {
        const name = (p.name || '').toLowerCase();
        const desc = (p.description || '').toLowerCase();
        const cat = (p.category_name || p.category?.name || p.category || '').toString().toLowerCase();

        // 1. Пошук
        const matchesSearch = !searchVal || name.includes(searchVal) || desc.includes(searchVal) || cat.includes(searchVal);

        // 2. Фільтрація за категорією
        let matchesCategory = true;
        if (currentCatKey === 'clothing') {
            matchesCategory = cat.includes('одяг') || name.includes('світшот') || name.includes('штани') || name.includes('худі') || name.includes('футболка') || desc.includes('одяг');
        } else if (currentCatKey === 'shoes') {
            matchesCategory = cat.includes('взуття') || name.includes('кросівки') || name.includes('кеди') || name.includes('air') || name.includes('tech') || desc.includes('взуття');
        } else if (currentCatKey === 'accessories') {
            matchesCategory = cat.includes('аксесуар') || name.includes('сумка') || name.includes('кепка') || name.includes('шапка') || desc.includes('аксесуар');
        } else if (['men', 'women', 'kids'].includes(currentCatKey)) {
            matchesCategory = true;
        } else if (currentCatKey !== 'all') {
            matchesCategory = cat.includes(currentCatKey) || name.includes(currentCatKey);
        }

        return matchesSearch && matchesCategory;
    });

    if (sortVal === 'price-asc') {
        filtered.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
    } else if (sortVal === 'price-desc') {
        filtered.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
    } else if (sortVal === 'name-asc') {
        filtered.sort((a, b) => a.name.localeCompare(b.name));
    }

    renderProductsGrid(filtered);
}
