###Name- Saba Ruhee Jagirdar
###ID- 1001848512
import socket
import portalocker
# socket module facilitates socket programming
import os
# os module allows to use os dependent functionalities
# https://www.geeksforgeeks.org/python-os-stat-method/
import datetime
import win32con
# datetime module allows to convert epoch datetime to local datetime
# installing win32 because of certain dependencies
from dirsync import sync
from watchdog.observers import Observer
# watchdog monitors is any changes are made to the directory
from watchdog.events import  FileSystemEventHandler
# Before using 'from' make sure the corresponding packages are installed

socketServer = socket.socket()
# by default socket considers--> socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET indicates that we are using ipv4 and SOCK_STREAM indicates TCP protocol
print('Socket created')
# Testing Server socket
socketServer.bind(('localhost',5633))
# Binds server to 5123 port number
socketServer.listen(50)
# listen API allows specified connections with server. A maximum of 50 clients can be connected with this server

print('Waiting for Client to get connected!')
dirBasePath = 'D:\Semester 1\CSE 5306 DS\lab3_DS\Directory_A\\'
# created directory_a(at above location)
# For instance, consider there are following files at this location-
# ['xyz.txt', 'abc.txt', 'qwerty.txt']
target_path = "D:\Semester 1\CSE 5306 DS\lab3_DS\Directory_A\\"
source_path = "D:\Semester 1\CSE 5306 DS\lab3_DS\Directory_B\\"

# Stores the files that has been locked
locked_files = []

# Make sure sync is stopped when file is locked.
def lock(file_name):
    os.chmod(target_path + "\\" + file_name,0o444)
    locked_files.append(file_name)
    print("file locked ",file_name)
# define the unlocking mechanism
def unlock(file_name):
    os.chmod(target_path + "\\" + file_name,0o777)
    locked_files.remove(file_name)

# Fetch index of the files has lock and unlock instructions.
def get_file_name_from_index(index):
    print(index)
    dira = os.listdir(target_path)
    for i in dira:
        file_index = dira.index(i)
        print(file_index)
        print(str(i))
        if file_index == index:
            return str(i)

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
    socketClient, addr = socketServer.accept()
    # print('Connected with', addr)

    # Checking for index from client_msg
    message = socketClient.recv(1024).decode()
    if message.startswith("unlock"): 
        file_name = get_file_name_from_index(int(message.split(" ")[1]))
        print("unlock ",file_name)
        unlock(file_name)
    elif message.startswith("lock"):
        file_name = get_file_name_from_index(int(message.split(" ")[1]))
        print("lock ",file_name)
        # If instruction is to lock, lock() is used from portalocker to lock the file.
        lock(file_name)
    sync(target_path, source_path, 'sync')

    listFiles = os.listdir(dirBasePath)
    # os.listdir(dirBasePath)--> Lists all files present in dirBasePath directory, into list
    # print(listFiles)
    # print(type(listFiles))--> list
    # listFiles --> ['xyz.txt', 'abc.txt', 'qwerty.txt']
    forData = []
    # forData--> stores the output of 'for loop', which has the meta data of files(Name, File size, Modified date)

    # using for loop, extract metadata of every file
    for i in listFiles:
        index_dir = listFiles.index(i)
        #print("heree!!")
        #print(index_dir)
        fileName = dirBasePath + i
        # print('Filename-', i)

        # Get file size
        fileObject = os.stat(fileName)
        # os.stat helps to get the status of the specified path
        # fileObject--> os.stat_result(st_mode=33206, st_ino=2814749767560588, st_dev=3962226677, st_nlink=1, st_uid=0,
        # st_gid=0, st_size=142, st_atime=1632704301, st_mtime=1632692620, st_ctime=1632664051)

        # print('Size in bytes-',fileSize.st_size) - 142
        fileSize = fileObject.st_size

        # Get file modified date
        # 1632692620
        fileDate = fileObject.st_mtime
        fileLocalDate = datetime.datetime.fromtimestamp(fileDate).strftime('%Y-%m-%d-%H:%M')
        # https://stackoverflow.com/questions/12400256/converting-epoch-time-into-the-datetime
        # print(fileLocalDate)

        fileData = '['+str(listFiles.index(i))+']'+" " + i + " " +str(fileSize)+" "+"Bytes"+ " "+str(fileLocalDate)

        if i in locked_files:
            fileData = fileData + " <locked>"

        # fileData = str(i) + " " + str(fileSize) + " " + str(fileLocalDate)
        forData.append(fileData)
        # finalData = i + " " + fileSize.st_size + " " + fileLocalDate
        # print('final data- ',finalData)
        # print(type(finalData))--> list

    # print('For loop output',forData)
    # forData--> ['xyz.txt 142 2021-09-26', 'abc.txt 140 2021-09-26', 'qwerty.txt 150 2021-09-26']

    # LOGIC-
    # At this point I have data of serverA(this server file) in the form of list
    # while the data that I have received from serverB is in string.
    # 1. Convert the data of serverA, from list to string(for concatenation)
    # 2. Concatenate both the strings
    # 3. Split the list at new line(using splitlines), this converts the string to list
    # 4. Apply the sort() method on the concatenated list
    # 5. Post sorting, convert the list to string
    # 6. Send the string to the client


    # connect to server2
    s2 = socket.socket()
    # print("Socket creation in progress!!!!")
    s2.connect(('localhost', 6633))
    # print("Socket creation is completed!!!!")
    data = s2.recv(2048).decode()
    # print("Data received",dataFromS2)
    # dataFromS2 is in string    

    # Convert this servers output also to a string, which break after \n
    dataFromS1 = '\n'.join(forData)
    # https://www.programiz.com/python-programming/methods/string/join
    # Join- converts the list to string
    print("Data from Server 1(Unsorted)",dataFromS1)

    concatenate_s1s2 = dataFromS1 +"\n"
    # concatenate_s1s2 = dataFromS1 +"\n"+ dataFromS2
    # print("concatenate_s1s2",concatenate_s1s2)
    # print(type(concatenate_s1s2))
    # concatenate_s1s2.splitlines()

    # Convert the string to list(so that sorting method could be applied)
    # .splitlines()--> Converts the string to lists, while splitting at \n
    # concatenate_s1s2 is in string, convert it to list, so that .sort() could be applied
    strToList = concatenate_s1s2.splitlines()
    # https://stackoverflow.com/questions/24237524/how-to-split-a-python-string-on-new-line-characters
    # print("String To List",strToList)
    # print(type(strToList))
    # strToList.sort()
    # .sort() is case sensitive, therefore use sorted
    sorted_list = sorted(strToList, key=str.casefold)
    # https://stackoverflow.com/questions/10269701/case-insensitive-list-sorting-without-lowercasing-the-result
    # The list is sorted, irrespective of case
    print("Sorted list",sorted_list)




    # Convert the sorted list to string
    concatenate_str = "\n".join(sorted_list)
    print("Sorted listing(both of the servers) \n",concatenate_str)

    socketClient.send(concatenate_str.encode())
    # concatenate_str--> contains the sorted filenames(along with metadata) of both the servers, as string
    socketClient.close()
    # break
    # close the connection
