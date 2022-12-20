"""
Module used as an interface to call the Gurobi solver for solving
(mixed-integer) linear or second-order cone programs of RSOME models.

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

import gurobipy as gp
import numpy as np
import warnings
import time
from .socp import SOCProg
from .lp import Solution


def solve(formula, display=True, params={}):

    try:
        if formula.xmat:
            warnings.warn('The SOCP solver ignores exponential cone constraints. ')
    except AttributeError:
        pass

    nv = formula.linear.shape[1]
    vtype = list(formula.vtype)

    grb = gp.Model()
    x = grb.addMVar(nv, lb=formula.lb, ub=formula.ub, vtype=vtype)

    indices_eq = (formula.sense == 1)
    indices_ineq = (formula.sense == 0)
    linear_eq = formula.linear[indices_eq, :]
    linear_ineq = formula.linear[indices_ineq, :]
    const_eq = formula.const[indices_eq]
    const_ineq = formula.const[indices_ineq]
    if len(indices_eq) > 0:
        grb.addMConstr(linear_eq, x, '=', const_eq)
        # grb.addMConstrs(linear_eq, x, '=', const_eq)
    if len(indices_ineq) > 0:
        grb.addMConstr(linear_ineq, x, '<', const_ineq)
        # grb.addMConstrs(linear_ineq, x, '<', const_ineq)

    if isinstance(formula, SOCProg):
        for constr in formula.qmat:
            index_right = constr[0:1]
            index_left = constr[1:]
            A = np.eye(len(index_left))
            grb.addConstr(x[index_left] @ A @ x[index_left] <=
                          x[index_right] @ x[index_right])

    grb.setObjective(formula.obj @ x)

    grb.setParam('LogToConsole', 0)
    try:
        for param, value in params.items():
            if eval('grb.Params.{}'.format(param)) is None:
                raise ValueError('Unknown parameter')
            grb.setParam(param, value)

    except (TypeError, ValueError):
        raise ValueError('Incorrect parameters or values.')
    if display:
        print('Being solved by Gurobi...', flush=True)
        time.sleep(0.2)
    grb.optimize()
    if display:
        print('Solution status: {0}'.format(grb.Status))
        print('Running time: {0:0.4f}s'.format(grb.Runtime))

    # if export:
    #     grb.write("out.lp")

    try:
        solution = Solution(grb.ObjVal, grb.getAttr('X'), grb.Status, grb.Runtime)
    except AttributeError:
        warnings.warn('Fail to find the optimal solution.')
        solution = None

    return solution
