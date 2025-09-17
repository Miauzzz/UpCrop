const API_BASE = "http://localhost:8000/api/";

export async function loginCliente(usuario, contrasena) {
  const res = await fetch(`${API_BASE}login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario, contrasena }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.msg);
  return data;
}
