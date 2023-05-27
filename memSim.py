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
    fifo_i = 0
    total = 0
    frame = 0
    block = 0
    byte = 0
    faults = 0
    hits = 0
    # go through each line of the file
    lines = file.readlines()
    for line in lines:
        # take out only first four bits to find page number
        # print()
        virtual = bin(int(line))
        virtual = virtual[2:]
        while (len(virtual) < 16):
            virtual = "0" + virtual
        page_num = int(virtual[0:8], 2)
        offset = int(virtual[8:16], 2)
        # check TLB for frame num
        in_tlb = False
        framenum = -1

        # print(tlb)
        for pair in tlb:
            if pair[0] == page_num:
                in_tlb = True
                framenum = pair[1]
                hits += 1
                # print("tlb hit")
        if in_tlb:
            #printing info
            block = memory[framenum]
            frame = framenum
            byte = block[offset]

            #update process usage parameter / valid bit
            if algorithm == "LRU":
                old_entry = ptable[page_num]
                ptable[page_num] = (old_entry[0], LRU_i)
                LRU_i += 1

        #     print(framenum)

        # if not in TLB check in page table
        else:
            entry = ptable[page_num]
            if entry[1] != -1:
                frame = entry[0]
                add_to_tlb(tlb, page_num, frame)

                #update process usage parameter / valid bit
                if algorithm == "LRU":
                    old_entry = ptable[page_num]
                    ptable[page_num] = (old_entry[0], LRU_i)
                    LRU_i += 1

                #printing info
                block = memory[frame]
                byte = block[offset]
                # print("ptable hit")

            else:
                # if not in page table, check BACKING_STORE.bin
                backend = open('BACKING_STORE.bin', 'rb')
                i = 0
                faults += 1

                #while num pages < page table size
                while (i != 256):
                    try:
                        #read frame
                        l = backend.read(256)
                        #if frame is page
                        if i == page_num:
                            #list of bytes
                            # print()
                            # print("i:", i)
                            # print(l)
                            block = list(l)
                            # print(block)
                            # print("offset:", offset)
                            byte = block[offset]
                            if byte > 127:
                                byte = 256 - byte
                                byte = byte * -1
                            
                            
                            if algorithm == "FIFO":
                                # print("FIFO")
                                #check for flip around
                                if fifo_i >= frames:
                                    fifo_i = 0
                                #invalidate previous frame's ptable
                                for i in range(len(ptable)):
                                    if ptable[i][0] == fifo_i:
                                        ptable[i] = (fifo_i, -1)
                                #overwrite frame
                                add_to_memory(memory, l, frames, fifo_i)
                                #add to page table
                                ptable[page_num] = (fifo_i, 1)
                                frame = fifo_i
                                
                                #remove from tlb table
                                for k in range(len(tlb)):
                                    # print(tlb)
                                    if tlb[k][1] == frame:
                                        tlb.pop(k)
                                        break
                                
                                fifo_i += 1

                            if algorithm == "LRU":
                                #check if memory filled
                                if LRU_i >= frames:
                                    #find least recently used frame
                                    min = -1
                                    for entry in ptable:
                                        if entry[1] != -1:
                                            if min == -1 or entry[1] < min:
                                                #this entry is oldest thus far
                                                min = entry[1]
                                                min_entry = entry
                                    #overwrite LRU frame and invalidate prev entry
                                    # print("min entry:", min_entry)
                                    for i in range(len(ptable)):
                                        if ptable[i] == min_entry:
                                            ptable[i] = (ptable[i][0], -1)
                                    add_to_memory(memory, l, frames, min_entry[0])
                                    #add to page table
                                    ptable[page_num] = (min_entry[0], LRU_i)
                                    frame = min_entry[0]
                                else:
                                    #memory not yet filled
                                    #add to memory
                                    add_to_memory(memory, l, frames, LRU_i)
                                    #add to page table
                                    ptable[page_num] = (LRU_i, LRU_i)
                                    frame = LRU_i
                                #increment lru i
                                LRU_i += 1
                                # for entry in ptable:
                                #     if entry != [-1, -1, -1]:
                                #         print("ptable entry:", entry)

                                
                                #remove from tlb table
                                for k in range(len(tlb)):
                                    # print(tlb)
                                    if tlb[k][1] == frame:
                                        tlb.pop(k)
                                        break

                                #add to tlb
                            add_to_tlb(tlb, page_num, frame)
                        i += 1
                    except StopIteration:
                        break
                backend.close()

            # for entry in memory:
            #     if entry != -1:
            #         print("entry:", entry[0:4])
            # print(tlb)

        # print third part of printout
        print(f'{int(line)}, {byte}, {frame},')
        for index in block:
            print(f'{index:X}', end='')

        # print("total:", total)
        # frame += 1
        total += 1

    print()
    print(f'Number of Translated Addresses = {total}')
    print(f'Page Faults = {faults}')
    print(f'Page Fault Rate = {faults/total:.3f}')
    print(f'TLB Hits = {hits}')
    print(f'TLB Misses = {total - hits}')
    print(f'TLB Hit Rate = {(hits/total):.3f}')




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

        # if we have not filled all of the frames in physical memory
        if total < frames:

            # check if we already have it in physical memory
            pass

        # if we have filled all of the frames
        else:

            # check for which ones will be used

            #  find oldest out of the frames that will not be used in future

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
    # print("memory:", len(memory))
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

    
    hardcoded(file, tlb, ptable, memory, frames, algorithm)


    return 0


if __name__ == '__main__':
    main()



# #update page table with new page
#                                 ptable[page_num] = (frame_num, LRU_i)
#                                 #update prints
#                                 frame = frame_num
                                
#                                 #if more pages than frames
#                                 print("lru i:", LRU_i)
#                                 if LRU_i >= frames:
#                                     #determine oldest frame (earliest use and/or placement)
#                                     min = -1
#                                     min_i = -1
#                                     for i in range(len(ptable)):
#                                         if ptable[i] != [-1, -1, -1]:
#                                             print("current page", ptable[i])
#                                             if min == -1:
#                                                 min = ptable[i][1]
#                                                 min_i = ptable[i][0]
#                                             elif ptable[i][1] < min:
#                                                 min = ptable[i][1]
#                                                 min_i = ptable[i][0]
#                                     #next frame to be updated will be least recently used
#                                     frame_num = min_i
#                                     print("frame num / min_i:", frame_num)