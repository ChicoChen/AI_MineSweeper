import sys
import pexpect
from collections import deque
import numpy as np
from random import randint
from pexpect import popen_spawn

symbol = ['#', ' ', 'F', '?']

def get_nearby(board, index):
    row_begin, row_end = max(index[0]-1, 0), min(index[0]+1, board.shape[0]-1)
    col_begin, col_end = max(index[1]-1, 0), min(index[1]+1, board.shape[1]-1)
    return board[row_begin: row_end + 1, col_begin: col_end + 1]


def globalize(centeral, local):
    offset = [int(centeral[0] != 0), int(centeral[1] != 0)] # offset for globalize local coordinate
    x = centeral[0] + local[0] - offset[0]
    y = centeral[1] + local[1] - offset[1]
    return (x, y)

def nextstep(board, input):
    if np.count_nonzero(board=='#') == board.shape[0] * board.shape[1]:
        x, y = randint(0, board.shape[0]-1), randint(0, board.shape[1]-1)
        input.append(str(x) + " " + str(y))
    else:
        global symbol
        pos = np.where(~np.isin(board, symbol)) # pos = [block with known numbers]
        pos = np.transpose(pos)

        unclear = []
        for ele in pos:
            local = get_nearby(board, ele)
            mines_remain = int(board[tuple(ele)]) - np.count_nonzero(local == 'F')
            if(mines_remain < 0): print("too many mines: " + str(ele[0]) + " " + str(ele[1]))
            unknown = np.transpose(np.nonzero(local == '#'))
            if(len(unknown) == 0): continue

            if(mines_remain == 0): # area is clear
                for safe in unknown: 
                    x, y = globalize(ele, safe)
                    input.append(str(x) + " " + str(y))
            elif (np.count_nonzero(local == '#') == mines_remain): # found mines
                for mine in unknown: 
                    x, y = globalize(ele, mine)
                    input.append(str(x) + " " + str(y) + " F")
            else: # need inference
                if(np.count_nonzero(~np.isin(local, symbol)) > 1):
                    unclear.append(tuple(ele))  

        # deductive reasoning
        if(len(input) == 0): inference(board, unclear)
        if(len(input) == 0): 
            print("inferencing failed")
            remain_blocks = np.transpose(np.nonzero(board == '#'))
            que = []
            for i in remain_blocks:
                if np.all(get_nearby(board, i) == '#'): que.append(i)
            if(len(que)):
                rand = randint(0, len(que)-1)
                input.append(str(que[rand][0]) + " " + str(que[rand][1]))
                print("random step - case1: " + str(que[rand][0]) + " " + str(que[rand][1]))
            else: 
                rand = randint(0, len(remain_blocks)-1)
                input.append(str(remain_blocks[rand][0]) + " " + str(remain_blocks[rand][1]))
                print("random step - case2: " + str(remain_blocks[rand][0]) + " " + str(remain_blocks[rand][1]))
    return 

def inference(board, unclear): # neighbor has unknown mine(s), and # of number > 1(self included)
    print("begin inferencing")
    for ele in unclear:
        local = get_nearby(board, ele)
        neighbors = np.transpose(np.nonzero(~np.isin(local, symbol))) # index of numbers around centeral
        for neighbor in neighbors:
            index = globalize(ele, neighbor)
            if index == ele: continue
            shared = [] # mutual unknown blocks
            for i in range(local.shape[0]):
                for j in range(local.shape[1]):
                    if local[i][j] == '#' and max(abs(i - neighbor[0]), abs(j - neighbor[1])) <= 1:
                        shared.append(globalize(ele, (i, j)))
            if len(shared) != 2: continue # only deal with 2 blocks case
            else:
                local_N = get_nearby(board, index)
                mines_remain = int(board[ele]) - np.count_nonzero(local == 'F')
                mines_remain_N = int(board[index]) - np.count_nonzero(local_N == 'F')
                if mines_remain != 1 and mines_remain_N != 1: continue # one's num of remained mines = 1
                block_remain = np.count_nonzero(local == '#')
                block_remain_N = np.count_nonzero(local_N == '#')
                prob = mines_remain / block_remain # P(A)= prob of block A has mine
                prob_AandB = prob * (mines_remain - 1)/(block_remain - 1) # P(A) * P(B|A)
                prob = 2 * prob - prob_AandB # P(A) + P(B) - P(AandB) = P(AorB)

                if prob >= 1: # so now we're sure there's a mine in mutual blocks
                    for x, y in np.transpose(np.nonzero(local == '#')):
                        pos = globalize(ele, (x, y))
                        if pos in shared: continue
                        if mines_remain == 1: input.append(str(pos[0]) + " " + str(pos[1]))
                        elif mines_remain - 1 == block_remain - 2: input.append(str(pos[0]) + " " + str(pos[1]) + " F")
                    
                    for x, y in np.transpose(np.nonzero(local_N == '#')):
                        pos = globalize(index, (x, y))
                        if pos in shared: continue
                        if mines_remain_N == 1: input.append(str(pos[0]) + " " + str(pos[1]))
                        elif mines_remain_N - 1 == block_remain_N - 2: input.append(str(pos[0]) + " " + str(pos[1]) + " F")

            if(len(input) != 0): 
                print("inference result:")
                print(input)
                break
        if(len(input) != 0): break
    return 

if __name__ == "__main__":
    exe_path = "D:/colding/MineSweeper/Debug/MineSweeper.exe"
    # I just notice my folder name is "colding" rather than "coding", lul
    # wait...so I use the wrong name for four years?
    win_count = 0
    win = []
    epoch = 50
    for i in range(epoch):
        process = popen_spawn.PopenSpawn([exe_path], logfile=sys.stdout.buffer)
        process.logfile = open("logs/map" + str(i+1) + ".txt", "wb")
        file = open("logs/map" + str(i+1) + ".txt", "r")
        process.expect("-------")

        lines = []
        end_flag = False
        input = deque()

        while(True):
            # read & extract the board
            lines.clear()
            flag = process.expect(["act:", "Gameover :\(", "we win :\)"]) 
            if flag != 0:
                if flag == 2:
                    win_count += 1
                    win.append(i)
                break # exit the loop if game end
            for line in file:
                lines.append(line.strip())

            board = np.array(lines[-19:-3]) # will read undesire line if len < 19
            temp = list(map(lambda x: x.split('|'), board))
            board = np.array(temp)[:, 1:-1] 
            
            if(len(input) == 0): nextstep(board, input)
            # sending input
            process.sendline(input[0])
            input.popleft()
            process.expect("step:")

        process.expect(pexpect.EOF, timeout = 2)
    print("winerate: " + str(win_count) + "/" + str(epoch))
    print(win)
