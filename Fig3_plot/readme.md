
# Fig3_plot
This folder contains the Materials required for piecewise linear fit, and that for reproducing figure 3 in our manuscript.

## 1. piecewise linear fiting

#### 1.1 code
- PiecewiseLinearFit.m: Matlab codes for piecewise linear fit; This code has a dependency on `parfor_progressbar.m` released by [Daniel Terry](https://ww2.mathworks.cn/matlabcentral/fileexchange/53773-parfor_progressbar), for displaying a graphical progress bar during execution.
 
- Pvalue.py: python codes (based on [piecewise-regression](https://github.com/chasmani/piecewise-regression) package) for Davies' significance level test:
  <pre><code>Davies, R. B. Hypothesis testing when a nuisance parameter is present only under the alternative. Biometrika, 74(1), 33-43 (1987)</code></pre>
  The change was considered statistically significant when p-value < 0.05.

#### 1.2 workflow
- Download example data: [InSAR-derived RLLS time series and velocity for Houston](https://drive.google.com/file/d/1376MdRwcObZUmJIERmbbKt5uXZDObeoO/view?usp=sharing), and unzipped the downloaded file to path `./Houston`
- Run `piecewiseLinearFit.m` to perfom piecewise linear fitting
- Run `Pvalue.py` to perfom significance level test
- The trend of deceleration/acceleration can be derived from the piecewise linear fitting results.

## 2. plot figures
We have provided data and codes to plot figure3 already. 
Steps for reproducing figure 3 in our manuscript:
- Unzip `../Regional_boundary.zip`
- Run `Fig3_ab_plot.py` to generate figure 3(a) and 3(b)
- Run `Fig3_c_plot.m` in matlab software to generate figure 3(c)
