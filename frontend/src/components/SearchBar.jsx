export default function SearchBar({ value, onChange }) {
  return (
    <input
      className="search"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Пошук: назва, бренд, категорія…"
    />
  );
}