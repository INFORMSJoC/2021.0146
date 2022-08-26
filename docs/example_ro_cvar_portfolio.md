<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

### Conditional Value-at-Risk in Robust Portfolio

This robust portfolio management model is proposed by [Zhu and Fukushima (2009)](#ref1). The portfolio allocation is determined via minimizing the worst-case conditional value-at-risk (CVaR) under ambiguous distribution information. The generic formulation is given as

$$
\begin{align}
\min~&\max\limits_{\pmb{\pi}\in \Pi} \alpha + \frac{1}{1-\beta}\pmb{\pi}^{\top}\pmb{u} &\\
\text{s.t.}~& u_k \geq \pmb{y}_k^{\top}\pmb{x} - \alpha, &\forall k = 1, 2, ..., s \\
&u_k \geq 0, &\forall k=1, 2, ..., s \\
&\sum\limits_{k=1}^s\pi_k\pmb{y}_k^{\top}\pmb{x} \geq \mu, &\forall \pmb{\pi} \in \Pi  \\
&\underline{\pmb{x}} \leq \pmb{x} \leq \overline{\pmb{x}} \\
&\pmb{1}^{\top}\pmb{x} = w_0
\end{align}
$$

with investment decisions\\(\pmb{x}\in\mathbb{R}^n\\) and auxiliary variables \\(\pmb{u}\in\mathbb{R}^s\\) and \\(\alpha\in\mathbb{R}\\), where \\(n\\) is the number of stocks, and \\(s\\) is the number of samples. The array \\(\pmb{\pi}\\) denotes the probabilities of samples, and \\(\Pi\\) is the uncertainty set that captures the distributional ambiguity of probabilities. The constant array \\(\pmb{y}_k\in\mathbb{R}^n\\) indicates the \\(k\\)th sample of stock return rates, and \\(\bar{x}\\) and \\(\underline{x}\\) are the lower and upper bounds of \\(x\\). The worst-case minimum expected overall return rate is set to be \\(\mu=0.001\\), the confidence level is \\(\beta=0.95\\), and the budget of investment is set to be \\(w_0=1\\). In this case study, we consider the sample data of five stocks "JPM", "AMZN", "TSLA", "AAPL", and	"GOOG" in the year of 2020, and the other parameters are specified by the following code segment.

```python
import pandas as pd
import yfinance as yf

stocks = ['JPM', 'AMZN', 'TSLA', 'AAPL', 'GOOG']
start = '2020-1-2'              # starting date of historical data
end='2020-12-31'                # end date of historical data

data = pd.DataFrame([])
for stock in stocks:
    each = yf.Ticker(stock).history(start=start, end=end)
    close = each['Close'].values
    returns = (close[1:] - close[:-1]) / close[:-1]
    data[stock] = returns

data
```

<div>
<table border="1" class="dataframe mystyle">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>JPM</th>
      <th>AMZN</th>
      <th>TSLA</th>
      <th>AAPL</th>
      <th>GOOG</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-0.013197</td>
      <td>-0.012139</td>
      <td>0.029633</td>
      <td>-0.009722</td>
      <td>-0.004907</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-0.000795</td>
      <td>0.014886</td>
      <td>0.019255</td>
      <td>0.007968</td>
      <td>0.024657</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-0.017001</td>
      <td>0.002092</td>
      <td>0.038801</td>
      <td>-0.004703</td>
      <td>-0.000624</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.007801</td>
      <td>-0.007809</td>
      <td>0.049205</td>
      <td>0.016086</td>
      <td>0.007880</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>247</th>
      <td>-0.004398</td>
      <td>-0.003949</td>
      <td>0.024444</td>
      <td>0.007712</td>
      <td>0.003735</td>
    </tr>
    <tr>
      <th>248</th>
      <td>0.006585</td>
      <td>0.035071</td>
      <td>0.002901</td>
      <td>0.035766</td>
      <td>0.021416</td>
    </tr>
    <tr>
      <th>249</th>
      <td>-0.002633</td>
      <td>0.011584</td>
      <td>0.003465</td>
      <td>-0.013315</td>
      <td>-0.009780</td>
    </tr>
    <tr>
      <th>250</th>
      <td>0.002800</td>
      <td>-0.010882</td>
      <td>0.043229</td>
      <td>-0.008527</td>
      <td>-0.010917</td>
    </tr>
  </tbody>
</table>
<p>251 rows × 5 columns</p>
</div>

```python
y = data.values     # stock data as an array
s, n = y.shape      # s: sample size; n: number of stocks

x_lb = np.zeros(n)  # lower bounds of investment decisions
x_ub = np.ones(n)   # upper bounds of investment decisions

beta =0.95          # confidence interval
w0 = 1              # investment budget
mu = 0.001          # target minimum expected return rate
```

#### Nominal CVaR model

In the nominal model, the CVaR and expected returns are evaluated assuming the exact distribution of stock returns is accurately represented by the historical samples without any distributional ambiguity. In other words, \\(\Pi\\) is written as a singleton uncertainty \\(\Pi = \\{\pmb{\pi}^0 \\}\\), where \\(\pi_k^0=1/s\\), with \\(k=1, 2, ..., s\\). The Python code for implementing the nominal model is given below.

```python
from rsome.rsome import ro
from rsome.rsome import msk_solver as msk

model = ro.Model()

pi = np.ones(s) / s

x = model.dvar(n)
u = model.dvar(s)
alpha = model.dvar()

model.min(alpha + 1/(1-beta) * (pi@u))
model.st(u >= y@x - alpha)
model.st(u >= 0)
model.st(pi@y@x >= mu)
model.st(x >= x_lb, x <= x_ub, x.sum() == w0)

model.solve(msk)
```

```
Being solved by Mosek...
Solution status: optimal
Running time: 0.0213s
```

The portfolio decision for the nominal model is retrieved by the following code.

```python
x.get().round(4)    # the optimal portfolio decision with 4 d.p.
```

```
array([0.3135, 0.5331, 0.0455, 0.    , 0.1079])
```

#### Worst-case CVaR model with box uncertainty
Now we consider a box uncertainty set

$$
\Pi = \left\{\pmb{\pi}: \pmb{\pi} = \pmb{\pi}^0 + \pmb{\eta}, \pmb{1}^{\top}\pmb{\eta}=0, \underline{\pmb{\eta}}\leq \pmb{\eta} \leq \bar{\pmb{\eta}} \right\}.
$$

In this case study, we assume that \\(-\underline{\pmb{\eta}}=\bar{\pmb{\eta}}=0.0001\\), and the Python code for implementation is provided below.

```python
from rsome.rsome import ro
from rsome.rsome import msk_solver as msk

model = ro.Model()

eta_ub = 0.0001                 # upper bound of eta
eta_lb = -0.0001                # lower bound of eta

eta = model.rvar(s)             # eta as random variables
uset = (eta.sum() == 0,
        eta >= eta_lb,
        eta <= eta_ub)
pi = 1/s + eta                  # pi as inexact probabilities

x = model.dvar(n)
u = model.dvar(s)
alpha = model.dvar()

model.minmax(alpha + 1/(1-beta) * (pi@u), uset)
model.st(u >= y@x - alpha)
model.st(u >= 0)
model.st(pi@y@x >= mu)
model.st(x >= x_lb, x <= x_ub, x.sum() == w0)

model.solve(msk)
```

```
Being solved by Mosek...
Solution status: optimal
Running time: 0.0295s
```

```python
x.get().round(4)    # the optimal portfolio decision with 4 d.p.
```

```
array([0.2605, 0.5601, 0.0651, 0.    , 0.1143])
```

#### Worst-case CVaR model with ellipsoidal uncertainty

In cases that \\(\Pi\\) is an ellipsoidal uncertainty set

$$
\Pi = \left\{\pmb{\pi}: \pmb{\pi} = \pmb{\pi}^0 + \rho\pmb{\eta}, \pmb{1}^{\top}\pmb{\eta}=0, \pmb{\pi}^0 + \rho\pmb{\eta} \geq \pmb{0}, \|\pmb{\eta}\| \leq 1 \right\},
$$

where the nominal probability \\(\pmb{\pi}^0\\) is the center of the ellipsoid, and the constant \\(\rho=0.001\\), then the model can be implemented by the code below.

```python
model = ro.Model()

rho = 0.001

eta = model.rvar(s)
uset = (eta.sum() == 0, 1/s + rho*eta >= 0,
        rso.norm(eta) <= 1)
pi = 1/s + rho*eta

x = model.dvar(n)
u = model.dvar(s)
alpha = model.dvar()

model.minmax(alpha + 1/(1-beta) * (pi@u), uset)
model.st(u >= y@x - alpha)
model.st(u >= 0)
model.st(pi@y@x >= mu)
model.st(x >= x_lb, x <= x_ub, x.sum() == w0)

model.solve(grb)
```

```
Being solved by Mosek...
Solution status: optimal
Running time: 0.0396s
```

```python
x.get().round(4)    # the optimal portfolio decision with 4 d.p.
```

```
array([0.1486, 0.6231, 0.0132, 0.    , 0.2151])
```

#### Worst-case CVaR with KL divergence
Here, we consider the KL divergence-constrained ambiguity of probabilities

$$
\Pi = \left\{\boldsymbol{\pi}: \sum_{k=1}^s\pi_k\log(\pi_k/\hat{\pi}_k) \leq \epsilon\right\}, 
$$

where \\(\hat{\pi}_k = 1/s\\) is the empirical probability of each sample. Assume that the constant \\(\epsilon=0.001\\), the code for implementing such a robust model is given below.

```python
from rsome.rsome import ro
from rsome.rsome import msk_solver as msk
import rsome.rsome as rso

model = ro.Model()

epsilon = 0.001

pi = model.rvar(s)
uset = (pi.sum() ==1, pi >= 0,
        rso.kldiv(pi, 1/s, epsilon))    # uncertainty set of pi

x = model.dvar(n)
u = model.dvar(s)
alpha = model.dvar()

model.minmax(alpha + 1/(1-beta) * (pi@u), uset)
model.st(u >= y@x - alpha)
model.st(u >= 0)
model.st(pi@y@x >= mu)
model.st(x >= x_lb, x <= x_ub, x.sum() == w0)

model.solve(msk)
```

```
Being solved by Mosek...
Solution status: optimal
Running time: 0.2003s
```

```python
x.get().round(4)    # the optimal portfolio decision with 4 d.p.
```

```
array([0.0904, 0.6185, 0.0446, 0.    , 0.2465])
```


In this example, we show that data acquisition tools provided in the Python ecosystem (<i>e.g.</i>, `pandas-datareader`) can be readily used to collect and feed real data into RSOME models.  Apart from acquiring data, rich machine learning tools in the Python ecosystem can also be used to develop data-driven optimization models. More such examples will be provided in introducing the `dro` module for modeling distributionally robust optimization problems.  

<br>
#### Reference

<a id="ref1"></a>

Zhu, Shushang, and Masao Fukushima. 2009. [Worst-case conditional value-at-risk with application to robust portfolio management](https://pubsonline.informs.org/doi/abs/10.1287/opre.1080.0684). <i>Operations Research</i> <b>57</b>(5) 1155-1168.