const API_URL = 'http://127.0.0.1:8000/api/';

const translations = {
    uk: {
        heroTitle: 'Преміальний спортивний одяг та взуття',
        heroSubtitle: 'Швидка відправка поштою 🚀',
        catalogTitle: 'Каталог товарів',
        buyBtn: 'Купити'
    },
    en: {
        heroTitle: 'Premium sportswear and footwear',
        heroSubtitle: 'Fast postal delivery 🚀',
        catalogTitle: 'Product Catalog',
        buyBtn: 'Buy'
    }
};

let currentLang = 'uk';

document.getElementById('langSelect').addEventListener('change', (e) => {
    currentLang = e.target.value;
    updateLanguage();
});

function updateLanguage() {
    document.getElementById('heroTitle').innerText = translations[currentLang].heroTitle;
    document.getElementById('heroSubtitle').innerText = translations[currentLang].heroSubtitle;
    document.getElementById('catalogTitle').innerText = translations[currentLang].catalogTitle;
    fetchProducts();
}

async function fetchProducts() {
    try {
        const response = await fetch(${API_URL}shop/products/);
        const products = await response.json();
        const container = document.getElementById('productList');
        container.innerHTML = '';

        products.forEach(product => {
            container.innerHTML += 
                <div class='bg-white rounded-xl shadow-lg overflow-hidden border border-gray-100 hover:shadow-xl transition'>
                    <div class='h-48 bg-gray-200 flex items-center justify-center text-gray-400'>📦 Photo</div>
                    <div class='p-5'>
                        <h4 class='font-bold text-lg mb-2'></h4>
                        <p class='text-orange-600 font-extrabold text-xl mb-4'> грн</p>
                        <button onclick='addToCart()' class='w-full bg-black text-white py-2 rounded-lg font-medium hover:bg-gray-800 transition'>
                            
                        </button>
                    </div>
                </div>
            ;
        });
    } catch (error) {
        console.error('Помилка завантаження товарів:', error);
    }
}

function addToCart(productId) {
    alert('Товар додано до кошика! (ID: ' + productId + ')');
}

fetchProducts();
