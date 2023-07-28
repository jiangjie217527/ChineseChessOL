from data import *
import cv2

def red_check_jiang(xx, yy, id):
    jiang_x = B_pieces_cordinate[0][0]
    jiang_y = B_pieces_cordinate[0][1]
    if R_pieces_cordinate[id][0] != jiang_x or jiang_x != R_pieces_cordinate[0][0]:
        return True
    for j in range(1, 10):
        detect_jiang_y = R_pieces_cordinate[0][1] - j
        if jiang_y == detect_jiang_y:
            return False
        for i in range(16):
            if active_R[i] is False:
                continue
            x = R_pieces_cordinate[i][0]
            y = R_pieces_cordinate[i][1]
            if i == id:
                x = xx
                y = yy
            if x == jiang_x and detect_jiang_y == y:
                return True
        for i in range(16):
            if active_B[i] is False:
                continue
            x = B_pieces_cordinate[i][0]
            y = B_pieces_cordinate[i][1]
            if x == jiang_x and detect_jiang_y == y:
                return True


def black_check_jiang(xx,yy,id):
    shuai_x = R_pieces_cordinate[0][0]
    shuai_y = R_pieces_cordinate[0][1]
    if B_pieces_cordinate[id][0] != shuai_x or shuai_x != B_pieces_cordinate[0][0]:
        return True
    for j in range(1, 10):
        detect_jiang_y = B_pieces_cordinate[0][1] + j
        if shuai_y == detect_jiang_y:
            return False
        for i in range(16):
            if active_R[i] is False:
                continue
            x = R_pieces_cordinate[i][0]
            y = R_pieces_cordinate[i][1]
            if x == shuai_x and detect_jiang_y == y:
                return True
        for i in range(16):
            if active_B[i] is False:
                continue
            x = B_pieces_cordinate[i][0]
            y = B_pieces_cordinate[i][1]
            if i == id:
                x = xx
                y = yy
            if x == shuai_x and detect_jiang_y == y:
                return True

def check_block(xx, yy):
    for j in range(16):
        if (active_R[j] and R_pieces_cordinate[j][0] == xx and R_pieces_cordinate[j][1] == yy) or (
                active_B[j] and B_pieces_cordinate[j][0] == xx and B_pieces_cordinate[j][1] == yy):
            return False
    if xx < 0 or xx > 8 or yy < 0 or yy > 9:
        return False
    return True


def check_black(xx, yy):
    for j in range(16):
        if active_B[j] and B_pieces_cordinate[j][0] == xx and B_pieces_cordinate[j][1] == yy:
            return True
    return False


def check_red(xx, yy):
    for j in range(16):
        if active_R[j] and R_pieces_cordinate[j][0] == xx and R_pieces_cordinate[j][1] == yy:
            return True
    return False


def r_check(xx, yy):
    for j in range(16):
        if active_R[j] and R_pieces_cordinate[j][0] == xx and R_pieces_cordinate[j][1] == yy:
            return False
    if xx < 0 or xx > 8 or yy < 0 or yy > 9:
        return False
    return True


def b_check(xx,yy):
    for j in range(16):
        if active_B[j] and black_pieces_cordinate_x(j) == xx and black_pieces_cordinate_y(j) == yy:
            return False
    if xx < 0 or xx > 8 or yy < 0 or yy > 9:
        return False
    return True

def red_indicate_1(id, x, y, local_img):
    for i in range(4):
        xx = x + move_1[i][0]
        yy = y + move_1[i][1]
        flag = r_check(xx,yy)
        if B_pieces_cordinate[0][0] == xx:
            for j in range(1, 10):
                detect_jiang_y = yy - j
                if B_pieces_cordinate[0][1] == detect_jiang_y:
                    flag = False
                    break
                if check_block(xx, detect_jiang_y) == False:
                    break
        if flag:
            local_img[cordinate_y[yy] - int(block_size / 2):cordinate_y[yy] + int(block_size / 2),
            cordinate_x[xx] - int(block_size / 2):cordinate_x[xx] + int(block_size / 2)] = block
            destination.append([xx, yy])


def red_indicate_2(id, x, y, local_img):
    if y > 4:
        xx = x
        yy = y - 1
        if r_check(xx, yy):
            local_img[cordinate_y[yy] - int(block_size / 2):cordinate_y[yy] + int(block_size / 2),
            cordinate_x[xx] - int(block_size / 2):cordinate_x[xx] + int(block_size / 2)] = block
            destination.append([xx, yy])
    else:
        for i in range(3):
            xx = x + move_2[i][0]
            yy = y + move_2[i][1]
            if r_check(xx, yy) and red_check_jiang(xx, yy, id):
                local_img[cordinate_y[yy] - int(block_size / 2):cordinate_y[yy] + int(block_size / 2),
                cordinate_x[xx] - int(block_size / 2):cordinate_x[xx] + int(block_size / 2)] = block
                destination.append([xx, yy])


def red_indicate_3(id, x, y, local_img):
    direction = [True] * 4
    for i in range(1, 10):
        for j in range(4):
            xx = x + move_1[j][0] * i
            yy = y + move_1[j][1] * i
            if red_check_jiang(xx, yy, id) is False:
                continue
            if direction[j] and check_black(xx, yy):
                local_img[cordinate_y[yy] - int(block_size / 2):cordinate_y[yy] + int(block_size / 2),
                cordinate_x[xx] - int(block_size / 2):cordinate_x[xx] + int(block_size / 2)] = block
                direction[j] = False
                destination.append([xx, yy])
            if direction[j] and r_check(xx, yy):
                local_img[cordinate_y[yy] - int(block_size / 2):cordinate_y[yy] + int(block_size / 2),
                cordinate_x[xx] - int(block_size / 2):cordinate_x[xx] + int(block_size / 2)] = block
                destination.append([xx, yy])
            else:
                direction[j] = False


def red_indicate_4(id, x, y, local_img):
    for i in range(8):
        xx = x + move_4[i][0]
        yy = y + move_4[i][1]
        if red_check_jiang(xx, yy, id) is False or check_block(x+unaccess_ma[i][0],y+unaccess_ma[i][1]) is False:
            continue
        if r_check(xx, yy):
            local_img[cordinate_y[yy] - int(block_size / 2):cordinate_y[yy] + int(block_size / 2),
            cordinate_x[xx] - int(block_size / 2):cordinate_x[xx] + int(block_size / 2)] = block
            destination.append([xx, yy])


def red_indicate_5(id, x, y, local_img):
    direction = [True] * 4
    direction_p = [True] * 4
    for i in range(1, 10):
        for j in range(4):
            xx = x + move_1[j][0] * i
            yy = y + move_1[j][1] * i
            if red_check_jiang(xx, yy, id) is False:
                continue
            if direction[j] is False and direction_p[j] and check_black(xx, yy):
                local_img[cordinate_y[yy] - int(block_size / 2):cordinate_y[yy] + int(block_size / 2),
                cordinate_x[xx] - int(block_size / 2):cordinate_x[xx] + int(block_size / 2)] = block
                direction_p[j] = False
                destination.append([xx, yy])
            if direction[j] and check_block(xx, yy):
                local_img[cordinate_y[yy] - int(block_size / 2):cordinate_y[yy] + int(block_size / 2),
                cordinate_x[xx] - int(block_size / 2):cordinate_x[xx] + int(block_size / 2)] = block
                destination.append([xx, yy])
            else:
                direction[j] = False


def red_indicate_6(id, x, y, local_img):
    for i in range(4):
        xx = x + move_6[i][0]
        yy = y + move_6[i][1]
        if red_check_jiang(xx, yy, id) is False:
            continue
        if r_check(xx, yy) and xx >= 3 and xx <= 5 and yy >= 7:
            local_img[cordinate_y[yy] - int(block_size / 2):cordinate_y[yy] + int(block_size / 2),
            cordinate_x[xx] - int(block_size / 2):cordinate_x[xx] + int(block_size / 2)] = block
            destination.append([xx, yy])


def red_indicate_7(id, x, y, local_img):
    for i in range(4):
        xx = x + move_6[i][0] * 2
        yy = y + move_6[i][1] * 2
        if red_check_jiang(xx, yy, id) is False:
            continue
        if r_check(xx, yy) and check_block(x + move_6[i][0], y + move_6[i][1]) and yy > 4:
            local_img[cordinate_y[yy] - int(block_size / 2):cordinate_y[yy] + int(block_size / 2),
            cordinate_x[xx] - int(block_size / 2):cordinate_x[xx] + int(block_size / 2)] = block
            destination.append([xx, yy])


# 1将2卒3车4马5炮6士7相

def red_indicate(id, img):
    t = tp[id]
    x = R_pieces_cordinate[id][0]
    y = R_pieces_cordinate[id][1]
    if t == 1:
        red_indicate_1(id, x, y, img)
    elif t == 2:
        red_indicate_2(id, x, y, img)
    elif t == 3:
        red_indicate_3(id, x, y, img)
    elif t == 4:
        red_indicate_4(id, x, y, img)
    elif t == 5:
        red_indicate_5(id, x, y, img)
    elif t == 6:
        red_indicate_6(id, x, y, img)
    elif t == 7:
        red_indicate_7(id, x, y, img)

def black_block(xx,yy,local_img):
    local_img[cordinate_y[9-yy] - int(block_size / 2):cordinate_y[9-yy] + int(block_size / 2),
    cordinate_x[8-xx] - int(block_size / 2):cordinate_x[8-xx] + int(block_size / 2)] = block

def black_indicate_1(id, x, y, local_img):
    for i in range(4):
        xx = x + move_1[i][0]
        yy = y + move_1[i][1]#raw
        flag = b_check(8-xx,9-yy)  #process check
        if R_pieces_cordinate[0][0] == xx:  #raw
            for j in range(1, 10):
                detect_jiang_y = yy + j
                if R_pieces_cordinate[0][1] == detect_jiang_y:
                    flag = False
                    break
                if check_block(xx, detect_jiang_y) == False:
                    break
        if flag:
            black_block(xx,yy,local_img)
            destination.append([xx, yy])


def black_indicate_2(id, x, y, local_img):
    if y < 5:
        xx = x
        yy = y + 1
        if b_check(8-xx, 9-yy):
            black_block(xx,yy,local_img)
            destination.append([xx, yy])
    else:
        for i in range(3):
            xx = x - move_2[i][0]
            yy = y - move_2[i][1]
            if b_check(8-xx, 9-yy) and black_check_jiang(xx, yy, id):
                black_block(xx,yy,local_img)
                destination.append([xx, yy])

#车
def black_indicate_3(id, x, y, local_img):
    direction = [True] * 4
    for i in range(1, 10):
        for j in range(4):
            xx = x + move_1[j][0] * i
            yy = y + move_1[j][1] * i
            if black_check_jiang(xx, yy, id) is False:
                continue
            if direction[j] and check_red(xx, yy):#raw check
                black_block(xx, yy, local_img)
                direction[j] = False
                destination.append([xx, yy])
            if direction[j] and b_check(8-xx, 9-yy):
                black_block(xx, yy, local_img)
                destination.append([xx, yy])
            else:
                direction[j] = False


def black_indicate_4(id, x, y, local_img):
    for i in range(8):
        xx = x + move_4[i][0]
        yy = y + move_4[i][1]
        if black_check_jiang(xx, yy, id) is False or check_block(x+unaccess_ma[i][0],y+unaccess_ma[i][1]) is False:
            continue
        if b_check(8-xx, 9-yy):
            black_block(xx, yy, local_img)
            destination.append([xx, yy])


def black_indicate_5(id, x, y, local_img):
    direction = [True] * 4
    direction_p = [True] * 4
    for i in range(1, 10):
        for j in range(4):
            xx = x + move_1[j][0] * i
            yy = y + move_1[j][1] * i
            if black_check_jiang(xx, yy, id) is False:
                continue
            if direction[j] is False and direction_p[j] and check_red(xx, yy):#raw
                black_block(xx, yy, local_img)
                direction_p[j] = False
                destination.append([xx, yy])
            if direction[j] and check_block(xx, yy):
                black_block(xx, yy, local_img)
                destination.append([xx, yy])
            else:
                direction[j] = False


def black_indicate_6(id, x, y, local_img):
    for i in range(4):
        xx = x + move_6[i][0]
        yy = y + move_6[i][1]
        if black_check_jiang(xx, yy, id) is False:
            continue
        if b_check(8-xx, 9-yy) and 3 <= xx <= 5 and yy <= 2:
            black_block(xx, yy, local_img)
            destination.append([xx, yy])


def black_indicate_7(id, x, y, local_img):
    for i in range(4):
        xx = x + move_6[i][0] * 2
        yy = y + move_6[i][1] * 2
        if black_check_jiang(xx, yy, id) is False:
            continue
        if b_check(8-xx, 9-yy) and check_block(x + move_6[i][0], y + move_6[i][1]) and yy < 5:
            black_block(xx, yy, local_img)
            destination.append([xx, yy])
            
            
            
def black_indicate(id, img):
    t = tp[id]
    x = B_pieces_cordinate[id][0]
    y = B_pieces_cordinate[id][1]
    if t == 1:
        black_indicate_1(id, x, y, img)
    elif t == 2:
        black_indicate_2(id, x, y, img)
    elif t == 3:
        black_indicate_3(id, x, y, img)
    elif t == 4:
        black_indicate_4(id, x, y, img)
    elif t == 5:
        black_indicate_5(id, x, y, img)
    elif t == 6:
        black_indicate_6(id, x, y, img)
    elif t == 7:
        black_indicate_7(id, x, y, img)


def red_select(i):
    img = cv2.imread('pad_800.jpg')
    for j in range(16):
        if active_R[j]:
            img[cordinate_y[R_pieces_cordinate[j][1]] - int(h / 2):cordinate_y[R_pieces_cordinate[j][1]] + int(
                h / 2),
            cordinate_x[R_pieces_cordinate[j][0]] - int(w / 2):cordinate_x[R_pieces_cordinate[j][0]] + int(
                w / 2)] = \
                R_pieces[j]
        if active_B[j]:
            img[cordinate_y[B_pieces_cordinate[j][1]] - int(h / 2):cordinate_y[B_pieces_cordinate[j][1]] + int(
                h / 2),
            cordinate_x[B_pieces_cordinate[j][0]] - int(w / 2):cordinate_x[B_pieces_cordinate[j][0]] + int(
                w / 2)] = \
                B_pieces[j]
    if i != -1:
        img[
        cordinate_y[R_pieces_cordinate[i][1]] - int(h / 2):cordinate_y[R_pieces_cordinate[i][1]] + int(h / 2),
        cordinate_x[R_pieces_cordinate[i][0]] - int(w / 2):cordinate_x[R_pieces_cordinate[i][0]] + int(w / 2)] = \
            R_pieces_s[i]
    return img


def black_select(i):
    img = cv2.imread('pad_800.jpg')
    for j in range(16):
        if active_R[j]:
            img[cordinate_y[black_pieces_cordinate_y_R(j)] - int(h / 2):cordinate_y[black_pieces_cordinate_y_R(j)] + int(
                h / 2),
            cordinate_x[black_pieces_cordinate_x_R(j)] - int(w / 2):cordinate_x[black_pieces_cordinate_x_R(j)] + int(
                w / 2)] = \
                R_pieces[j]
        if active_B[j]:
            img[cordinate_y[black_pieces_cordinate_y(j)] - int(h / 2):cordinate_y[black_pieces_cordinate_y(j)] + int(
                h / 2),
            cordinate_x[black_pieces_cordinate_x(j)] - int(w / 2):cordinate_x[black_pieces_cordinate_x(j)] + int(
                w / 2)] = \
                B_pieces[j]
    if i != -1:
        img[
        cordinate_y[black_pieces_cordinate_y(i)] - int(h / 2):cordinate_y[black_pieces_cordinate_y(i)] + int(h / 2),
        cordinate_x[black_pieces_cordinate_x(i)] - int(w / 2):cordinate_x[black_pieces_cordinate_x(i)] + int(w / 2)] = \
            B_pieces_s[i]
    return img

def red_hit_pieces(x, y, i):
    return active_R[i] and cordinate_x[R_pieces_cordinate[i][0]] - int(w / 2) < x < cordinate_x[
        R_pieces_cordinate[i][0]] + int(w / 2) and cordinate_y[R_pieces_cordinate[i][1]] - int(
        h / 2) < y < cordinate_y[R_pieces_cordinate[i][1]] + int(h / 2)


def red_hit_block(x, y, d):
    return cordinate_x[d[0]] - int(block_size / 2) < x < cordinate_x[d[0]] + int(block_size / 2) and cordinate_y[
        d[1]] - int(block_size / 2) < y < cordinate_y[d[1]] + int(block_size / 2)

def black_hit_block(x,y,d):
    return cordinate_x[8-d[0]] - int(block_size / 2) < x < cordinate_x[8-d[0]] + int(block_size / 2) and cordinate_y[
        9-d[1]] - int(block_size / 2) < y < cordinate_y[9-d[1]] + int(block_size / 2)


def black_pieces_cordinate_x(i):
    return 8 - B_pieces_cordinate[i][0]


def black_pieces_cordinate_x_R(i):
    return 8 - R_pieces_cordinate[i][0]


def black_pieces_cordinate_y(i):
    return 9 - B_pieces_cordinate[i][1]


def black_pieces_cordinate_y_R(i):
    return 9 - R_pieces_cordinate[i][1]


def black_hit_pieces(x, y, i):
    return active_B[i] and cordinate_x[black_pieces_cordinate_x(i)] - int(w / 2) < x < cordinate_x[
        black_pieces_cordinate_x(i)] + int(w / 2) and cordinate_y[black_pieces_cordinate_y(i)] - int(
        h / 2) < y < cordinate_y[black_pieces_cordinate_y(i)] + int(h / 2)

