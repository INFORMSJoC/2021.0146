from rsome import ro
from rsome import dro
from rsome import eco_solver as eco
import rsome as rso
import numpy as np


def test_ro_model():

    n = 150
    step = 1
    i = np.arange(1, n+1, step)
    p = 1.15 + 0.05/n*i
    sig = 0.05/450 * (2*i*n*(n+1))**0.5
    phi = 5

    model = ro.Model()
    x = model.dvar(len(i))

    model.max(p@x + phi*rso.quad(x, -np.diag(sig**2)))
    model.st(sum(x) == 1)
    model.st(x >= 0)

    model.solve(eco)
    model.get()

    objval = 1.18534

    assert abs(model.get() - objval) < 1e-4

    primal_sol = model.do_math().solve(eco)
    assert abs(primal_sol.objval + objval) < 1e-4

    dual_sol = model.do_math(primal=False).solve(eco)
    assert abs(dual_sol.objval - objval) < 1e-4

    dual_sol = model.do_math(primal=False).solve(eco)
    assert abs(dual_sol.objval - objval) < 1e-4


def test_dro_model():

    n = 150
    step = 1
    i = np.arange(1, n+1, step)
    p = 1.15 + 0.05/n*i
    sig = 0.05/450 * (2*i*n*(n+1))**0.5
    phi = 5

    model = dro.Model()
    x = model.dvar(len(i))

    model.max(p@x - phi*rso.quad(x, np.diag(sig**2)))
    model.st(sum(x) == 1)
    model.st(x >= 0)

    model.solve(eco)
    model.get()

    objval = 1.18534

    assert abs(model.get() - objval) < 1e-4

    primal_sol = model.do_math().solve(eco)
    assert abs(primal_sol.objval + objval) < 1e-4

    dual_sol = model.do_math(primal=False).solve(eco)
    assert abs(dual_sol.objval - objval) < 1e-4

    dual_sol = model.do_math(primal=False).solve(eco)
    assert abs(dual_sol.objval - objval) < 1e-4
