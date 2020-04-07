import socket
import threading
import argparse


def serve_client(socket, ip_address, port):
    clientRequest = socket.recv(4096)
    print(f"[!] Received data from the client ({ip_address}:{port}):{clientRequest}")

    # reply back to client with a response
    socket.send("I am a server response, my version is 3.2".encode('utf-8'))
    # We're done close the client socket
    socket.close()


def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(10)
    print("[!] Listening locally on port %d ..." % port)

    while True:
        client, address = server.accept()
        print("[+] Connected with the client: %s:%d" % (address[0], address[1]))

        # Handle clients through multi-threading
        # serveClientThread = threading.Thread(target=serve_client, args=(client, address[0], address[1]))
        # serveClientThread.start()
        serve_client(client, address[0], address[1])


def main():
    parser = argparse.ArgumentParser('TCP server')
    parser.add_argument("-p", "--port", type=int, help="The port number to connect with", default=4444)
    args = parser.parse_args()

    portNumber = args.port

    start_server(portNumber)


if __name__ == "__main__":
    main()
