###Name- Saba Ruhee Jagirdar
###ID- 1001848512
import socket
import argparse
# An object of argparse
my_parser = argparse.ArgumentParser()
# Strings on command line and  turn them into objects.
my_parser.add_argument('-lock',
                       type=int,
                       help="lock a file using index",nargs="?")
#add parser arguments for lock and unlock
my_parser.add_argument('-unlock',
                       type=int,
                       help="unlock a file using index",nargs="?")
args = my_parser.parse_args()
#print and find argument values
#print(args.lock)
#print(args.unlock)

# socket module facilitates socket programming
# https://www.ibm.com/docs/en/i/7.3?topic=programming-how-sockets-work
# I have referred the abo ve document to understand the process of socket
socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# https://www.youtube.com/watch?app=desktop&v=Lbfe3-v7yE0
# AF_INET indicates that we are using ipv4 and SOCK_STREAM indicates TCP protocol
socketClient.connect(('localhost',5633))
to_send = "Hello"
# Test with to_send Hello
if args.lock:
    to_send = "lock " + str(args.lock)
elif args.unlock:
    to_send = "unlock " + str(args.unlock)
# Send the arguments to use encode
socketClient.send(to_send.encode())

#connect API allows to connect to the server at port 5123
print(socketClient.recv(2048).decode())
# Print the data received
