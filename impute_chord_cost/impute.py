# Index Left and Middle Left had identical timings of 0.530973451.
# This is undesirable for several reasons:
# 1) It seems unlikely in a real-world large user study that any
#       two chords would have identical timings.
# 2) It seems likely that identical timings will make the job of
#       the solver harder, because it increases the probability
#       that multiple configurations have the same cost. The
#       solver must then spend time checking if the cost of
#       each of these configurations, instead of learning a
#       a constraint that would prune some of the configurations
#       from the search space.
# 3)    Because we are not running a user study our goal is to
#       test the computational model, not generate an optimal
#       configuration. Non-idential timings should produce a more
#       realistic test.
# Therefore:
#   Each timing 0.530973451 was modified as follows:
#   NEW_TIMING = 0.530973451 + Random_Number[-0.01, 0.01)
#   New Index Left = 0.526762113
#   New Middle Left = 0.537003738
def c(finger, button):
    if finger == "i":
        if button == 1:
            return 0.526762113
        if button == 2:
            return 0.452830189
        if button == 3:
            return 0.560747664
    if finger == "m":
        if button == 1:
            return 0.537003738
        if button == 2:
            return 0.470588235
        if button == 3:
            return 0.52173913
    if finger == "r":
        if button == 1:
            return 0.674157303
        if button == 2:
            return 0.465116279
        if button == 3:
            return 0.594059406
    if finger == "p":
        if button == 1:
            return 0.689655172
        if button == 2:
            return 0.538116592
        if button == 3:
            return 0.625

    return 0.0

def chord_to_int(index, middle, ring, pinky):
    chord_int = 0
    if index == 3:
        chord_int += 2048
    elif index == 2:
        chord_int += 1024
    elif index == 1:
        chord_int += 512
        
    if middle == 3:
        chord_int += 256
    elif middle == 2:
        chord_int += 128
    elif middle == 1:
        chord_int += 64
        
    if ring == 3:
        chord_int += 32
    elif ring == 2:
        chord_int += 16
    elif ring == 1:
        chord_int += 8
        
    if pinky == 3:
        chord_int += 4
    elif pinky == 2:
        chord_int += 2
    elif pinky == 1:
        chord_int += 1
    return chord_int

# 1) Enumerate chords
# 0 = No button
# 1 = Left button
# 2 = Middle button
# 3 = Right button
for index in range(4):
    for middle in range(4):
        for ring in range(4):
            for pinky in range(4):
                
                # 2) For every chord impute a cost
                fingers = 0
                if index != 0:
                    fingers += 1
                if middle != 0:
                    fingers += 1
                if ring != 0:
                    fingers += 1
                if pinky != 0:
                    fingers += 1
                
                if fingers == 0:
                    continue

                max_cost = max(c("i", index), c("m", middle), c("r", ring), c("p", pinky))
                mean_cost = (c("i", index) + c("m", middle) + c("r", ring) + c("p", pinky)) / fingers
                cost = 0
                if fingers == 1:
                    cost = max_cost
                else:
                    cost = max_cost + 0.25 * fingers * mean_cost

                # 3) Print every chord
                chord_int = chord_to_int(index, middle, ring, pinky)
                print(f"s.add( If(n.G[h2_index] == {chord_int}, raw_H2_cost[i] == {cost}))")