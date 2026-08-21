import { request } from "./client";

export function fetchProducts({ search, ordering, inStock, signal } = {}) {
  const params = new URLSearchParams();
  if (search) params.set("search", search);
  if (ordering) params.set("ordering", ordering);
  if (inStock) params.set("in_stock", "true");

  const query = params.toString();

  return request(`/products/${query ? `?${query}` : ""}`, { signal });
}


export function addFavourite(id) {
  return request(`/products/${id}/favourite/`, { method: "POST" });
}

export function removeFavourite(id) {
  return request(`/products/${id}/favourite/`, { method: "DELETE" });
}