import socket
import threading
import resp
from handler import Handlers  # Remove SETsMu, HSETsMu
from aof import AOF

def handle_client_connection(client_socket, aof_handler):
    try:
        while True:
            request = client_socket.recv(1024)
            if not request:
                break

            try:
                value,_ = resp.read(request)
            except ValueError as e:
                client_socket.send(resp.marshal(resp.Value(typ="error", str_value=str(e))))
                continue

            if value.typ != "array":
                client_socket.send(resp.marshal(resp.Value(typ="error", str_value="Invalid request, expected array")))
                continue

            if len(value.array) == 0:
                client_socket.send(resp.marshal(resp.Value(typ="error", str_value="Invalid request, expected array length > 0")))
                continue

            command = value.array[0].bulk.upper()
            args = value.array[1:]

            if command in ("SET", "HSET"):
                aof_handler.write(value)

            if command in Handlers:
                result = Handlers[command](args)
            else:
                result = resp.Value(typ="error", str_value=f"Unknown command '{command}'")

            client_socket.send(resp.marshal(result))

    except ConnectionResetError:
        print(f"Connection reset by peer")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        client_socket.close()

def main():
    print("Listening on port 6380")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 6380))
    server.listen(5)

    aof_handler = AOF("database.aof")
    aof_handler.read(lambda value: Handlers[value.array[0].bulk.upper()](value.array[1:]))

    try:
        while True:
            client_sock, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client_connection, args=(client_sock, aof_handler))
            client_handler.start()
    except KeyboardInterrupt:
        server.close()
        aof_handler.close()

if __name__ == "__main__":
    main()
