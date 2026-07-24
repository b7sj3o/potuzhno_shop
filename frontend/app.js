document.addEventListener('DOMContentLoaded', () => {
    loadProducts('all');
    updateCartCount();
});

function switchCategory(filter, title) {
    const titleEl = document.getElementById('sectionTitle');
    if (titleEl) titleEl.innerText = title;
    loadProducts(filter);
}