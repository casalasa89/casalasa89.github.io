# Asistente SAHER · piloto privado

Servidor Node.js 22 o superior, sin dependencias. Conserva la clave OpenAI únicamente en el servidor. No hay base de datos ni pagos reales.

1. Copiar `api/.env.example` a `api/.env`. Completar `OPENAI_API_KEY`, `OPENAI_MODEL` (modelo disponible en la cuenta) y `PILOT_TOKEN` (código largo y aleatorio para participantes del piloto). No subir `.env` a GitHub.
2. Desde esta carpeta: `node --env-file=api/.env api/server.mjs`. Abrir http://127.0.0.1:3000.
3. Para GitHub Pages: alojar este servidor detrás de HTTPS, configurar `HOST` según el proveedor y sustituir `SAHER_AI_URL` en el HTML por la URL completa del endpoint `/api/chat`. GitHub Pages no ejecuta el servidor.
4. Compartir el código del piloto solo con participantes autorizados. La interfaz lo conserva únicamente en memoria.

`POST /api/chat`: JSON `{ "city": "Pasto", "messages": [{"role":"user","content":"Tengo una fuga"}] }`, cabecera `Authorization: Bearer <PILOT_TOKEN>`. Devuelve `{ "reply": "..." }`. Solo transmite conversación y ciudad; no fotos ni datos del formulario.

Limitaciones: clave y modelo no configurados; conexión real aún no probada. Límite global de 20 consultas/minuto y 3 simultáneas por proceso, reiniciable; acceso por código compartido apropiado solo para pruebas privadas. Antes del lanzamiento abierto hacen falta usuarios autenticados, cuotas persistentes y presupuesto de consumo. Los prospectos investigados no son profesionales inscritos y no se ofrecen como disponibles.

Pruebas: `node --test api/server.test.mjs` (proveedor simulado, sin gasto de API).
