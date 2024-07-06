import sys
import argparse
import ipdb
import re
import glob
import copy

def parse_arguments(argv) :
    print(argv)
    parser = argparse.ArgumentParser( description = "Input" )
    parser.add_argument( "--stocking_slot", required=True, type = list, help="Stocking slot")
    parser.add_argument( "--blanking_slot", required=True, type = list, help="blanking_slot")
    parser.add_argument( "--border_slot", required=True, type = list, help="Border_slot")
    parser.add_argument( "--num_tanks", required=True, type = int, help="Number of tanks" )
    parser.add_argument( "--num_hoists", required=True, type = int, help="Number of hoists" )
    
    parser.add_argument( "--hoist_interval", required=True, type = list, help="hoist_interval")
    parser.add_argument( "--hoist_position", required=True, type = list, help="hoist_position")
    
    parser.add_argument( "--hoist_moving_duration", required=True, type = int, help="hoist_moving_duration")
    parser.add_argument( "--hoist_start_duaration", required=True, type = int, help="hoist_start_duaration")
    parser.add_argument( "--hoist_stop_duration", required=True, type = int, help="hoist_stop_duration")
    parser.add_argument( "--hoist_load_duration", required=True, type = int, help="hoist_load_duration")
    parser.add_argument( "--hoist_unload_duration", required=True, type = int, help="hoist_unload_duration")
    parser.add_argument( "--problem", required=True, type = str, help="problem")
    args = parser.parse_args()
    return args

def gen_problem(TNum, HNum, P, hoist_interval, hoist_position):
    T = TNum
    H = HNum
    
    stocking_slot=[0]
    blanking_slot=[T - 1]
    border_slot=[0, T - 1]

    s_index = 0
    hoist_interval=hoist_interval
    hoist_position=hoist_position

    hoist_moving_duration=1
    hoist_start_duaration=2
    hoist_stop_duration=2
    hoist_load_duration=5
    hoist_unload_duration=5

    problem='problem.pddl'

    problem = open(problem, 'w')

    str1 = f'''
        (define (problem electroplating)
        (:domain Electroplating)
        (:objects
    '''     
    print(str1, file = problem)
    for i in range(H):
        print(f'pole{i} - pole', file = problem)

    for i in range(s_index, T + s_index, 1):
        print(f'slot{i} - slot', file = problem)

    for p in P:
        print(f'p{p} - product', file = problem)

    print(f')', file = problem)

    print(f'(:init', file = problem)
    
    for slot in border_slot:
        print(f'(border_slot slot{slot})', file = problem)

    for slot in stocking_slot:
        print(f'(stocking_slot slot{slot})', file = problem)

    for slot in blanking_slot:
        print(f'(blanking_slot slot{slot})', file = problem)

    for p in P:
        print(f'(product_at p{p} slot0)', file = problem)
    
    for index, position in enumerate(hoist_position):
        print(f'(pole_position pole{index} slot{position})', file = problem)
        print(f'(pole_start_moving pole{index })', file = problem)
        print(f'(slot_have_pole slot{position})', file = problem)
        print(f'(pole_available pole{index})', file = problem)
        print(f'(pole_empty pole{index})', file = problem)
        lower = hoist_interval[index].lower
        upper = hoist_interval[index].upper
        for k in range(lower, upper + 1, 1):
            print(f'(pole_region pole{index} slot{k})', file = problem)

    for i in range(s_index, T + s_index - 1, 1):
        print(f'(forward_slot_connection slot{i} slot{i + 1})', file = problem)
        print(f'(inverse_slot_connection slot{i + 1} slot{i})', file = problem)


    print(f'(= (pole_moving_duration_each_slot) {hoist_moving_duration})', file = problem)
    print(f'(= (pole_hangon_duration) {hoist_load_duration})', file = problem)
    print(f'(= (pole_hangoff_duration) {hoist_unload_duration})', file = problem)
    print(f'(= (pole_start_duration) {hoist_start_duaration})', file = problem)
    # print(f'(= (pole_stop_duration) {hoist_start_duaration})', file = problem)
    print(f')', file = problem)

    print(f'(:goal', file = problem)
    print(f'(and', file = problem)
    print(f')', file = problem)
    print(f')', file = problem)
    print(f')', file = problem)
    problem.close()

def gen_goal(state, parser, goal):
    state = state
    
    new_f = open(f'new_problem.pddl', 'w')

    print('(define (problem electroplating)', file=new_f)
    print('\t(:domain Electroplating)', file=new_f)
    print('\t(:objects', file=new_f)

    for object in parser.objects:
        for o in parser.objects[object]:
            print('\t\t'+o+' - '+object, file=new_f)

    print('\t\t)', file=new_f)
    print('\t(:init', file=new_f)

    for s in state:
        s = str(s)
        s = s.replace("'", '')
        s = s.replace(",", '')
        print('\t\t'+s, file=new_f)
    print('\t)', file=new_f)
    print('\t(:goal', file=new_f)
    print('\t(and', file=new_f)

    for g in goal:
        print('\t\t'+str(g), file=new_f)
    print('\t)', file=new_f)
    print('\t)', file=new_f)
    # print('\t(:metric minimize (TOTAL-TIME))', file=new_f)
    print(')', file=new_f)

    new_f.close()
    
def parser_sas(goal):
    actions_name = []
    products = ''
    start_poles = []
    move_poles = {}

    if goal:
        for name in glob.glob('tmp_sas_plan*'):
            tmp_plan = name

        for sg in goal:
            products = products + ' ' + sg
        try:
            with open(tmp_plan) as sas_plan:
                
                for line in sas_plan:
                    if ';' not in line:
                        line = line.strip('\n')
                        regMatch = re.findall(
                            r'(\d+\.\d+): ([(].*[)]) [[](\d+)\.\d+[]]', line)

                        if 'START-MOVING-POLE' in line:
                            reg = re.findall(r'(\d+\.\d+).*(POLE\d+)', line)[0]
                            start_poles.append((float(reg[0]), reg[1]))
                        if 'MOVE-POLE' in line:
                            reg = re.findall(r'(\d+\.\d+).*(POLE\d+)', line)[0]
                            move_poles[reg[1]] = float(reg[0])
                        # 删除多余的hangup动作，如果物品不在subgoal里，不执行它的hanggup动作
                        if 'HANGUP'  in line:
                            reg = regMatch[0][1].split(' ')
                            reg = reg[-1].split(')')
                            product = reg[0]
                            product = product.lower()
                            if product not in products:
                                print('出现多余的hangup hangup 动作')
                                # ipdb.set_trace()
                                continue
                        # 解析出来的动作，添加到actions_name
                        if regMatch != []:
                            actions_name.append(
                                (float(format(float(regMatch[0][0]), '.1f')), regMatch[0][1].lower(), float(format(float(regMatch[0][2])))))
        except:
            ipdb.set_trace()
            pass
    # self.is_invalid_action(start_poles, move_poles, actions_name)
    return actions_name
    
def parser_min_time(actions_name):
    min_end_time = 1000
    
    for time, act_name, duration in sorted(actions_name):
        if 'pole' in act_name:
            pole = re.findall(r'(pole\d+)', act_name)[0]
            pole = int(pole[4:])
            
            if 'hangoff' in act_name:
                if time + duration < min_end_time:
                    min_end_time = time + duration

    return min_end_time

def filter_actions(actions_name, min_end_time):
    temp_acts = []
    
    for time, act_name, duration in sorted(actions_name):
        
        reg = re.findall(r'(pole\d+)', act_name)
        
        if reg:
            pole = reg[0]
            
            if time <= min_end_time:
                
                temp_acts.append((time, act_name, duration))
    return temp_acts

def update_state(actions_name, min_end_time, state, parser):
    
    template_actions = parser.actions
    
    for time, act, duration in sorted(actions_name):
        if time <= min_end_time:
            sp = re.split('[( )]', act)
            sp = sp[1:-1]
            for action in template_actions:
                
                if action.name == sp[0]:
                    tem_act = copy.deepcopy(action)
                    param = []
                    param_map = {}
                    
                    for index, o in enumerate(tem_act.parameters):
                        param.append(o[0])
                        param_map[o[0]] = sp[index+1]
                    
                    for index, p in enumerate(tem_act.parameters):
                        tem_act.parameters[index] = sp[index+1]
                    
                    tem_act.positive_preconditions = sub_param(param, param_map, tem_act.positive_preconditions)
                    tem_act.negative_preconditions = sub_param(param, param_map, tem_act.negative_preconditions)
                    
                    tem_act.add_effects = sub_param(param, param_map, tem_act.add_effects)
                    tem_act.del_effects = sub_param(param, param_map, tem_act.del_effects)
                    
                    tem_act.numeric_effects = sub_param(param, param_map, tem_act.numeric_effects)
                    state = apply(tem_act.add_effects, tem_act.del_effects, tem_act.numeric_effects, 'at start', state)
                    
                    state = apply(tem_act.add_effects, tem_act.del_effects, tem_act.numeric_effects, 'at end', state)
                    break
    for s in state:
        if 'target_slot' in s:
            state.remove(s)
    return state
    
def get_hoist_position(state):
    hoist_position = {}
    for s in state:
        
        if 'pole_position' in s:
            pole = s[1]
            pole = int(pole[4:])
            tank = s[2]
            tank = int(tank[4:])
            hoist_position[pole] = tank
            
    return hoist_position
            # if product in products:
                
            #     position = int(s[2][4:])
                
            #     products[product].position = position
    
def get_product_position(state):
    product_position = {}
    for s in state:
        
        if 'product_at' in s:
            product = s[1]
            try:
                product = int(product[1:])
            except:
                ipdb.set_trace()
            tank = s[2]
            tank = int(tank[4:])
            product_position[product] = tank
            
    return product_position

def update_goal(goal, T, I):
    for g in goal:
        p = re.findall(r'(p\d+)', g)[0]
        p = int(p[1:])
        tank = re.findall(r'(slot\d+)', g)[0]
        tank = int(tank[4:])
        if tank == T[p, I[p]]:
            goal.remove(g)
    
    return goal         

def sub_param(param, param_map, pre_or_effect):
    
    pre_or_effect = list(pre_or_effect)
    
    for index1, pre in enumerate(pre_or_effect):
    
        pre_or_effect[index1] = list(pre_or_effect[index1])
    
        for index2, p in enumerate(pre):
    
            if p in param:
    
                pre_or_effect[index1][index2] = param_map[p]
    
        pre_or_effect[index1] = tuple(pre_or_effect[index1])
    
    return frozenset(pre_or_effect)  

def fliter_proposition(pro, time='all'):
    
    if time == 'all':
        
        temp = [p[1:] for p in pro]
    
    else:
    
        temp = [p[1:] for p in pro if p[0] == time or p[0] == 'over all']
    
    return temp

def apply(add_effects, del_effects, numeric_effects, time, state):
    
    temp_add = fliter_proposition(add_effects, time)
    
    temp_del = fliter_proposition(del_effects, time)

    state = list(tuple(set(state).difference(temp_del).union(temp_add)))
    
    return state

def get_SI1(actions_name, SI1, I, N, PL, P, min_end_time, parser, state, Flag):
    products = []
    for time, act_name, duration in sorted(actions_name):
        if 'hangup' in act_name:
            product = re.findall(r'(p\d+)', act_name)[0]
            product = int(product[1:])
            products.append(product)
            SI1[product] = time + min_end_time
            if Flag[product]:
                I[product] += 1 
                Flag[product] = False
        if 'hangoff' in act_name:
            Flag[product] = True
    new_SI1 = {}
    
    for p in list(SI1):
        if p in products and I[p] != N[p]:
            new_SI1[p] = SI1[p]
            if p not in PL:
                PL.append(p)
        else:
            new_SI1[p] = SI1[p] - min_end_time
        
    for p in list(SI1):
        if I[p] == N[p] and Flag[p]:
            if p in PL:
                PL.remove(p)
            if p in P:
                P.remove(p)
                parser, state = delete_product(parser, state, p)
        else:
            new_SI1[p] = SI1[p]
    return new_SI1, I, N, PL, P, parser, state

def delete_product(parser, state, p):
    parser.objects['product'].remove(f'p{p}')
    for s in state:
        if f'p{p}' in s:
            # if 'product_at' in s:
            #     position = int(s[2][4:])
            #     ipdb.set_trace()
            #     state.remove(f'(slot_not_available slot{position})')
            state.remove(s)
    return parser, state

def add_product_to_state(parser, state, data):
    p = max(data.P)
    state.append(('product_at', f'p{p}', 'slot0'))
    return state

def delete_unloading(state, unload_tank):
    for s in state:
        if f'(slot_not_available slot{unload_tank})' in state:
            state.remove(f'(slot_not_available slot{unload_tank})')