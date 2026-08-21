import { request } from "./client.js";

const ACCESS = "potuzhno_access";
const REFRESH = "potuzhno_refresh";

export const getAccess = () => localStorage.getItem(ACCESS);
export const getRefresh = () => localStorage.getItem(REFRESH);

export function saveTokens({ access, refresh }) {
  localStorage.setItem(ACCESS, access);
  if (refresh) localStorage.setItem(REFRESH, refresh);
}

export function clearTokens() {
  localStorage.removeItem(ACCESS);
  localStorage.removeItem(REFRESH);
}

export const isLoggedIn = () => Boolean(getAccess());


export async function login(username, password) {
  const tokens = await request("/token/", {
    method: "POST",
    body: { username, password },
  });
  saveTokens(tokens);
  return tokens;
}