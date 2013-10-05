import socket
import sys
import time

HOST, PORT = "localhost", 1337
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    while (1==1):
        sock.sendall(data + "\n")

        # Receive data from the server and shut down
        received = str(sock.recv(1024))
        sys.sleep(1000);
finally:
    sock.close()

print("Sent:     {}".format(data))
print("Received: {}".format(received))