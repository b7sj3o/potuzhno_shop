import { getAccess } from "./auth.js";

const BASE = import.meta.env.VITE_API_URL;


export async function request(path, { method = "GET", body, signal } = {}) {
    const headers = {};

    if (body) headers["Content-Type"] = "application/json";

    const token = getAccess();
    if (token) headers["Authorization"] = `Bearer ${token}`;


    const response = await fetch(`${BASE}${path}`, {
        method,
        headers,
        signal,
        body: body ? JSON.stringify(body) : undefined
    })

    return await response.json().catch(() => null)
}