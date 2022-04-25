import sys

# ******************************************************
# Print out quick view of what configuration looks like.
# ******************************************************

def print_config(d, m, b):
    # The default buttons and double row buttons
    f = [
        2048, 3072, 1024, 1536, 512,
        2304, 3456, 1152, 1728, 576,
        256, 384, 128, 192, 64,
        288, 432, 144, 216, 72,
        32, 48, 16, 24, 8,
        36, 54, 18, 27, 9,
        4, 6, 2, 3, 1,
    ]

    # Mask f here when adding combo display feature.

    # If a chord doesn't have an n_gram fill it with the empty string.
    for x in f:
        if x not in d:
            d[x] = ""
    # print(f[0].sort())
    
    actual_cost = int(str(m[b.total_cost]))
    print(f'Total Cost: {actual_cost}', file=sys.stderr)
    print(f'\n   Left       Middle       Right', file=sys.stderr)
    print(f' ________________________________', file=sys.stderr)
    print(f'|                                | <-- Mouseclick buttons', file=sys.stderr)
    print(f'|--------------------------------|', file=sys.stderr)
    print(f'| [{d[f[0]]:4}] {d[f[1]]:4} [{d[f[2]]:4}] {d[f[3]]:4} [{d[f[4]]:4}] |', file=sys.stderr)
    print(f'|                                |', file=sys.stderr)
    print(f'|  {d[f[5]]:4}  {d[f[6]]:4}  {d[f[7]]:4}  {d[f[8]]:4}  {d[f[9]]:4}  |', file=sys.stderr)
    print(f'|                                |', file=sys.stderr)
    print(f'| [{d[f[10]]:4}] {d[f[11]]:4} [{d[f[12]]:4}] {d[f[13]]:4} [{d[f[14]]:4}] |', file=sys.stderr)
    print(f'|                                |', file=sys.stderr)
    print(f'|  {d[f[15]]:4}  {d[f[16]]:4}  {d[f[17]]:4}  {d[f[18]]:4}  {d[f[19]]:4}  |', file=sys.stderr)
    print(f'|                                |', file=sys.stderr)
    print(f'| [{d[f[20]]:4}] {d[f[21]]:4} [{d[f[22]]:4}] {d[f[23]]:4} [{d[f[24]]:4}] |', file=sys.stderr)
    print(f'|                                |', file=sys.stderr)
    print(f'|  {d[f[25]]:4}  {d[f[26]]:4}  {d[f[27]]:4}  {d[f[28]]:4}  {d[f[29]]:4}  |', file=sys.stderr)
    print(f'|                                |', file=sys.stderr)
    print(f'| [{d[f[30]]:4}] {d[f[31]]:4} [{d[f[32]]:4}] {d[f[33]]:4} [{d[f[34]]:4}] |', file=sys.stderr)
    print(f'|________________________________|', file=sys.stderr, flush = True)

def print_details(s, m, b, n, this_run_time, all_run_time):
    # We generate a dictionary where the chords are the keys and n_grams the values.
    num_2 = 0
    num_3 = 0
    num_4 = 0
    num_5 = 0
    press_lookup = {}
    if m == None:
        print(s.unsat_core())
        return
    # print(m) # Uncomment to debug.
    for i in range(len(n.G)):
        if m[b.G[i]] in press_lookup:
            assert m[b.G[i]] == 0
        else:
            press_lookup[int(str(m[b.G[i]]))] = n.G[i]
            if len(n.G[i]) == 2:
                # print("i: " + str(i) + ", m[G[i]]: " + str(m[G[i]]) + ", n.G: " + n.G[i])
                num_2 += 1
            elif len(n.G[i]) == 3:
                num_3 += 1
            elif len(n.G[i]) == 4:
                num_4 += 1
            elif len(n.G[i]) == 5:
                num_5 += 1
            # elif len(n.G[i]) == 1:
            print("i: " + str(i) + ", m[G[i]]: " + str(m[b.G[i]]) + ", n_gram: " + n.G[i], file=sys.stderr)
    print(f'Chorded-2_grams: {num_2}, 3_grams: {num_3}, 4_grams: {num_4}, 5_grams: {num_5}', file=sys.stderr)
    print(f'Time for this run: {this_run_time}, Time for all runs: {all_run_time}', file=sys.stderr)
    
    print_config(press_lookup, m, b)