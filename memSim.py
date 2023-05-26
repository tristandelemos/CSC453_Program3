#!usr/bin/env python3
"""
Created by Tristan de Lemos and Trenten Spicer
Simulates virtual memory by translating virtual memory addresses to physical memory addresses
"""

import sys


def hardcoded(file):
    lines = file.readlines()

    # go through each line of the file
    for line in lines:
        # take out only first four bits to find page number
        virtual = bin(int(line))
        virtual = virtual[2:]
        page_num = virtual[0:7]
        # check TLB for frame num
        for index in TLB:
            if int(page_num)  ==
        # if not in TLB check in page table
        for index in ptable:
            if int(page_num) ==
        # if not in page table, check BACKING_STORE.bin


def main():
    page_table = [-1, -1, -1]
    page_table = [page_table] * 256

    algorithm = "FIFO"
    frames = 256
    # check for algorithm


    
    numOfArgs = len(sys.argv)
    if numOfArgs > 1:
        file = open(str(sys.argv[1]), "r")
    else:
        file = open("fifo1.txt", "r")

    hardcoded(file)

    """"
    
    if numOfArgs > 4 or numOfArgs == 1:
        print("Usage: memSim <reference.txt> <FRAME_SIZE> <ALGORITHM>")
        return 0

    if numOfArgs > 2:
        frames = int(sys.argv[2])

    if numOfArgs > 3:
        algorithm = sys.argv[3]

    """
    return 0


if __name__ == '__main__':
    main()