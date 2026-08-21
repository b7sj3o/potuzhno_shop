import { useEffect, useState } from "react";
import { fetchProducts } from "./api/products";
import './App.css'
import LoginForm from "./components/LoginForm.jsx";
import SearchBar from "./components/SearchBar.jsx";
import ProductList from "./components/ProductList.jsx";
import {clearTokens, isLoggedIn} from "./api/auth.js";


function App() {
  const [search, setSearch] = useState("");
  const [query, setQuery] = useState("");
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [logged, setLogged] = useState(isLoggedIn());

  useEffect(() => {
    const timer = setTimeout(() => setQuery(search), 400);
    return () => clearTimeout(timer);
  }, [search]);

  useEffect(() => {
    const controller = new AbortController();

    setLoading(true);
    setError(null);

    fetchProducts({ search: query, signal: controller.signal })
      .then((data) => setProducts(data.results))
      .catch((err) => {
        if (err.name !== "AbortError") setError(err);
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, [query]);

  async function handleToggleFavourite(product) {
      const wasFavourite = product.is_favourite;

      setProducts((prev) =>
        prev.map((p) =>
          p.id === product.id ? { ...p, is_favourite: !wasFavourite } : p
        )
      );

      try {
        if (wasFavourite) {
          await removeFavourite(product.id);
        } else {
          await addFavourite(product.id);
        }
      } catch (err) {
        // Не вийшло — повертаємо як було
        setProducts((prev) =>
          prev.map((p) =>
            p.id === product.id ? { ...p, is_favourite: wasFavourite } : p
          )
        );
        if (err.status === 401) {
          alert("Спершу увійдіть");
        }
      }
  }

  function handleLogout() {
    clearTokens();
    setLogged(false);
  }

  return (
    <main className="app">
      <header className="topbar">
        <h1>ПОТУЖНО Shop</h1>
        {logged ? (
          <button onClick={handleLogout}>Вийти</button>
        ) : (
          <LoginForm onSuccess={() => setLogged(true)} />
        )}
      </header>

      <SearchBar value={search} onChange={setSearch} />

      <ProductList
        products={products}
        loading={loading}
        error={error}
        canFavourite={logged}
        onToggleFavourite={handleToggleFavourite}
      />
    </main>
  );
}

export default App
