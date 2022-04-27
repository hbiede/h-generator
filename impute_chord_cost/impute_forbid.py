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

def custom_chord_cost(finger_limit, reserved_finger, max_chords_per_finger_limit):
    # Chords Grouped by Finger Combo (cgfc)
    cgfc = {'else': dict()}
    # 1) Enumerate chords
    # 0 = No button
    # 1 = Left button
    # 2 = Middle button
    # 3 = Right button
    for index in range(4):
        for middle in range(4):
            for ring in range(4):
                for pinky in range(4):
                    
                    finger_cnt = 0
                    finger_id = 0
                    if index != 0:
                        finger_cnt += 1
                        finger_id += 8
                    if middle != 0:
                        finger_cnt += 1
                        finger_id += 4
                    if ring != 0:
                        finger_cnt += 1
                        finger_id += 2
                    if pinky != 0:
                        finger_cnt += 1
                        finger_id += 1
                    
                    if finger_cnt == 0 or finger_cnt > finger_limit:
                        continue
                    if (reserved_finger == "index"  and (index  == 1 or index  == 3)) or \
                       (reserved_finger == "middle" and (middle == 1 or middle == 3)) or \
                       (reserved_finger == "ring"   and (ring   == 1 or ring   == 3)) or \
                       (reserved_finger == "pinky"  and (pinky  == 1 or pinky  == 3)):
                       continue

                    max_cost = max(c("i", index), c("m", middle), c("r", ring), c("p", pinky))
                    mean_cost = (c("i", index) + c("m", middle) + c("r", ring) + c("p", pinky)) / finger_cnt
                    cost = 0
                    if finger_cnt == 1:
                        cost = max_cost
                    else:
                        cost = max_cost + 0.25 * finger_cnt * mean_cost
                    cost = round(cost * 10000)
                    
                    chord_int = chord_to_int(index, middle, ring, pinky)

                    if finger_cnt == finger_limit:
                        if finger_id in cgfc:
                            cgfc[finger_id].append((chord_int, cost))
                        else:
                            cgfc[finger_id] = [(chord_int, cost)]
                    else:
                        cgfc["else"][chord_int] = cost  # All chords not limited by max_chords_per_finger_limit

    s = "Chord Costs\n"
    cost_lines = 0
    forbidden_chords = "# Forbidden chord combinations\n"
    forbidden_chords = forbidden_chords + "s.add( And( "
    forbidden_cnt = 0
    for finger_id, chord_and_cost in cgfc.items():
        if finger_id == "else":
            for chord_int, cost in chord_and_cost.items():
                s = s + f"s.add( Or( Not( G[i] == {chord_int}), raw_G_cost[i] == {cost}))\n"
                cost_lines += 1
        else:
            chord_and_cost.sort(key=lambda y: y[1]) # Sort by 2nd element (cost) in tuple
            take_this_many_chords = min(len(chord_and_cost), max_chords_per_finger_limit)
            for i in range(take_this_many_chords):
                s = s + f"s.add( Or( Not( G[i] == {chord_and_cost[i][0]}), raw_G_cost[i] == {chord_and_cost[i][1]}))\n"
                cost_lines += 1
            for i in range(take_this_many_chords, len(chord_and_cost)):
                forbidden_chords = forbidden_chords + f"Not(G[i] == {chord_and_cost[i][0]}), "
                forbidden_cnt += 1

    s = s + f"Lines: {cost_lines}"
    forbidden_chords = forbidden_chords[:-2] + "))\n"
    forbidden_chords = forbidden_chords + f"Chords forbidden: {forbidden_cnt}"
    return (s, forbidden_chords)

def forbidden(finger_limit):
    s = "# Forbidden finger combinations\n"
    s = s + "s.add( And( "
    if finger_limit < 4:
        s = s + "Not(G_D[i] == 4095), "
    if finger_limit < 3:
        s = s + "Not(G_D[i] == 4088), Not(G_D[i] == 4039), Not(G_D[i] == 3647), Not(G_D[i] == 511), "
    if finger_limit < 2:
        s = s + "Not(G_D[i] == 4032), Not(G_D[i] == 3640), Not(G_D[i] == 3591), Not(G_D[i] == 504), Not(G_D[i] == 455), Not(G_D[i] == 63), "
        
    s = s[:-2] + "))\n"

    return s

# Left and right buttons on this finger will not be used and are reserved for numbers and symbols.
reserved_finger = "pinky"
# Forbid chords involving more than this many fingers.
finger_limit = 2
# All unique finger combinations of size finger_limit are limited to only this many chords.
#   The cheapest chords are selected.
max_chords_per_finger_limit = 3

(chord_cost, forbidden_chords) = custom_chord_cost(finger_limit, reserved_finger, max_chords_per_finger_limit)
print("---------------------------------------------------------------------------")
print(chord_cost)
print("---------------------------------------------------------------------------")
forbidden_finger_combos = forbidden(finger_limit)
print("---------------------------------------------------------------------------")
print(forbidden_finger_combos)
print(forbidden_chords)
print("---------------------------------------------------------------------------")

        # s.add( And( Not(G_D[i] == 4095), Not(G_D[i] == 4088), Not(G_D[i] == 4039), Not(G_D[i] == 3647), Not(G_D[i] == 511)))
