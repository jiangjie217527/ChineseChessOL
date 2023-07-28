import cv2
from data import *
from utils import *
from socket import *
import _thread
import time


def control_fun(threadname,delay):
    while True:
        # if state[1]:
        #     cv2.setMouseCallback('ChineseChessOL:R', on)
        #     state[1] = False
        rec = sock.dataSocket.recv(BUFLEN)
        print(rec.decode())
        str_num = rec.decode().split()
        num = []
        for i in range(3):
            num.append(int(str_num[i]))
        B_pieces_cordinate[num[0]][0] = num[1]
        B_pieces_cordinate[num[0]][1] = num[2]
        for i in range(16):
            if active_R[i] and B_pieces_cordinate[num[0]] == R_pieces_cordinate[i]:
                active_R[i] = False
                break
        time.sleep(delay)
        state[1] = True


def on(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and state[0]:
        # xy= "%d %d"%(x,y)
        # print(x, y)
        for i in range(16):
            if red_hit_pieces(x, y, i):
                img = red_select(i)
                destination.clear()
                red_indicate(i, img)
                sel[0] = i
                cv2.imshow('ChineseChessOL:R', img)
                break
        for d in destination:
            if red_hit_block(x,y,d):
                cv2.setMouseCallback('ChineseChessOL:R',do_nothing_R)
                state[1] = False
                sock.dataSocket.send((str(sel[0])+' '+str(d[0])+' '+str(d[1])).encode())
                R_pieces_cordinate[sel[0]][0] = d[0]
                R_pieces_cordinate[sel[0]][1] = d[1]
                for i in range(16):
                    if active_B[i] and B_pieces_cordinate[i] == d:
                        active_B[i] = False
                        break
                img = red_select(-1)
                if active_B[0] is False or active_R[0] is False:
                    cv2.putText(img, "end", (400, 400), cv2.FONT_HERSHEY_COMPLEX, 1.0, (200, 50, 50), 2)
                    state[0] = False
                cv2.imshow('ChineseChessOL:R', img)
                break

def do_nothing_R(event, x, y, flags, param):
    if state[1]:
        img = red_select(-1)
        cv2.imshow('ChineseChessOL:R', img)
        cv2.setMouseCallback('ChineseChessOL:R', on)
def red_init():
    state[1] = False
    for i in range(16):
        R_pieces[i] = cv2.resize(R_pieces[i], (50, 50))
        B_pieces[i] = cv2.resize(B_pieces[i], (50, 50))
        R_pieces_s[i] = cv2.resize(R_pieces_s[i], (50, 50))
        B_pieces_s[i] = cv2.resize(B_pieces_s[i], (50, 50))
        img[cordinate_y[R_pieces_cordinate[i][1]] - int(h / 2):cordinate_y[R_pieces_cordinate[i][1]] + int(h / 2),
        cordinate_x[R_pieces_cordinate[i][0]] - int(w / 2):cordinate_x[R_pieces_cordinate[i][0]] + int(w / 2)] = \
        R_pieces[i]
        img[cordinate_y[B_pieces_cordinate[i][1]] - int(h / 2):cordinate_y[B_pieces_cordinate[i][1]] + int(h / 2),
        cordinate_x[B_pieces_cordinate[i][0]] - int(w / 2):cordinate_x[B_pieces_cordinate[i][0]] + int(w / 2)] = \
        B_pieces[i]
    cv2.imshow("ChineseChessOL:R",img)
    try:
        _thread.start_new_thread(control_fun,("threadR",0.1))
    except:
        print("err")


def red_play():
    red_init()
    cv2.setMouseCallback('ChineseChessOL:R', on)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
