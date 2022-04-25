from z3 import *
from datetime import datetime, timedelta
import lib

# Twiddler BitVector Index
#   L   M   R
#   11  10  9 - Index
#   8   7   6 - Middle
#   5   4   3 - Ring
#   2   1   0 - Pinky

setupTime = datetime.now()
s = Solver()
p = lib.Parameters.setup()
n = lib.NGrams.load_G_H(p)
b = lib.problem_def(s, n, p)


# ******************************************************
# ******************************************************
# |          Problem: Minimize b.total_cost            |
# ******************************************************
# ******************************************************


# **************************************************
# Sit back relax and let the SMT solver do the work.
# **************************************************

s.set("auto_config", True)
print(f"N-Grams: {str(len(n.G))}, Setup Time: {datetime.now() - setupTime}, Current Time: {datetime.now()}")
print("---------------------------------------------------------------------------------------------")
print(f"Cost Constraint         - Actual Cost             - Result  - Time:This Run  - Time:All Runs")

lo_sat = float("inf")
hi_unsat = 0
hi_unknown = 0
search_has_failed = False
last_print_time = datetime.min
last_sat_time = datetime.min
solver_start_time = datetime.now()
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
    
    solver_elapsed_time = datetime.now() - solver_start_time
    this_timeout = min(p.timeout, p.max_time - solver_elapsed_time)
    this_timeout_millisec = (this_timeout.days * 24 * 60 * 60 + this_timeout.seconds) * 1000
    if this_timeout_millisec <= 0:
        break
    # Timeout is given in milliseconds
    s.set("timeout", this_timeout_millisec)
    result = s.check()
    guess_time = datetime.now() - solveTime
    all_run_time = datetime.now() - solver_start_time

    if result == sat:
        m = s.model()
        actual_cost = int(str(m[b.total_cost]))
        lo_sat = actual_cost
        if datetime.now() >= last_sat_time + p.sat_time:
            last_sat_time = datetime.now()
            lib.print_details(s, m, b, n, guess_time, all_run_time)

        # Sometimes after a timeout (i.e. unknown) a subsequent guess
        #   will be better than the guess_cost that timed_out. In this case
        #   we reset the highest unknown to 0. 
        if lo_sat < hi_unknown:
            hi_unknown = 0
        assert lo_sat > hi_unsat
    elif result == unsat:
        hi_unsat = guess_cost
        search_has_failed = True
        lib.print_details(s, m, b, n, guess_time, all_run_time)
        s.pop() # Restore state (i.e. Remove guess constraint)
                # Only remove guess constraint when it can't be attained, not when sat.
    elif result == unknown:
        hi_unknown = guess_cost
        search_has_failed = True
        lib.print_details(s, m, b, n, guess_time, all_run_time)
        s.pop() # Restore state (i.e. Remove guess constraint)
                # Only remove guess constraint when it can't be attained, not when sat.

    if datetime.now() >= last_print_time + p.update_time:
        if last_was_update:
            print("") # Print newline
            last_was_update = False
        last_print_time = datetime.now()
        actual_cost = int(str(m[b.total_cost]))
        print(f"{int(guess_cost):<23,} - {actual_cost:<23,} - {str(result):7} - {guess_time} - {all_run_time}")
    else:
        print(f".", flush=True, end="")
        last_was_update = True


if last_was_update:
    print("") # Print newline
print("---------------------------------------------------------------------------------------------")
print(f"Sat: {lo_sat}, Unknown: {hi_unknown}, Unsat: {hi_unsat}")
print(f"Total Time: {datetime.now() - setupTime}")
print("---------------------------------------------------------------------------------------------")

print("---------------------------------------------------------------------------------------------", file=sys.stderr)
print("********************************** Reprinting last SAT run **********************************", file=sys.stderr)
print("---------------------------------------------------------------------------------------------", file=sys.stderr)
lib.print_details(s, m, b, n, guess_time, all_run_time)

# ******************************************************
# TODO: Convert SMT solver output to configuration file.
# ******************************************************