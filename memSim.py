#!usr/bin/env python3
"""
Created by Tristan de Lemos and Trenten Spicer
Simulates virtual memory by translating virtual memory addresses to physical memory addresses
"""

import sys


def add_to_tlb(tlb, page_num, frame):
    if (len(tlb) < 16):
        #append to end of fifo queue
        tlb.append((page_num, frame))
    else:
        #remove oldest, then append
        tlb.pop(0)
        tlb.append((page_num, frame))

    return



def hardcoded(file, tlb, ptable):
    lines = file.readlines()
    frame = 0
    # go through each line of the file
    for line in lines:
        # take out only first four bits to find page number
        virtual = bin(int(line))
        virtual = virtual[2:]
        page_num = virtual[0:7]
        # check TLB for frame num
        in_tlb = False
        framenum = -1
        for pair in tlb:
            if (pair[0] == page_num):
                in_tlb = True
                framenum = pair[1]
        if in_tlb:
            print(framenum)

        else:
            # if not in TLB check in page table
            entry = ptable[int(page_num)]
            if entry[2] != -1:
                frame = entry[1]
                # put into TLB
                add_to_tlb(tlb, page_num, frame)

            else:
                # if not in page table, check BACKING_STORE.bin
                pass


def main():

    tlb = []

    ptable = [-1, -1, -1]
    ptable = [ptable] * 256

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