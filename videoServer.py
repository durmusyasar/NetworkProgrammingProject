import cv2
import pickle
import numpy as np
import socket
import struct


# Ana bilgisayarı ve bağlantı noktasını tanımla
host='192.168.43.47'
port=5005

# Soketi tanımlama
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # TCP

# Ana bilgisayarı bağlantı noktasına bağlama
s.bind((host,port))

# Sunucunun bağlantı noktasını dinlemesini sağlama {port_id}
s.listen(1)
print(f'[BİLGİ]: Sunucu bağlantı noktasında dinliyor {port}.')

# İstemci bağlanana kadar bekle
conn,addr=s.accept()

# Mesajı al
first_msg = conn.recv(1024).decode('utf-8')
print(f'[BİLGİ]: Yeni bağlantı {first_msg}')

# Cevap gönder
conn.send(b'Baglanti kabul edildi.')

# Gelen videonun boyutunu al
video_size = int(conn.recv(1024).decode('utf-8'))
video_size = struct.calcsize("L")

# Boş bayt dizisini başlat. Video akışının baytları ile doldurulacak
data = b""
print(f'[BİLGİ]: İstemciden video akışı için hazır')

# İstemciye bir cevap gönder
conn.send(bytes(f'Sunucu boyutu video akışı için hazır {video_size}', 'utf-8'))

# Video akışını almaya başla
while True:

    # Alınan verilerin boyutu video boyutuna eşit olana kadar veri alın
    while len(data) < video_size:
        # İstemciden video akışı ile bayt dizisini güncelle
        data += conn.recv(4096)

    # Bayt dizisini böl
    packed_msg_size = data[:video_size]
    data = data[video_size:]

    # Tek bir çerçevenin boyutunu alın
    msg_size = struct.unpack("L", packed_msg_size)[0]
    
    # Tek çerçeveyi al
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Çerçeveyi bayt tipinden dönüştür
    frame = pickle.loads(frame_data)
    # Videonun istemciden karesini göster
    cv2.imshow('frame',frame)
    cv2.waitKey(1)
