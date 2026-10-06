# Activación del piloto SAHER

La interfaz permanece en GitHub Pages. El servidor de IA se prepara en Render; todavía no está desplegado.

## Configuración preparada

`render.yaml`, en la raíz del repositorio, define un servicio Node del plan gratuito, con el código de la rama `saher-ia-piloto`. Ejecuta las pruebas antes de iniciar. Render debe permitir el plan elegido en la cuenta; no se ha contratado un servicio de pago.

Los valores de `OPENAI_API_KEY` y `OPENAI_MODEL` se ingresan en la configuración privada de Render. `PILOT_TOKEN` se genera como secreto. No se deben pegar secretos en GitHub ni en el chat. El acceso compartido es solo para pruebas privadas.

## Orden para activar

1. Conectar Render y OpenAI Developers a ChatGPT.
2. Crear el servicio desde el Blueprint del repositorio. Configurar la clave de OpenAI y un modelo disponible en la cuenta. Mantener el servicio en el plan gratuito durante el piloto.
3. Comprobar `/api/health`: debe devolver `configured: true`. Esto solo comprueba presencia de configuración; no verifica crédito ni acceso al modelo.
4. Probar `/api/chat` con el código del piloto y un caso de plomería. Verificar respuesta real, errores y límites.
5. Configurar `SAHER_AI_URL` en `saher/index.html` con el endpoint HTTPS asignado. No adivinar el dominio. Publicar la interfaz cuando la prueba real pase.
6. Abrir SAHER desde el celular y comprobar la conversación y el paso al formulario.

El servicio también puede mostrar la interfaz en su propia raíz para probar antes de publicar en GitHub Pages. `ALLOWED_ORIGIN` restringe las llamadas del navegador al origen de GitHub; para pruebas con la interfaz del servidor, configurar el origen de ese servidor.

En el checkout local anterior, la interfaz está en `dist/index.html`; iniciar con `HTML_PATH=../dist/index.html`. En GitHub está en `saher/index.html`, que es la ruta predeterminada del servidor.

## Límites de esta versión

La IA no crea reservas, no asigna profesionales y no fija precios. No se ha conectado la base de prospectos a un catálogo de profesionales inscritos. El límite de consultas está en memoria; para apertura comercial hacen falta autenticación y cuotas persistentes.

Referencia técnica: https://render.com/docs/blueprint-spec
