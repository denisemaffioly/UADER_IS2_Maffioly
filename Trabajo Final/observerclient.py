# observerclient.py
import socket
import json
import argparse
import uuid
import logging
import time
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# -----------------------------
# Funciones principales
# -----------------------------

def subscribe(host, port, uuid_client, stop_event):
    """Conecta al servidor y recibe notificaciones."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while not stop_event.is_set():
        try:
            s.connect((host, port))
            logging.info("Conectado a %s:%s", host, port)
            break
        except Exception as e:
            logging.warning("Cannot connect to %s:%s - retry in 5s", host, port)
            time.sleep(5)
    payload = {"UUID": uuid_client, "ACTION": "subscribe"}
    s.sendall((json.dumps(payload) + '\n').encode('utf-8'))

    # receive ack
    data = b''
    while True:
        part = s.recv(4096)
        if not part:
            logging.error("Connection closed by server")
            return
        data += part
        if b'\n' in data:
            break
    try:
        ack = json.loads(data.decode('utf-8').strip())
        logging.info("Subscribe ack: %s", ack)
    except Exception:
        logging.info("Non-json ack: %s", data)

    # ahora seguir recibiendo notificaciones
    buffer = b''
    try:
        while not stop_event.is_set():
            chunk = s.recv(4096)
            if not chunk:
                logging.info("Server closed connection")
                break
            buffer += chunk
            while b'\n' in buffer:
                line, buffer = buffer.split(b'\n', 1)
                if not line:
                    continue
                try:
                    msg = json.loads(line.decode('utf-8'))
                    print("\n[NOTIFICACIÓN RECIBIDA]")
                    print(json.dumps(msg, indent=2, ensure_ascii=False))
                    print("Ingrese comando (get/list/set/exit): ", end="", flush=True)
                except Exception as e:
                    logging.warning("Malformed msg: %s", e)
    except KeyboardInterrupt:
        logging.info("Observer client stopped")
    finally:
        try:
            s.close()
        except:
            pass

# -----------------------------
# Menú interactivo
# -----------------------------

def command_loop(stop_event):
    """Permite escribir comandos mientras se reciben notificaciones."""
    while not stop_event.is_set():
        cmd = input("Ingrese comando (get/list/set/exit): ").strip().lower()
        if cmd == "get":
            archivo = input("Nombre del archivo a obtener: ")
            print(f"[SIMULACIÓN] GET {archivo}")
            # Aquí podrías enviar un JSON al servidor
        elif cmd == "list":
            print("[SIMULACIÓN] LIST")
            # Aquí podrías enviar un JSON al servidor
        elif cmd == "set":
            archivo = input("Nombre del archivo a subir: ")
            contenido = input("Contenido: ")
            print(f"[SIMULACIÓN] SET {archivo} -> {contenido}")
            # Aquí podrías enviar un JSON al servidor
        elif cmd == "exit":
            logging.info("Saliendo del programa...")
            stop_event.set()
            break
        else:
            print("Comando no reconocido")

# -----------------------------
# Punto de inicio
# -----------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H','--host', default='localhost')
    parser.add_argument('-p','--port', type=int, default=8080)
    parser.add_argument('-u','--uuid', default=str(uuid.getnode()))
    args = parser.parse_args()

    stop_event = threading.Event()

    # Iniciar hilo del menú interactivo
    threading.Thread(target=command_loop, args=(stop_event,), daemon=True).start()

    # Iniciar conexión al servidor
    subscribe(args.host, args.port, args.uuid, stop_event)
