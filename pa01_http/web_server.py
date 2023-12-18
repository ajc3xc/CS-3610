#!/usr/bin/pyt	hon3
# -*- coding: utf-8 -*-
"""
A simple Web server.
GET requests must name a specific file,
since it does not assume an index.html.
"""

import socket
import threading
import time


def handler(conn_socket: socket.socket, address: tuple[str, int]) -> None:
    """
    Handles the part of the client work-flow that is client-dependent,
    and thus may be delayed by the user, blocking program flow.
    """
    try:
        # Receives the request message from the client
        # Delete pass and write
        sentence = conn_socket.recv(1024)

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        # Delete pass and write
        decoded_sentence = sentence.decode()
        path_to_file = decoded_sentence.split()[1][
            1:
        ]  # should be 2nd word in request string

        # Because the extracted path of the HTTP request includes
        # a character '\', we read the path from the second character
        # Read file off disk, to send
        # Store the content of the requested file in a temporary buffer
        # Delete pass and write
        file = open(path_to_file, "rb")
        fileContent = file.read()
        file.close()

        # Send the HTTP response header line to the connection socket
        # Delete pass and write
        response_string = "HTTP/1.1 200 OK\r\n\r\n"
        response_binary = response_string.encode()
        conn_socket.send(response_binary)

        # Send the content of the requested file to the connection socket
        # Delete pass and write
        conn_socket.send(fileContent)

    except IOError:
        # Send HTTP response message for file not found (404)
        # Delete pass and write
        error_string = "HTTP/1.1 404 File Not Found\r\n\r\n"
        error_binary = error_string.encode()
        conn_socket.send(error_binary)

        # Open file, store the content of the requested file in a temporary buffer (variable).
        # Delete pass and write
        invalid_path_to_file = "web_files/not_found.html"
        invalidFile = open(invalid_path_to_file, "rb")
        invalidFileContent = invalidFile.read()
        invalidFile.close()

        # Send the content of the requested file to the connection socket
        # Delete pass and write
        conn_socket.send(invalidFileContent)

    except:
        print("Bad request")
    finally:
        conn_socket.close()


def main() -> None:
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_port = 6789

    # Bind the socket to server address and server port
    # Delete pass and write
    server_socket.bind(("", server_port))

    # Listen to at most 2 connection at a time
    # Server should be up and running and listening to the incoming connections
    # Delete pass and write
    server_socket.listen(2)  # this may need to be changed to 1

    threads = []
    try:
        while True:
            # Set up a new connection from the client
            # Delete pass and write
            # this has a cooldown of a minute. And it resets every time you try to run it again.
            clientSocket, clientAddress = server_socket.accept()

            # call handler here, start any threads needed
            # Delete pass and write
            client_thread = threading.Thread(
                target=handler,
                args=(
                    clientSocket,
                    clientAddress,
                ),
                name="client_thread" + str(time.time()),
            )
            client_thread.start()

            # Just to keep track of threads
            threads.append(client_thread)
    except Exception as e:
        print("Exception occured (maybe you killed the server)")
        print(e)
    except:
        print("Exception occured (maybe you killed the server)")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
