from model import *
from gen_problems import *
from craft import data, add_product, generate_process
import subprocess
import PDDL
import copy
craft = generate_process(data.hoist_interval, data.W)
add_product(craft, data)
gen_problem(data.W, len(data.hoist_interval), [10000], data.hoist_interval, data.hoist_position)
domain = 'domain.pddl'
problem = 'problem.pddl'
parser = PDDL.init_parser(domain, problem)
parser.state_to_tuple()
state = copy.deepcopy(parser.state)
goal = []
S = {}
Flag = {}
def add_product_to_PL(parser, state, Flag, data):
    goals = []
    p = data.P.pop(0)
    data.PL.append(p)
    parser.objects['product'].append(f'p{p}')
    state.append(('product_at', f'p{p}', 'slot0'))
    Flag[p] = True
    data.SI1[p] = 0
add_product_to_PL(parser, state, Flag, data)
for i in range(1000):
    res = solver(data, S)
    while res == None:
        for r, i in S:
            data.LB[r, i] -= 0.1 * data.LB[r, i]
            data.UB[r, i] += 0.1 * data.UB[r, i]
        res = solver(data, S)
    S = res
    min_end_time = 1000
    
    for r in data.PL:
        if min_end_time > S[r, data.I[r]]:
            min_end_time = S[r, data.I[r]] 
    for r in data.PL:
        if S[r, data.I[r]] <= min_end_time + data.D[r, data.I[r]]:
            goal.append(f'(product_at p{r} slot{data.T[r, data.I[r] + 1]})')
            state.append(f'(target_slot slot{data.T[r, data.I[r] + 1]} p{r})')
    goal = list(set(goal))
    gen_goal(state, parser, goal)
    subprocess.run(f'python2 ~/Documents/temporal-planning/bin/plan.py she domain.pddl new_problem.pddl --no-iterated  --time 5 > console_output.txt', shell=True)
    actions_name = parser_sas(goal)
    
    data.TS = parser_min_time(actions_name) + min_end_time
    for r in data.P:
        if min_end_time < S[r, data.I[r]] < data.TS:
            data.TS = S[r, data.I[r]]
    actions_name = filter_actions(actions_name, data.TS - min_end_time)
    state = update_state(actions_name, data.TS, state, parser)
    data.hoist_position = get_hoist_position(state)
    data.product_position = get_product_position(state)
    data.SI1, data.I, data.N, data.PL, data.P, parser, state = get_SI1(actions_name, data.SI1, data.I, data.N, data.PL, data.P, min_end_time, parser, state, Flag)
    goal = update_goal(goal, data.T, data.I)
    if not data.P:
        break
    print(data.SI1, data.I, data.product_position, goal)
    
    if i > 0 and i == 10 or i == 20:
        add_product_to_PL(parser, state, Flag, data)
        
