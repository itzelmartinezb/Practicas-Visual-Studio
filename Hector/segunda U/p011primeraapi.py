# ============================================================
# API BÁSICA UTILIZANDO SOLAMENTE PYTHON
# Sin ningún framework
# ============================================================

# Permite crear un servidor HTTP.
from http.server import BaseHTTPRequestHandler, HTTPServer

# Permite convertir diccionarios de Python a formato JSON.
import json


# Definimos la clase que atenderá las solicitudes HTTP.
class MiAPI(BaseHTTPRequestHandler):

    # Este método atiende las peticiones GET.
    def do_GET(self):

        # Ruta principal.
        if self.path == "/":
            respuesta = {
                "mensaje": "Bienvenido a mi API",
                "estado": "Funcionando"
            }

        # Ruta para mostrar un saludo.
        elif self.path == "/saludo":
            respuesta = {
                "mensaje": "Hola, estamos aprendiendo a crear APIs"
            }

        # Nueva ruta GET para consultar productos.
        elif self.path == "/productos":
            respuesta = {
                "productos": [
                    {
                        "id": 1,
                        "nombre": "Mesa",
                        "precio": 30
                    },
                    {
                        "id": 2,
                        "nombre": "Silla",
                        "precio": 20
                    },
                    {
                        "id": 3,
                        "nombre": "Mantel",
                        "precio": 11
                    }
                ]
            }

        # Si la ruta no existe, devolvemos un error 404.
        else:
            contenido = json.dumps(
                {"error": "Ruta no encontrada"},
                ensure_ascii=False
            ).encode("utf-8")

            self.send_response(404)
            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )
            self.send_header(
                "Content-Length",
                str(len(contenido))
            )
            self.end_headers()
            self.wfile.write(contenido)
            return

        # Convertimos la respuesta a JSON y después a bytes.
        contenido = json.dumps(
            respuesta,
            ensure_ascii=False
        ).encode("utf-8")

        # Indicamos que la solicitud fue exitosa.
        self.send_response(200)

        # Informamos que la respuesta contiene JSON.
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        # Indicamos el tamaño del contenido.
        self.send_header(
            "Content-Length",
            str(len(contenido))
        )

        # Finalizamos las cabeceras HTTP.
        self.end_headers()

        # Enviamos el contenido al cliente.
        self.wfile.write(contenido)


# ============================================================
# INICIAR EL SERVIDOR
# ============================================================

if __name__ == "__main__":

    # Creamos el servidor en el puerto 8000.
    servidor = HTTPServer(
        ("127.0.0.1", 8000),
        MiAPI
    )

    print("API disponible en http://127.0.0.1:8000")
    print("Saludo: http://127.0.0.1:8000/saludo")
    print("Productos: http://127.0.0.1:8000/productos")
    print("Presiona CTRL+C para detener el servidor.")

    # Mantenemos el servidor en funcionamiento.
    servidor.serve_forever()