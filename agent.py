import sys
import numpy as np
from random import randint
import pexpect
from pexpect import popen_spawn

if __name__ == "__main__":
    exe_path = "D:/colding/MineSweeper/Debug/MineSweeper.exe"

    process = popen_spawn.PopenSpawn([exe_path], logfile=sys.stdout.buffer)
    process.logfile = open("map.txt", "wb")
    file = open("map.txt", "r")
    process.expect("-------")

    lines = []
    end_flag = False
    while(True):
        # reading the board
        lines.clear()
        for line in file:
            if line == "Gameover :(\n":
                end_flag = True
                break
            lines.append(line.strip())
        if(end_flag): break

        # extract the board
        board = np.array(lines[-18:-2])
        temp = list(map(lambda x: x.split('|'), board))
        board = np.array(temp)[:, 1:-1]

        # sending input
        x, y =  randint(0, 15), randint(0, 15)
        process.sendline(str(x) + " " + str(y))
        process.expect("step: ")        
        
    process.expect(pexpect.EOF, timeout = 2)

