import ProductCard from "./ProductCard";

export default function ProductList({ products, loading, error, ...rest }) {
  if (loading) return <p className="hint">Завантаження…</p>;
  if (error) return <p className="error">Не вдалося завантажити товари</p>;
  if (products.length === 0) return <p className="hint">Нічого не знайдено</p>;

  return (
    <div className="flex flex-wrap">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} {...rest} />
      ))}
    </div>
  );
}
