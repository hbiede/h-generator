from z3 import *
from datetime import datetime, timedelta
import lib
import sys

# Twiddler BitVector Index
#   L   M   R
#   11  10  9 - Index
#   8   7   6 - Middle
#   5   4   3 - Ring
#   2   1   0 - Pinky

setupTime = datetime.now()
s = Solver()
set_option(max_args=10000000, max_lines=1000000, max_depth=10000000, max_visited=1000000)
p = lib.Parameters.setup()
n = lib.NGrams.load_G_H(p)
b = lib.problem_def(s, n, p)

# ********************************
# |   Incorporate all of these   |
# |   into problem_def() above   |
# ********************************
# lib.mcc_from_scc(s, n, b)

# These letters frequently end words, so we don't want them
#   using the index finger, so they stride with SPACE.
# s.add(Extract(11, 11, b.F[n.index['E']]) == 0) #Ends 20.1% of words
# s.add(Extract(11, 11, b.F[n.index['S']]) == 0) #Ends 12.9% of words
# s.add(Extract(11, 11, b.F[n.index['D']]) == 0) #Ends 9.98% of words
# s.add(Extract(11, 11, b.F[n.index['N']]) == 0) #Ends 9.31% of words
# s.add(Extract(11, 11, b.F[n.index['T']]) == 0) #Ends 8.97% of words
# s.add(Extract(11, 11, b.F[n.index['Y']]) == 0) #Ends 6.00% of words
# s.add(Extract(11, 11, b.F[n.index['R']]) == 0) #Ends 5.90% of words
# s.add(Extract(11, 11, b.F[n.index['F']]) == 0) #Ends 4.71% of words
# s.add(Extract(11, 11, b.F[n.index['O']]) == 0) #Ends 4.18% of words
# s.add(Extract(11, 11, b.F[n.index['L']]) == 0) #Ends 3.47% of words
# s.add(Extract(11, 11, b.F[n.index['G']]) == 0) #Ends 2.94% of words
# s.add(Extract(11, 11, b.F[n.index['A']]) == 0) #Ends 2.82% of words
# s.add(Extract(11, 11, b.F[n.index['H']]) == 0) #Ends 2.71% of words

# If E cannot use *M** can it achieve 2.6846? If not fix E here.
# s.add(Extract(7, 7, b.G[n.index['E']]) == 0)


# ******************************************************
# ******************************************************
# |   Problem: Minimize b.total_cost  |
# ******************************************************
# ******************************************************


# **************************************************
# Sit back relax and let the SMT solver do the work.
# **************************************************

# Timeout is given in milliseconds
s.set("timeout", (p.timeout.days * 24 * 60 * 60 + p.timeout.seconds) * 1000)
print(f"N-Grams: {str(len(n.G))}, Setup Time: {datetime.now() - setupTime}")
print("---------------------------------------------------------------------------------------------")
print(f"Cost Constraint         - Actual Cost             - Result  - Time:This Run  - Time:All Runs")

lo_sat = float("inf")
hi_unsat = 0
hi_unknown = 0
search_has_failed = False
last_print_time = datetime.min
last_sat_time = datetime.min
solver_time = datetime.now()
last_was_update = False
m = None # Output of latest SAT solver model
# See comments above in "Guide the Search" for understanding how this works.
while min(lo_sat, p.cost_hi) - max(hi_unsat, hi_unknown, p.cost_lo) > p.cost_res:
    solveTime = datetime.now()

    # We start from p.cost_hi initially and decrement up by initial_step_up()
    #   until we encounter an UNSAT or UNKNOWN problem then we decrement by
    #   after_failure_step_up().
    if not search_has_failed:
        guess_cost = min(lo_sat, p.cost_hi - p.initial_step_up()) - p.initial_step_up()
    else:
        guess_cost = p.after_failure_step_up(min(lo_sat, p.cost_hi),
                                            max(hi_unsat, hi_unknown, p.cost_lo))
    assert lo_sat >= guess_cost
    assert hi_unknown <= guess_cost
    assert hi_unsat <= guess_cost

    # We add the constraint the the total cost must be less than or equal
    #   to the guess_cost. Pushing a new state allows us to remove this constraint
    #   if it turns out to be UNSAT/UNKNOWN.
    s.push() # Create new state
    s.add(b.total_cost <= guess_cost)
    
    result = s.check()
    guess_time = datetime.now() - solveTime
    
    if result == sat:
        lo_sat = guess_cost
        m = s.model()
        if datetime.now() >= last_sat_time + p.sat_time:
            last_sat_time = datetime.now()
            lib.print_details(s, m, b, n)
    elif result == unsat:
        hi_unsat = guess_cost
        search_has_failed = True
        s.pop() # Restore state (i.e. Remove guess constraint)
                # Only remove guess constraint when it can't be attained, not when sat.
    elif result == unknown:
        hi_unknown = guess_cost
        search_has_failed = True
        s.pop() # Restore state (i.e. Remove guess constraint)
                # Only remove guess constraint when it can't be attained, not when sat.

    if datetime.now() >= last_print_time + p.update_time:
        if last_was_update:
            print("") # Print newline
            last_was_update = False
        last_print_time = datetime.now()
        if result == sat:
            actual_cost = int(str(m[b.total_cost]))
            print(f"{guess_cost:<28,} - {actual_cost:<28,} - {str(result):7} - {guess_time} - {datetime.now() - solver_time}")
        else:
            print(f"{guess_cost:<28,} -                         - {str(result):7} - {guess_time} - {datetime.now() - solver_time}")
    else:
        print(f".", flush=True, end="")
        last_was_update = True


if last_was_update:
    print("") # Print newline
print("---------------------------------------------------------------------------------------------")
print(f"Sat: {lo_sat}, Unknown: {hi_unknown}, Unsat: {hi_unsat}")
print(f"Total Time: {datetime.now() - setupTime}")
print("---------------------------------------------------------------------------------------------")

lib.print_details(s, m, b, n)

lib.print_details(s, m, b, n)
# ******************************************************
# TODO: Convert SMT solver output to configuration file.
# ******************************************************