let cart = JSON.parse(localStorage.getItem('potuzhno_cart')) || [];

function addToCart(product) {
    cart.push(product);
    localStorage.setItem('potuzhno_cart', JSON.stringify(cart));
    updateCartCount();
}

function updateCartCount() {
    const badge = document.getElementById('cartCount');
    if (badge) badge.innerText = cart.length;
}

function toggleCart() {
    const modal = document.getElementById('cartModal');
    if (modal) modal.classList.toggle('hidden');
}