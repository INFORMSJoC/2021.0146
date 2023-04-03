[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# [RSOME in Python: An Open-Source Package for Robust Stochastic Optimization Made Easy](https://doi.org/10.1287/ijoc.2023.1291)

This archive is distributed in association with the [INFORMS Journal on
Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

The software and data in this repository are a snapshot of the software and data
that were used in the research reported on in the paper 
[RSOME in Python: An Open-Source Package for Robust Stochastic Optimization Made Easy](https://doi.org/10.1287/ijoc.2023.1291) by Zhi Chen and Peng Xiong.
The snapshot is based on 
[this SHA](https://github.com/tkralphs/JoCTemplate/commit/f7f30c63adbcb0811e5a133e1def696b74f3ba15) 
in the development repository. 

**Note: RSOME in Python is being developed, on an on-going basis, at 
https://github.com/XiongPengNUS/rsome. Please visit there if you would like to
get a more recent version or would like to find support.**

## Cite

To cite this software, please cite the paper, using its DOI, and  using the following DOI.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7463845.svg)](https://doi.org/10.5281/zenodo.7463845)

Below is the BibTex for citing this version of the code.

```
@article{chen2021rsome,
  author={Chen, Zhi and Xiong, Peng},
  publisher={INFORMS Journal on Computing},
  title={{RSOME} in Python: an open-source package for robust stochastic optimization made easy, Version v2021.0146},
  year={2022},
  doi={10.5281/zenodo.7463845},
  url={https://github.com/INFORMSJoC/2021.0146}
}  
```

## Description

### Introduction

RSOME (Robust Stochastic Optimization Made Easy) is an open-source Python package for generic modeling of optimization problems (subject to uncertainty). Models in RSOME are constructed by variables, constraints, and expressions that are formatted as N-dimensional arrays. These arrays are consistent with the NumPy library in terms of syntax and operations, including broadcasting, indexing, slicing, element-wise operations, and matrix calculation rules, among others. In short, RSOME provides a convenient framework to facilitate developments of robust and distributionally optimization models as well as their applications.

### Installation

The RSOME package can be installed by using the <code>pip</code> command:

```
pip install rsome
```

### Supported Solvers

The current version of RSOME supports a rich variety of open-source and commerical solvers. Once installed, these solvers can be called to solve RSOME models via the specialized solver interfaces. The table below summarizes all supported solvers and their RSOME interfaces. 

| Solver                                                                                                                                          | License  type | Required version | RSOME interface | Integer variables | Second-order cone constraints | Exponential cone constraints |
|:----------------------------------------------------------------------------------------------------------------------------------------------- |:------------- |:---------------- |:--------------- |:----------------- |:----------------------------- |:---------------------------- |
| [scipy.optimize](https://docs.scipy.org/doc/scipy/reference/optimize.html)                                                                      | Open-source   | >= 1.2.1         | `lpg_solver`    | No                | No                            | No                           |
| [CyLP](https://github.com/coin-or/cylp)                                                                                                         | Open-source   | >= 0.9.0         | `clp_solver`    | Yes               | No                            | No                           |
| [OR-Tools](https://developers.google.com/optimization/install)                                                                                  | Open-source   | >= 7.5.7466      | `ort_solver`    | Yes               | No                            | No                           |
| [ECOS](https://github.com/embotech/ecos-python)                                                                                                 | Open-source   | >= 2.0.10        | `eco_solver`    | Yes               | Yes                           | Yes                          |
| [Gurobi](https://www.gurobi.com/documentation/9.0/quickstart_mac/ins_the_anaconda_python_di.html)                                               | Commercial    | >= 9.1.0         | `grb_solver`    | Yes               | Yes                           | No                           |
| [MOSEK](https://docs.mosek.com/9.2/pythonapi/install-interface.html)                                                                            | Commercial    | >= 9.1.11        | `msk_solver`    | Yes               | Yes                           | Yes                          |
| [CPLEX](https://www.ibm.com/support/knowledgecenter/en/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/Python_setup.html) | Commercial    | >= 12.9.0.0      | `cpx_solver`    | Yes               | Yes                           | No                           |
| [COPT](https://www.shanshu.ai/copt)                                                                                                             | Commercial    | >= 5.0           | `cpt_solver`    | Yes               | Yes                           | No                           |

## Additional Information

This repository contains the following folders:

- The `src` folder provides the source code of the RSOME package.
- The `docs` folder provides files for building the office webpage of RSOME.
- The `cases` folder provides the code for replicating all numerical case studies in the paper and the online supplementary document.

Detailed documentation of RSOME can be found from:

- [RSOME quick start](https://xiongpengnus.github.io/rsome/)
- [RSOME users guide](https://xiongpengnus.github.io/rsome/user_guide)
- [Application examples](https://xiongpengnus.github.io/rsome/examples)

The code is being developed on an on-going basis at the authors' [Github site](https://github.com/XiongPengNUS/rsome).
