import cv2
import numpy as np
import socket


host = '127.0.0.1'
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

cap = cv2.VideoCapture(0)
# Video dosyası / web kamerası çerçevelerini okuyun

while True:
    s, frame = cap.read()

    frame = cv2.flip(frame,1)

    cv2.imshow('caption',frame)
    
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
