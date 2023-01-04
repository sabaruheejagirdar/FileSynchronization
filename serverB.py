###Name- Saba Ruhee Jagirdar
###ID- 1001848512
import socket
# https://www.youtube.com/watch?app=desktop&v=u4kr7EFxAKk
# socket module facilitates socket programming
import os
# https://www.geeksforgeeks.org/python-os-stat-method/
# os module allows to use os dependent functionalities
import datetime
#  datetime module allows to convert epoch datetime to local datetime\
from watchdog.observers import Observer
from watchdog.events import  FileSystemEventHandler

from dirsync import sync

# Reference-
socketServer2 = socket.socket()
# by default socket considers--> socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET indicates that we are using ipv4 and SOCK_STREAM indicates TCP protocol
print('Socket created')
# Testing server socket
socketServer2.bind(('localhost',6633))
# Binds server2 to 6123 port
socketServer2.listen(50)
# listen() API allows specified connections with server allowed
print('Waiting for Client to get connected!')
dirBasePath = 'D:\Semester 1\CSE 5306 DS\lab3_DS\Directory_B\\'
# Created directory_b(at above location)
# While executing this program on any other machine, make sure to update the dirBasePath
target_path = "D:\Semester 1\CSE 5306 DS\lab3_DS\Directory_B\\"
source_path = "D:\Semester 1\CSE 5306 DS\lab3_DS\Directory_A\\"

# https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/
class Handler(FileSystemEventHandler):
# Handler is an obect which notifies when a change of event happens

    @staticmethod
    #staticmethod doesnt require the implicit arguments
    def on_any_event(event):
        #on_any_event is executed whenever any event happens
        strObject = event.src_path
        #store the path
        indexOfLastSlash = strObject.rfind('\\') + 1
        # In the file path find // and get the last slashes
        eventfileName = strObject[indexOfLastSlash:]
        # Store the name of file post eventfileName

        # check for events
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            print("File has been created in Server-B - % s." % eventfileName)
        #if new file is created then pop up in the console
        elif event.event_type == 'modified':
            print("File has been modified in Server-B - % s." % eventfileName)
        #if modified then popup in the console
        elif event.event_type == 'deleted':
            delete_file_name = target_path + "\\" + eventfileName
            if os.path.exists(delete_file_name):
                os.remove(delete_file_name)
                print("File has been deleted in Server-B - % s." % eventfileName)
            else:
                print(delete_file_name + " - This file was not found or was deleted from another server instance")
        #Run this when the file is deleted

observer = Observer()
# Observer detects the file system changes
event_handler = Handler()
observer.schedule(event_handler, source_path, recursive=False)
# schedules watching the path
observer.start()

while True:
    # Accept the client request, while this server is on
    sync(target_path, source_path, 'sync')
    socketServer, addr = socketServer2.accept()
    # accept() API accepts the client connection and provides the socket object and address info
    listFiles = os.listdir(dirBasePath)
    # os.listdir(dirBasePath)--> Lists all files present in dirBasePath directory, into list
    # print("listFiles -->",listFiles)
    forData2 = []

    # Write a for loop to fetch the metadata of files
    for i in listFiles:
        fileName = dirBasePath + i
        # Get file size
        fileObject = os.stat(fileName)
        # print("fileObject-->", fileObject)
        # os.stat helps to get the status of the specified path
        # fileObject--> os.stat_result(st_mode=33206, st_ino=2814749767560588, st_dev=3962226677, st_nlink=1, st_uid=0,
        # st_gid=0, st_size=142, st_atime=1632704301, st_mtime=1632692620, st_ctime=1632664051)

        # print('Size in bytes-',fileSize.st_size) - 142
        fileSize = fileObject.st_size

        # Get file modified date
        # 1632692620
        fileDate = fileObject.st_mtime
        fileLocalDate = datetime.datetime.fromtimestamp(fileDate).strftime('%Y-%m-%d-%H:%M')
        # print(fileLocalDate)

        fileData = str(i) + " " + str(fileSize) + " " + str(fileLocalDate)
        forData2.append(fileData)
        # finalData = i + " " + fileSize.st_size + " " + fileLocalDate
        # print('final data- ',finalData)
        # print(type(finalData))--> list

    # print('Final data 2',finalData2)
    # Final data ['abc.txt 142 2021-09-26', 'test.txt 140 2021-09-26', 'xyz.txt 150 2021-09-26']
    finalDataInString2 = '\n'.join(forData2)
    # Join- converts the list to string, and this string we'll forward to client
    # target_path = "C:\\Users\\Saba Ruhee\\PycharmProjects\\lab2_jagirdar_saj8512\\directory_b\\"
    # source_path = "C:\\Users\\Saba Ruhee\\PycharmProjects\\lab2_jagirdar_saj8512\\directory_a\\"
    # sync(target_path,source_path,'sync')
    # sync(source_path,target_path,'sync')
    print("Data from Server 2 \n",finalDataInString2)
    # abcd.txt 150 2021-09-26
    # mnop.txt 150 2021-09-26
    # testing.txt 140 2021-09-26
    # print(type(finalDataInString2))--> string

    socketServer.send(finalDataInString2.encode())
    # On request client can get this data, this is an unsorted list
    # Sorting is performed in other server file
    socketServer.close()
    # break
    # close the connection