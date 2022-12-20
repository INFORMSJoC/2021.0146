"""
Module used as an interface to call the OR-Tools solver for solving
(mixed-integer) linear programming problems of RSOME models.

Copyright 2020-2022 Peng Xiong, & Zhi Chen

This file is a part of RSOME

This file may be used under the terms of the GNU General Public License
version 3 as published by the Free Software Foundation and appearing in
the file LICENSE.GPL included in the packaging of this file.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from ortools.linear_solver import pywraplp

import numpy as np
import warnings
import time
from .lp import Solution
from numbers import Real


def solve(formula, display=True, params={}):

    try:
        if formula.qmat:
            warnings.warn('the LP solver ignnores SOC constriants.')
    except AttributeError:
        pass

    try:
        if formula.xmat:
            warnings.warn('The LP solver ignores exponential cone constriants.')
    except AttributeError:
        pass

    obj = formula.obj.flatten()
    linear = formula.linear
    sense = formula.sense
    const = formula.const
    ub = formula.ub
    lb = formula.lb
    vtype = formula.vtype

    if all(vtype == 'C'):
        solver = pywraplp.Solver.CreateSolver('GLOP')
    else:
        solver = pywraplp.Solver.CreateSolver('SCIP')

    row, col = linear.shape

    xs = [solver.NumVar(lb[i], ub[i], 'x' + str(i)) if vtype[i] == 'C' else
          solver.IntVar(max(0, lb[i]), min(1, ub[i]),
                        'x' + str(i)) if vtype[i] == 'B' else
          solver.IntVar(lb[i], ub[i], 'x' + str(i)) for i in range(col)]

    solver.Minimize(sum([obj[i] * xs[i] for i in range(col)]))

    for j in range(row):
        indices = linear[j].indices
        coeff = linear[j].data
        nz = len(indices)
        left = sum([coeff[i] * xs[indices[i]] for i in range(nz)])
        if not isinstance(left, Real):
            if sense[j] == 1:
                solver.Add(left == const[j])
            else:
                solver.Add(left <= const[j])

    if display:
        print('Being solved by OR-Tools...', flush=True)
        time.sleep(0.2)
    t0 = time.time()
    status = solver.Solve()
    stime = time.time() - t0
    if display:
        print('Solution status: {0}'.format(status))
        print('Running time: {0:0.4f}s'.format(stime))

    if status == pywraplp.Solver.OPTIMAL:
        x_sol = np.array([xs[i].solution_value() for i in range(col)])
        solution = Solution(solver.Objective().Value(), x_sol, status, stime)
    else:
        warnings.warn('Fail to find the optimal solution.')
        solution = None

    return solution
