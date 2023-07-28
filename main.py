import random
import red_player
import black_plater
from data import sock,IP,PORT,BUFLEN
from socket import *

sock.dataSocket = socket(AF_INET,SOCK_STREAM)

sock.dataSocket.connect((IP,PORT))

rec = sock.dataSocket.recv(BUFLEN)

print('连接信息为：',rec.decode())

rec = sock.dataSocket.recv(BUFLEN)

print('执棋情况为：',rec.decode())

sock.dataSocket.send(f'got it'.encode())

check = sock.dataSocket.recv(BUFLEN)

if check.decode() == 'r':
    red_player.red_play()
else:
    black_plater.black_play()

sock.dataSocket.close()