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

def add_to_memory(memory, frame, max_frames, frame_num):
    if frame_num == max_frames:
        frame_num = 0

    # print("frame num:", frame_num)
    memory[frame_num] = frame

    return

def hardcoded(file, tlb, ptable, memory, frames, algorithm):

    LRU_i = 0
    total = 0
    frame_num = 0
    frame = 0
    block = 0
    byte = 0
    faults = 0
    hits = 0
    # go through each line of the file
    lines = file.readlines()
    for line in lines:
        # take out only first four bits to find page number
        print()
        virtual = bin(int(line))
        virtual = virtual[2:]
        while (len(virtual) < 16):
            virtual = "0" + virtual
        page_num = int(virtual[0:8], 2)
        offset = int(virtual[8:16], 2)
        # check TLB for frame num
        in_tlb = False
        framenum = -1

        for pair in tlb:
            if pair[0] == page_num:
                in_tlb = True
                framenum = pair[1]
                hits += 1
        if in_tlb:
            #printing info
            block = memory[framenum]
            frame = framenum
            byte = block[offset]

        #     print(framenum)

        # if not in TLB check in page table
        else:
            entry = ptable[page_num]
            if entry[2] != -1:
                frame = entry[1]
                add_to_tlb(tlb, page_num, frame)

                #update process usage parameter / valid bit
                if algorithm == "LRU":
                    old_entry = ptable[page_num]
                    ptable[page_num] = (old_entry[0], LRU_i)
                    LRU_i += 1

                #printing info
                block = memory[frame]
                byte = block[offset]

            else:
                # if not in page table, check BACKING_STORE.bin
                backend = open('BACKING_STORE.bin', 'rb')
                i = 0
                faults += 1

                #while num pages < page table size
                while (i != 256):
                    try:
                        l = backend.read(256)
                        if i == page_num:
                            block = list(l)
                            byte = block[offset]
                            if byte > 127:
                                byte = 256 - byte
                                byte = byte * -1
                            #add to page table / main memory
                            add_to_memory(memory, l, frames, frame_num)
                            if algorithm == "FIFO" or algorithm == "LRU":
                                #update page table with new page
                                ptable[page_num] = (frame_num, LRU_i)
                                #update prints
                                frame = frame_num
                                #increase num pages added
                                LRU_i += 1
                                #if more pages than frames
                                if LRU_i >= frames:
                                    #determine oldest frame (earliest use and/or placement)
                                    min = -1
                                    min_i = -1
                                    for i in range(len(ptable)):
                                        if min == -1:
                                            min = ptable[i][1]
                                            min_i = i
                                        if ptable[i][1] < min:
                                            min = ptable[i][1]
                                            min_i = i
                                    #next frame to be updated will be least recently used
                                    frame_num = min_i
                            #add to tlb
                            add_to_tlb(tlb, page_num, frame_num)

                            #increment
                            if LRU_i < frames:
                                frame_num += 1
                        i += 1
                    except StopIteration:
                        break
                backend.close()

        # print third part of printout
        print(f'{int(line)}, {byte}, {frame},')
        for index in block:
            print(f'{index:X}', end='')

        print("total:", total)
        # frame += 1
        total += 1

    print()
    print(f'Number of Translated Addresses = {total}')
    print(f'Page Faults = {faults}')
    print(f'Page Fault Rate = {faults/total:.3f}')
    print(f'TLB Hits = {hits}')
    print(f'TLB Misses = {total - hits}')
    print(f'TLB Hit Rate = {1 - (faults/total):.3f}')


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


    memory = [-1] * frames
    # print("memory:", len(memory))

    hardcoded(file, tlb, ptable, memory, frames, algorithm)

    # print(memory)


    if numOfArgs > 4 or numOfArgs == 1:
        print("Usage: memSim <reference.txt> <FRAME_SIZE> <ALGORITHM>")
        return 0

    # if given only a txt file, use default
    # if numOfArgs == 2:
    #     hardcoded(file, tlb, ptable, memory, frames, algorithm)

    if numOfArgs > 2:
        frames = int(sys.argv[2])

    if numOfArgs > 3:
        algorithm = sys.argv[3]

    return 0


if __name__ == '__main__':
    main()
