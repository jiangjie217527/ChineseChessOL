from data import *
from utils import *
from socket import *
import _thread
import time

def control_fun(threadname,delay):
    while True:
        #
        # if state[1]:
        #     cv2.setMouseCallback('ChineseChessOL:B', on)
        #     state[1] = False
        rec = sock.dataSocket.recv(BUFLEN)
        print(rec.decode())
        str_num = rec.decode().split()
        num = []
        for i in range(3):
            num.append(int(str_num[i]))
        R_pieces_cordinate[num[0]][0] = num[1]
        R_pieces_cordinate[num[0]][1] = num[2]
        for i in range(16):
            if active_B[i] and R_pieces_cordinate[num[0]] == B_pieces_cordinate[i]:
                active_B[i] = False
                break
        state[1]= True
        time.sleep(delay)

def on(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and state[0]:
        for i in range(16):
            if black_hit_pieces(x,y,i):
                img = black_select(i)
                destination.clear()
                black_indicate(i,img)
                sel[0] = i
                cv2.imshow('ChineseChessOL:B', img)
                break
        for d in destination:
            if black_hit_block(x, y, d):
                sock.dataSocket.send((str(sel[0])+' '+str(d[0])+' '+str(d[1])).encode())
                cv2.setMouseCallback('ChineseChessOL:B', do_nothing_B)
                state[1] = False
                B_pieces_cordinate[sel[0]][0] = d[0]
                B_pieces_cordinate[sel[0]][1] = d[1]
                for i in range(16):
                    if active_R[i] and R_pieces_cordinate[i] == d:
                        active_R[i] = False
                        break
                img = black_select(-1)
                if active_B[0] is False or active_R[0] is False:
                    cv2.putText(img, "end", (400, 400), cv2.FONT_HERSHEY_COMPLEX, 1.0, (200, 50, 50), 2)
                    state[0] = False
                cv2.imshow('ChineseChessOL:B', img)
                break


def do_nothing_B(event, x, y, flags, param):
    if state[1]:
        img = black_select(-1)
        cv2.imshow('ChineseChessOL:B',img)
        cv2.setMouseCallback('ChineseChessOL:B', on)
def black_init():
    state[1] = False
    for i in range(16):
        R_pieces[i] = cv2.resize(R_pieces[i], (50, 50))
        B_pieces[i] = cv2.resize(B_pieces[i], (50, 50))
        R_pieces_s[i] = cv2.resize(R_pieces_s[i], (50, 50))
        B_pieces_s[i] = cv2.resize(B_pieces_s[i], (50, 50))
        img[cordinate_y[black_pieces_cordinate_y_R(i)] - int(h / 2):cordinate_y[black_pieces_cordinate_y_R(i)] + int(h / 2),
        cordinate_x[black_pieces_cordinate_x_R(i)] - int(w / 2):cordinate_x[black_pieces_cordinate_x_R(i)] + int(w / 2)] = \
        R_pieces[i]
        img[cordinate_y[black_pieces_cordinate_y(i)] - int(h / 2):cordinate_y[black_pieces_cordinate_y(i)] + int(h / 2),
        cordinate_x[black_pieces_cordinate_x(i)] - int(w / 2):cordinate_x[black_pieces_cordinate_x(i)] + int(w / 2)] = \
        B_pieces[i]
    cv2.imshow("ChineseChessOL:B",img)
    try:
        _thread.start_new_thread(control_fun,("threadB",0.1))
    except:
        print("err")

def black_play():
    black_init()
    cv2.setMouseCallback('ChineseChessOL:B', do_nothing_B)
    cv2.waitKey(0)
    cv2.destroyAllWindows()