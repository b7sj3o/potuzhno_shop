// додав клієнтський API-модуль для замовлень та відгуків
class ShopAPI {
    static async createOrder(orderData, token) {
        const response = await fetch('/api/orders/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(orderData)
        });
        return await response.json();
    }

    static async addReview(reviewData, token) {
        const response = await fetch('/api/shop/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(reviewData)
        });
        return await response.json();
    }
}
