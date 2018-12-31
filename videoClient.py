import os
import pickle
import socket
import struct
import numpy as np
import cv2

# Soket üzerinden yayınlanacak video dosyasını seç
file_to_share = 'Kodla18 Kısa Film.mp4'

# Ana bilgisayarı ve bağlantı noktasını başlat
host = '192.168.43.47'
port = 5005

# İstemci soket bağlantısını tanımla
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Ana bilgisayara bağlan
clientsocket.connect((host,port))

# Sunucuya bağlantı onayı gönder
clientsocket.send(bytes(clientsocket.getsockname()[0], 'utf-8'))

# Yanıtı al
first_response = clientsocket.recv(1024).decode('utf-8')
print(f'[BİLGİ]: {first_response} host sahibine {host}:{port}')

# Videonun boyutunu sunucuya gönder ve yanıt al
filesize = bytes(str(os.path.getsize(file_to_share)),'utf-8')
clientsocket.send(filesize)

second_response = clientsocket.recv(1024).decode('utf-8')
print(f'[MESAJ]: {second_response}')

# videoyu al
cap = cv2.VideoCapture(file_to_share)

# Video dosyası / web kamerası çerçevelerini okuyun
while True:

    ret,frame = cap.read()

    # verileri bayt dizisine dönüştürme
    data = pickle.dumps(frame)
    
    # Sunucuya gönder
    clientsocket.send(struct.pack("L", len(data))+data)
