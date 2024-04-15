def worst_fit_memory_management(nb, nf, b, f):
    max_size = 25
    frag = [0] * max_size
    bf = [0] * max_size
    ff = [0] * max_size
    for i in range(nf):
        highest = 0
        for j in range(nb):
            if bf[j] != 1:  # if bf[j] is not allocated
                temp = b[j] - f[i]
                if temp >= 0:
                    if highest < temp:
                        ff[i] = j
                        highest = temp
        frag[i] = highest
        bf[ff[i]] = 1
    print("\nFile_no:\tFile_size :\tBlock_no:\tBlock_size:\tFragment")
    for i in range(nf):
        print(f"{i}\t\t{f[i]}\t\t{ff[i]}\t\t{b[ff[i]]}\t\t{frag[i]}")


nb = 5
nf = 4
b = [100, 500, 200, 300, 600] 
f = [212, 417, 112, 426] 

worst_fit_memory_management(nb, nf, b, f)
