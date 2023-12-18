#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import threading
from typing import Optional


def serve_client(client_socket: socket.socket) -> None:
    """
    1. receives from the client,
    2. extracts the hostname and port from its request,
    3. forwards the message unchanged to the remote,
    4. receives a response from the remote by calling receive_response,
    5. sends that message back to the client
    6. Close the out_socket at the end of the request
    """
    header = receive_header(client_socket)
    extracted_hostname = extract_hostname(header)

    if extracted_hostname is not None:
        hostname, port = extracted_hostname
        # create out socket, send message to server and client
        out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out_socket.connect((socket.gethostbyname(hostname.decode()), port))
        out_socket.send(header)
        response = receive_response(out_socket)
        client_socket.send(response)

        # close client and server sockets
        out_socket.close()
        client_socket.close()


def receive_header(sock: socket.socket) -> bytes:
    """
    receives from the socket until either:
    a HTTP header is received,
    or the socket is closed.
    """
    socket = sock.recv(1024)
    return socket


def extract_hostname(message: bytes) -> Optional[tuple[bytes, int]]:
    """
    Extracts the hostname and port from the HTTP header's Host field,
    and returns them as a tuple (hostname, port).
    Does not decode the hostname (leaves it as bytes)
    If no port is specified, it assumes the port is 80
    If no hostname is present, it returns None
    """
    hostname = None
    port = 80
    decoded_header = message.decode()
    header_lines = decoded_header.splitlines()

    # look for line beginning w/ host, return
    for line in header_lines:
        if "Host:" in line:
            combined_str = line.split()[1]

            # split hostname and port string by :
            hostname_and_port = combined_str.split(":")

            hostname = hostname_and_port[0].encode()

            # if :port# in string, change port to the second line
            if len(hostname_and_port) == 2:
                port = int(hostname_and_port[1])

            return (hostname, port)

    return None


def receive_response(out_socket: socket.socket) -> bytes:
    """
    Receives the messages from the out_socket,
    and sends them to the client_socket.
    Receives HTTP message from the out_socket
    (HTTP request must already be sent by caller)
    Receive until the content is fully transmitted
    Return the message in full
    """

    # keep adding items from the byte string until you get until you get to the end of the byte string
    response = []
    while True:
        new_data = out_socket.recv(4096)
        if new_data == b"":
            break
        response.append(new_data)
    return b"".join(response)


def main() -> None:
    """
    Creates the proxy server's main socket and binds to it.
    With each new client that connects,
    serves their requests.
    This one is done for you.
    """
    # create the server socket, a TCP socket on localhost:6789
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("", 6789))

    # listen for connections
    server_sock.listen(20)

    # forever accept connections
    # thread list is never cleaned (this is a vulnerability)
    threads = []
    while True:
        client_sock, addr = server_sock.accept()
        threads.append(threading.Thread(target=serve_client, args=(client_sock,)))
        threads[-1].start()


if __name__ == "__main__":
    main()
