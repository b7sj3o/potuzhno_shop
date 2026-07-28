document.addEventListener('DOMContentLoaded', () => {
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
