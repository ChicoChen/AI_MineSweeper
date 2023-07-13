import sys
import pexpect
from collections import deque
import numpy as np
from random import randint
from pexpect import popen_spawn

def nextstep(board, input):
    if np.count_nonzero(board=='#') == board.shape[0] * board.shape[1]:
        x, y = randint(0, 15), randint(0, 15)
        input.append(str(x) + " " + str(y))
    else:
        symbol = ['#', ' ', 'F', '?']
        pos = np.where(~np.isin(board, symbol)) # pos = [block with known numbers]
        pos = np.transpose(pos)

        for ele in pos:
            row_begin, row_end = max(ele[0]-1, 0), min(ele[0]+1, board.shape[0]-1)
            col_begin, col_end = max(ele[1]-1, 0), min(ele[1]+1, board.shape[1]-1)
            neighbor = board[row_begin: row_end + 1, col_begin: col_end + 1]

            mines_remain = int(board[tuple(ele)]) - np.count_nonzero(neighbor == 'F')
            if(mines_remain < 0): print("too many mines: " + str(ele[0]) + " " + str(ele[1]))
            unknown = np.transpose(np.nonzero(neighbor == '#'))
            if(len(unknown) == 0): continue

            x, y = tuple(ele)
            offset = [int(x != 0), int(y != 0)] # offset for globalize neighbor coordinate
            if(mines_remain == 0): # area is clear
                for safe in unknown: input.append(str(x + safe[0] - offset[0]) + " " + str(y + safe[1] - offset[1]))
            elif (np.count_nonzero(neighbor == '#') == mines_remain): # found mines
                for mine in unknown: input.append(str(x + mine[0] - offset[0]) + " " + str(y + mine[1] - offset[1]) + " F")

    if(len(input) == 0): 
        x, y = randint(0, 15), randint(0, 15)
        print("random_step: " + str(x) + " " + str(y))
        input.append(str(x) + " " + str(y))
    return 

if __name__ == "__main__":
    exe_path = "D:/colding/MineSweeper/Debug/MineSweeper.exe" 
    # I just notice my folder name is "colding" rather than "coding", lul
    # wait, so I use the wrong name for four years?

    process = popen_spawn.PopenSpawn([exe_path], logfile=sys.stdout.buffer)
    process.logfile = open("map.txt", "wb")
    file = open("map.txt", "r")
    process.expect("-------")

    lines = []
    end_flag = False
    input = deque()

    while(True):
        # read & extract the board
        lines.clear()
        flag = process.expect(["act:", "Gameover :\(", "we win :\)"]) 
        if flag != 0: break # exit the loop if game end
        for line in file:
            lines.append(line.strip())

        board = np.array(lines[-19:-3]) # will read undesire line if len < 19
        temp = list(map(lambda x: x.split('|'), board))
        board = np.array(temp)[:, 1:-1] 
        
        if(len(input) == 0): nextstep(board, input)
        # sending input
        process.sendline(input[0])
        print("len: " + str(len(input)))
        input.popleft()
        process.expect("step:")

    process.expect(pexpect.EOF, timeout = 2)

