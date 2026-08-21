export default function ProductCard({ product, onToggleFavourite, canFavourite }) {
  return (
    <article className="card">
      <h3>{product.name}</h3>
      <p className="brand">
        {product.brand?.name} · {product.category?.name}
      </p>
      <p className="price">{product.price} ₴</p>

      <p className="rating">
        {product.avg_rating === null
          ? "Ще без оцінок"
          : `★ ${Number(product.avg_rating).toFixed(1)} (${product.reviews_count})`}
      </p>

      {canFavourite && (
        <button
          className={product.is_favourite ? "fav active" : "fav"}
          onClick={() => onToggleFavourite(product)}
        >
          {product.is_favourite ? "♥ В обраному" : "♡ В обране"}
        </button>
      )}
    </article>
  );
}
