"""
Module used as an interface to call the CyLP solver for solving
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

from cylp.cy import CyClpSimplex
from cylp.py.modeling.CyLPModel import CyLPArray

import numpy as np
import warnings
import time
from .lp import Solution


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

    eq_linear = linear[sense == 1, :]
    eq_const = const[sense == 1]
    ineq_linear = linear[sense == 0, :]
    ineq_const = const[sense == 0]

    is_con = vtype == 'C'
    is_int = vtype == 'I'
    is_bin = vtype == 'B'

    s = CyClpSimplex()

    obj_expr = 0
    ncv = sum(is_con)
    if ncv:
        cv = s.addVariable('cv', ncv)
        s += cv <= ub[is_con]
        s += cv >= lb[is_con]
        obj_expr += CyLPArray(obj[is_con]) * cv

    niv = sum(is_int)
    if niv:
        iv = s.addVariable('iv', niv, isInt=True)
        s += iv <= ub[is_int]
        s += iv >= lb[is_int]
        obj_expr += CyLPArray(obj[is_int]) * iv

    nbv = sum(is_bin)
    if nbv:
        bv = s.addVariable('bv', nbv, isInt=True)
        s += bv <= np.minimum(1, ub[is_bin])
        s += bv >= np.maximum(0, lb[is_bin])
        obj_expr += CyLPArray(obj[is_bin]) * bv
    s.objective = obj_expr

    if eq_linear.shape[0] > 0:
        left = 0
        if ncv:
            left += eq_linear[:, is_con] * cv
        if niv:
            left += eq_linear[:, is_int] * iv
        if nbv:
            left += eq_linear[:, is_bin] * bv

        s += (left == eq_const)

    if ineq_linear.shape[0] > 0:
        left = 0
        if ncv:
            left += ineq_linear[:, is_con] * cv
        if niv:
            left += ineq_linear[:, is_int] * iv
        if nbv:
            left += ineq_linear[:, is_bin] * bv

        s += (left <= ineq_const)
        # print(ineq_linear[:, is_bin].toarray())

    cbcModel = s.getCbcModel()
    s.writeLp('blah.lp')

    if display:
        print('Being solved by CyLP...', flush=True)
        time.sleep(0.2)
    t0 = time.time()
    # status = s.primal()
    cbcModel.solve()
    stime = time.time() - t0
    status = cbcModel.status
    if display:
        print('Solution status: {0}'.format(status))
        print('Running time: {0:0.4f}s'.format(stime))

    if status == 'solution':
        x_sol = np.zeros(linear.shape[1])
        if ncv:
            x_sol[is_con] = cbcModel.primalVariableSolution['cv']
        if niv:
            x_sol[is_int] = cbcModel.primalVariableSolution['iv']
        if nbv:
            x_sol[is_bin] = cbcModel.primalVariableSolution['bv']

        solution = Solution(cbcModel.objectiveValue, x_sol, status, stime)

    else:
        warnings.warn('Fail to find the optimal solution.')
        solution = None

    return solution
