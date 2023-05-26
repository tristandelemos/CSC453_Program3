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

def hardcoded(file, tlb, ptable, memory, frames):

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
            print(framenum)

        # if not in TLB check in page table
        else:
            entry = ptable[page_num]
            if entry[2] != -1:
                frame = entry[1]
                # put into TLB
                if len(tlb) < 16:
                    # append to end of fifo queue
                    tlb.append((page_num, frame))
                else:
                    # remove oldest, then append
                    tlb.pop(0)
                    tlb.append((page_num, frame))

            else:
                # if not in page table, check BACKING_STORE.bin
                backend = open('BACKING_STORE.bin', 'rb')
                i = 0
                faults += 1

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
                            ptable[page_num] = (frame_num, 1)
                            frame_num += 1
                        i += 1
                    except StopIteration:
                        break
                backend.close()

        # print third part of printout
        print(f'{int(line)}, {byte}, {frame},')
        for index in block:
            print(f'{index:X}', end='')

        frame += 1
        total += 1
    print()
    print(f'Number of Translated Addresses = {total}')
    print(f'Page Faults = {faults}')
    print(f'Page Fault Rate = {faults/total:.3f}')
    print(f'TLB Hits = {hits}')
    print(f'TLB Misses = {total - hits}')
    print(f'TLB Hit Rate = {1 - (faults/total):.3f}')


def opt(file, tlb, ptable, memory, frames):
    total = 0
    frame_num = 0
    frame = 0
    block = 0
    byte = 0
    faults = 0
    hits = 0

    # now all lines of the file are in the lines list
    lines = file.readlines()

    for line in lines:

        if total < frames:
            # if we have not filled all of the frames in physical memory
            pass

    print()
    print(f'Number of Translated Addresses = {total}')
    print(f'Page Faults = {faults}')
    print(f'Page Fault Rate = {faults / total:.3f}')
    print(f'TLB Hits = {hits}')
    print(f'TLB Misses = {total - hits}')
    print(f'TLB Hit Rate = {1 - (faults / total):.3f}')





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

    if numOfArgs > 4 or numOfArgs == 1:
        print("Usage: memSim <reference.txt> <FRAME_SIZE> <ALGORITHM>")
        return 0

    # if given only a txt file, use default
    if numOfArgs == 2:
        hardcoded(file, tlb, ptable, frames)

    if numOfArgs > 2:
        frames = int(sys.argv[2])

    if numOfArgs > 3:
        algorithm = sys.argv[3]

    return 0


if __name__ == '__main__':
    main()
