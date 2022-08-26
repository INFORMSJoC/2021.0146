"""
This module is used as an interface to call the MOSEK solver for solving (mixed-
integer) linear or second-order cone programs.
"""

import mosek
import numpy as np
from scipy.sparse import coo_matrix
from .socp import SOCProg
from .gcp import GCProg
import warnings
import time
from .lp import Solution


def solve(form, display=True, params={}):

    numlc, numvar = form.linear.shape
    if isinstance(form, (SOCProg, GCProg)):
        qmat = form.qmat
    else:
        qmat = []
    if isinstance(form, GCProg):
        xmat = form.xmat
    else:
        xmat = []

    ind_int = np.where(form.vtype == 'I')[0]
    ind_bin = np.where(form.vtype == 'B')[0]

    if ind_bin.size:
        form.ub[ind_bin] = np.minimum(1, form.ub[ind_bin])
        form.lb[ind_bin] = np.maximum(0, form.lb[ind_bin])

    ind_ub = np.where((form.ub != np.inf) & (form.lb == -np.inf))[0]
    ind_lb = np.where((form.lb != -np.inf) & (form.ub == np.inf))[0]
    ind_ra = np.where((form.lb != -np.inf) & (form.ub != np.inf))[0]
    ind_fr = np.where((form.lb == -np.inf) & (form.ub == np.inf))[0]
    ind_eq = np.where(form.sense)[0]
    ind_ineq = np.where(form.sense == 0)[0]

    with mosek.Env() as env:

        with env.Task(0, 0) as task:

            task.appendvars(numvar)
            task.appendcons(numlc)

            if ind_ub.size:
                task.putvarboundlist(ind_ub,
                                     [mosek.boundkey.up] * len(ind_ub),
                                     form.lb[ind_ub], form.ub[ind_ub])

            if ind_lb.size:
                task.putvarboundlist(ind_lb,
                                     [mosek.boundkey.lo] * len(ind_lb),
                                     form.lb[ind_lb], form.ub[ind_lb])

            if ind_ra.size:
                task.putvarboundlist(ind_ra,
                                     [mosek.boundkey.ra] * len(ind_ra),
                                     form.lb[ind_ra], form.ub[ind_ra])

            if ind_fr.size:
                task.putvarboundlist(ind_fr,
                                     [mosek.boundkey.fr] * len(ind_fr),
                                     form.lb[ind_fr], form.ub[ind_fr])

            if ind_int.size:
                task.putvartypelist(ind_int,
                                    [mosek.variabletype.type_int]
                                    * len(ind_int))

            if ind_bin.size:
                task.putvartypelist(ind_bin,
                                    [mosek.variabletype.type_int]
                                    * len(ind_bin))

            task.putcslice(0, numvar, form.obj.flatten())
            task.putobjsense(mosek.objsense.minimize)

            coo = coo_matrix(form.linear)
            task.putaijlist(coo.row, coo.col, coo.data)

            if ind_eq.size:
                task.putconboundlist(ind_eq, [mosek.boundkey.fx] * len(ind_eq),
                                     form.const[ind_eq], form.const[ind_eq])
            if ind_ineq.size:
                task.putconboundlist(ind_ineq,
                                     [mosek.boundkey.up] * len(ind_ineq),
                                     [-np.inf] * len(ind_ineq),
                                     form.const[ind_ineq])

            for cone in qmat:
                task.appendcone(mosek.conetype.quad,
                                0.0, cone)
            for cone in xmat:
                msk_cone = [cone[1], cone[2], cone[0]]
                task.appendcone(mosek.conetype.pexp, 0.0, msk_cone)

            if display:
                print('Being solved by Mosek...', flush=True)
                time.sleep(0.2)

            try:
                for param, value in params.items():
                    if isinstance(value, float):
                        task.putdouparam(getattr(mosek.dparam, param), value)
                    if isinstance(value, int):
                        task.putintparam(getattr(mosek.iparam, param), value)
                    if isinstance(value, str):
                        task.putstrparam(getattr(mosek.sparam, param), value)
            except (TypeError, ValueError, AttributeError):
                raise ValueError('Incorrect parameters or values.')

            t0 = time.time()
            task.optimize()
            stime = time.time() - t0

            soltype = mosek.soltype
            solsta = None

            if 'B' in form.vtype or 'I' in form.vtype:
                stype = soltype.itg
            elif not qmat and not xmat:
                stype = soltype.bas
            else:
                stype = soltype.itr

            solsta = task.getsolsta(stype)
            if display:
                print('Solution status: {0}'.format(solsta.__repr__()))
                print('Running time: {0:0.4f}s'.format(stime))

            xx = [0.] * numvar
            task.getxx(stype, xx)

            # if export:
            #     task.writedata("out.mps")

            if solsta in [mosek.solsta.optimal, mosek.solsta.integer_optimal]:
                solution = Solution(xx @ form.obj.flatten(), xx, solsta, stime)
            else:
                warnings.warn('Fail to find the optimal solution.')
                solution = None

            return solution
