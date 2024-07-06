from ortools.linear_solver import pywraplp
import pandas as pd 
from func_timeout import func_set_timeout
from utils import define_zeta
import craft0 as data
from craft0 import generate_data
import ipdb
class Model:
    def __init__(self, input):
        self.input = input
    
    @func_set_timeout(10)
    def solve(self):
        crafts = self.input.Crafts
        crafts_num = self.input.CraftQuantities

        solver = pywraplp.Solver.CreateSolver('SAT')
        solver.time_limit = 10
        if not solver:
            print('---------Not SAT SOLVER----------')

        constants = self.define_constants(crafts, crafts_num)
        variables = self.define_variables(solver, constants)
        solver = self.define_constraints(solver, constants, variables, crafts, crafts_num)

        s, y, Z = variables
        solver.Minimize(Z)
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            print('Solution:')
            print('Objective value =', solver.Objective().Value())
            print('Z =', Z.solution_value())
        else:
            statusname = {pywraplp.Solver.FEASIBLE: 'feasible, or stopped by limit.',
                          pywraplp.Solver.INFEASIBLE: 'proven infeasible.',
                          pywraplp.Solver.UNBOUNDED: 'proven unbounded.',
                          pywraplp.Solver.ABNORMAL: 'abnormal, i.e., error of some kind.',
                          pywraplp.Solver.MODEL_INVALID: 'the model is trivially invalid (NaN coefficients, etc).',
                          pywraplp.Solver.NOT_SOLVED: 'not been solved yet.', }
            print('The problem does not have an optimal solution.')
            print(statusname.get(status))

        print('\nAdvanced usage:')
        print('Problem solved in %f milliseconds' % solver.wall_time())
        print('Problem solved in %d iterations' % solver.iterations())
        print('Problem solved in %d branch-and-bound nodes' % solver.nodes())

        # return self.output_result(constants, variables)
        return Z.solution_value()

    def define_constants(self, crafts, crafts_num):
        H, R, W, C, I, N, V, F, D, UP, DOWN, LB, UB = data.H, data.R, data.W, data.C, data.I, data.N, data.V, data.F, data.D, data.UP, data.DOWN, data.LB, data.UB

        M = 1000000
        e = 0.00001
        hoist_length = 1  # 天车之间至少要各几个槽位

        RI = [(r, i) for r in R for i in range(I[r], N[r])]
        RI_1 = [(r, i) for r in R for i in range(I[r] + 1, N[r])]
        RIUJ = [(r, i, u, j) for r in R for i in range(I[r], N[r]) for u in R for j in range(I[u], N[u]) if
                (r, i) != (u, j)]
        RIUJ_1 = [(r, i, u, j) for r in R for i in range(I[r] + 1, N[r]) for u in R for j in range(I[u] + 1, N[u]) if
                  (r, i) != (u, j)]
        zeta = define_zeta(H, R, N, V, C, D, F, M, I, UP, DOWN, hoist_length, W, RIUJ, data.H_Interval, data.Gear, data.Segments, 0, 0)
        return (
            H, R, W, C, I, N, V, F, D, UP, DOWN, zeta, M, e, RI, RI_1, RIUJ, RIUJ_1, LB, UB)
    
    def define_variables(self, solver, constants):
        H, R, W, C, I, N, V, F, D, UP, DOWN, zeta, M, e, RI, RI_1, RIUJ, RIUJ_1, LB, UB = constants
        infinity = solver.infinity()
        s = {(r, i): solver.IntVar(0.0, infinity, name=f's_{r}_{i}') for r in R for i in range(I[r], N[r])}

        y = {(r, i, u, j): solver.BoolVar(name=f'y_{r}_{i}_{u}_{j}') for r in R for i in range(I[r], N[r]) for u in R
             for j in range(I[u], N[u])}

        Z = solver.IntVar(0.0, infinity, name='Z')
        return s, y, Z

    def define_constraints(self, solver, constants, variables, crafts, crafts_num):
        H, R, W, C, I, N, V, F, D, UP, DOWN, zeta, M, e, RI, RI_1, RIUJ, RIUJ_1, LB, UB = constants
        s, y, Z = variables
        
        for r, i, u, j in RIUJ:
            solver.Add(s[u, j] - s[r, i] >= zeta[r, i, u, j, data.HP[u, j] - data.HP[r, i]] - M * (1 - y[r, i, u, j]))
            if V[r, i] == V[u, j]:
                solver.Add(s[u, j] - s[r, i] >= D[r, i] + F[V[r, i + 1], V[u, j]] - M * (1 - y[r, i, u, j]))
            if (r, i) != (u, j):
                solver.Add(y[r, i, u, j] + y[u, j, r, i] == 1)
        for r, i in RI:
            if i > I[r]:
                solver.Add(s[r, i] - s[r, i - 1] -D[r, i - 1] >= LB[r, i])
                solver.Add(s[r, i] - s[r, i - 1] -D[r, i - 1] <= UB[r, i])   
                solver.Add(Z >= s[r, i] + D[r, i])
        return solver

    def output_result(self, constants, variables):
        H, R, W, C, I, N, V, F, D, UP, DOWN, zeta, M, e, RI, RI_1, RIUJ, RIUJ_1, LB, UB = constants
        s, y, Z = variables
        output = {
            'Step': [],
            'Action': [],
            'Hoist': [],
            'Start': [],
            'Duration': [],
            'Tank': [],
            'NextTank': [],
            'Segment': [],
            'Item': [],
            # 'Process': [],
            # 'AcrossCycle':[],
            # 'T':[],
        }
        hoists = {}
        AcrossCycle = {}
        init_T = 0

        for r, i in s:
            hoists[r, i] = data.HP[r, i]
            AcrossCycle[r, i] = 0
            sri = s[r, i].solution_value()
            segment = -1
            # for index, seg in enumerate(self.input.Segments):
            #     if V[r, i] in seg and V[r, i + 1] in seg:
            #         segment = index
            #         break
            # else:
            #     segment = 'gear'

            if segment != 'gear':
                output['Step'].append(i)
                output['Action'].append('Up')
                output['Start'].append(sri)
                output['Duration'].append(UP[r, i])
                output['Segment'].append(segment)
                # output['T'].append(T.solution_value)
                output['Tank'].append(V[r, i])
                output['NextTank'].append(V[r, i])
                output['Hoist'].append(hoists[r, i])
                output['Item'].append(r)
                # output['Process'].append(Craft[r])
                # output['AcrossCycle'].append(AcrossCycle[r, i])

                output['Step'].append(i)
                output['Action'].append('Move')
                output['Start'].append(sri + UP[r, i])
                output['Duration'].append(F[V[r, i], V[r, i + 1]])
                output['Segment'].append(segment)
                # output['T'].append(T.solution_value)
                output['Tank'].append(V[r, i])
                output['NextTank'].append(V[r, i + 1])
                output['Hoist'].append(hoists[r, i])
                output['Item'].append(r)
                # output['Process'].append(Craft[r])
                # output['AcrossCycle'].append(AcrossCycle[r, i])

                output['Step'].append(i)
                output['Action'].append('Down')
                output['Start'].append(sri + UP[r, i] + F[V[r, i], V[r, i + 1]])
                output['Duration'].append(DOWN[r, i])
                output['Segment'].append(segment)
                # output['T'].append(T.solution_value)
                output['Tank'].append(V[r, i + 1])
                output['NextTank'].append(V[r, i + 1])
                output['Hoist'].append(hoists[r, i])
                output['Item'].append(r)
                # output['Process'].append(Craft[r])
                # output['AcrossCycle'].append(AcrossCycle[r, i])

            else:
                output['Step'].append(i)
                output['Action'].append('Up')
                output['Start'].append(sri)
                output['Duration'].append(D[r, i])
                output['Segment'].append(segment)
                # output['T'].append(T.solution_value)
                output['Tank'].append(V[r, i])
                output['NextTank'].append(V[r, i + 1])
                output['Hoist'].append(hoists[r, i])
                # output['AcrossCycle'].append(AcrossCycle[r, i])
                output['Item'].append(r)
                # output['Process'].append(Craft[r])
        return pd.DataFrame(output)

    def get_result(self):
        for index, craft in enumerate(self.input.Crafts):
            self.input.Crafts[index] = pd.DataFrame(craft)

        # 求解
        model_result = self.solve()
        return model_result
        # model_result.to_excel('output.xlsx')

        # 获取额外的绘制数据
        # lines, segments = read_data(model_result, self.input.HoistLaunchDuration, self.input.HoistTerminateDuration, False)
        # draw_result = add_empty_move_non_cycle(lines, segments, self.input.HoistLaunchDuration, self.input.HoistTerminateDuration)
        # empty_move_data = get_empty_move_data(draw_result)
        # write_data(lines)
        # plot(draw_result)

        # draw_data = []
        # for line in draw_result:
        #     for segment in line:
        #         if segment.__class__.__name__ in ['Move', 'Wait']:
        #             draw_data.append({
        #                 'Type': segment.__class__.__name__,
        #                 'Tank': getattr(segment, 'tank', None),
        #                 'STank': getattr(segment, 'stank', None),
        #                 'ETank': getattr(segment, 'etank', None),
        #                 'Start': getattr(segment, 'start', None),
        #                 'End': getattr(segment, 'end', None),
        #                 'Process': getattr(segment, 'process', None),
        #                 'Item': getattr(segment, 'item', None),
        #             })

        # return {
        #     'ModelResult': model_result.to_dict(orient='records'),
        #     # 'AdditionalDrawData': draw_data,
        #     # 'EmptyMoveData': empty_move_data,
        # }


if __name__ == '__main__':
    data.Crafts = [
        pd.read_excel('craft_0_2pcs.xlsx'),
    ]
    data.CraftQuantities = [2]
    import time
    res = {'time':[], 'Z':[]}
    for i in range(1, 21):
        start = time.time()
        R, I, N, LB, UB, V, F, D, UP, DOWN, HP = generate_data(i, 7)
        data.R, data.I, data.N, data.LB, data.UB, data.V, data.F, data.D, data.UP, data.DOWN, data.HP = R, I, N, LB, UB, V, F, D, UP, DOWN, HP
        model = Model(data)
        Z = model.get_result()
        end = time.time()
        res['time'].append(end - start)
        res['Z'].append(Z)
    res = pd.DataFrame(res)
    res.to_excel('result.xlsx')
