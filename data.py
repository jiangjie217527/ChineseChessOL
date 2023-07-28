import cv2
from socket import *

cordinate_x = [84,
               162,
               240,
               318,
               396,
               474,
               552,
               630,
               708
               ]
cordinate_y = [48,
               126,
               204,
               282,
               360,
               440,
               518,
               596,
               674,
               752
               ]

img = cv2.imread('pad_800.jpg')
R_shuai = cv2.imread('R_shuai.png')
R_bin = cv2.imread('R_bin.png')
R_ju = cv2.imread('R_ju.png')
R_ma = cv2.imread('R_ma.png')
R_pao = cv2.imread('R_pao.png')
R_shi = cv2.imread('R_shi.png')
R_xiang = cv2.imread('R_xiang.png')

B_jiang = cv2.imread('B_jiang.png')
B_zu = cv2.imread('B_zu.png')
B_ju = cv2.imread('B_ju.png')
B_ma = cv2.imread('B_ma.png')
B_pao = cv2.imread('B_pao.png')
B_shi = cv2.imread('B_shi.png')
B_xiang = cv2.imread('B_xiang.png')

R_shuai_s = cv2.imread('R_shuai_s.png')
R_bin_s = cv2.imread('R_bin_s.png')
R_ju_s = cv2.imread('R_ju_s.png')
R_ma_s = cv2.imread('R_ma_s.png')
R_pao_s = cv2.imread('R_pao_s.png')
R_shi_s = cv2.imread('R_shi_s.png')
R_xiang_s = cv2.imread('R_xiang_s.png')

B_jiang_s = cv2.imread('B_jiang_s.png')
B_zu_s = cv2.imread('B_zu_s.png')
B_ju_s = cv2.imread('B_ju_s.png')
B_ma_s = cv2.imread('B_ma_s.png')
B_pao_s = cv2.imread('B_pao_s.png')
B_shi_s = cv2.imread('B_shi_s.png')
B_xiang_s = cv2.imread('B_xiang_s.png')

R_pieces_cordinate = [
    [4, 9],
    [0, 6],
    [2, 6],
    [4, 6],
    [6, 6],
    [8, 6],
    [0, 9],
    [8, 9],
    [1, 9],
    [7, 9],
    [1, 7],
    [7, 7],
    [3, 9],
    [5, 9],
    [2, 9],
    [6, 9]
]

B_pieces_cordinate = [
    [4, 0],
    [0, 3],
    [2, 3],
    [4, 3],
    [6, 3],
    [8, 3],
    [0, 0],
    [8, 0],
    [1, 0],
    [7, 0],
    [1, 2],
    [7, 2],
    [3, 0],
    [5, 0],
    [2, 0],
    [6, 0]
]

# 1将2卒3车4马5炮6士7相

tp = [
    1,
    2,
    2,
    2,
    2,
    2,
    3,
    3,
    4,
    4,
    5,
    5,
    6,
    6,
    7,
    7
]

move_1 = [[1, 0], [-1, 0], [0, 1], [0, -1]]

move_2 = [[1, 0], [-1, 0], [0, -1]]

move_4 = [[1, 2], [2, 1], [-1, 2], [2, -1], [1, -2], [-2, 1], [-1, -2], [-2, -1]]

unaccess_ma = [[0,1],[1,0],[0,1],[1,0],[0,-1],[-1,0],[0,-1],[-1,0]]

move_6 = [[-1, -1], [1, -1], [1, 1], [-1, 1]]

R_pieces = [R_shuai,
            R_bin,
            R_bin,
            R_bin,
            R_bin,
            R_bin,
            R_ju,
            R_ju,
            R_ma,
            R_ma,
            R_pao,
            R_pao,
            R_shi,
            R_shi,
            R_xiang,
            R_xiang
            ]

B_pieces = [B_jiang,
            B_zu,
            B_zu,
            B_zu,
            B_zu,
            B_zu,
            B_ju,
            B_ju,
            B_ma,
            B_ma,
            B_pao,
            B_pao,
            B_shi,
            B_shi,
            B_xiang,
            B_xiang,
            ]
R_pieces_s = [R_shuai_s,
              R_bin_s,
              R_bin_s,
              R_bin_s,
              R_bin_s,
              R_bin_s,
              R_ju_s,
              R_ju_s,
              R_ma_s,
              R_ma_s,
              R_pao_s,
              R_pao_s,
              R_shi_s,
              R_shi_s,
              R_xiang_s,
              R_xiang_s
              ]

B_pieces_s = [B_jiang_s,
              B_zu_s,
              B_zu_s,
              B_zu_s,
              B_zu_s,
              B_zu_s,
              B_ju_s,
              B_ju_s,
              B_ma_s,
              B_ma_s,
              B_pao_s,
              B_pao_s,
              B_shi_s,
              B_shi_s,
              B_xiang_s,
              B_xiang_s
              ]

active_R = [True] * 16
active_B = [True] * 16

block_size = 16

block = cv2.imread('block.png')
block = cv2.resize(block, (block_size, block_size))

w = 50

h = 50

destination = []
sel = [0]

state = [True] * 2

PORT = 50000

BUFLEN = 512

IP = '106.54.224.13'


class sock:
    dataSocket = socket(AF_INET, SOCK_STREAM)

