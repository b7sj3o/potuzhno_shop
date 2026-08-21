import { useState } from "react";
import { login } from "../api/auth";


export default function LoginForm({ onSuccess }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [busy, setBusy] = useState(false);

    async function handleSubmit(event) {
        if (busy) return;

        event.preventDefault();
        setError(null);
        setBusy(true);
        try {
          await login(username, password);
          onSuccess();
        } catch (err) {
          setError(
            err.status === 401
              ? "Невірний логін або пароль"
              : "Не вдалося зайти. Спробуйте ще раз."
          );
        } finally {
          setBusy(false);
        }
    }

    return (
        <form onSubmit={handleSubmit} className="login">
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Логін"
            autoComplete="username"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Пароль"
            autoComplete="current-password"
          />
          <button disabled={busy}>{busy ? "Входимо…" : "Увійти"}</button>
          {error && <p className="error">{error}</p>}
        </form>
    );
}