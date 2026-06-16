# Mathematics

> Linear algebra, calculus, optimisation, signal processing — the language MRI, statistics, and ML all share underneath.

A working neuroimager doesn't need to *prove* every theorem, but needs the vocabulary to read a methods paper and the intuition to spot when something looks wrong. This page gives the working depth.

## Linear algebra

Linear algebra is the load-bearing math of neuroimaging.

### Vectors, matrices, basics

A vector $v \in \mathbb{R}^n$; a matrix $A \in \mathbb{R}^{m \times n}$.

- **Dot product** — $\langle u, v \rangle = u^T v$.
- **Outer product** — $u v^T$, an $m\times n$ matrix.
- **Norms** — $\|v\|_2 = \sqrt{\sum v_i^2}$, $\|v\|_1 = \sum |v_i|$.
- **Orthogonality** — $u \perp v \iff u^T v = 0$.
- **Identity, transpose, inverse** — $A^{-1} A = I$ when $A$ is square and non-singular.

### Eigenvalues and eigenvectors

$$
A v = \lambda v
$$

Geometric meaning: directions $v$ along which $A$ acts as scaling by $\lambda$. PCA, spectral clustering, diffusion tensor estimation all hinge on this.

### Singular Value Decomposition (SVD)

Every real matrix factors as

$$
A = U \Sigma V^T
$$

with orthogonal $U, V$ and diagonal non-negative $\Sigma$. SVD generalises eigendecomposition to non-square matrices and underlies:

- **PCA** — the columns of $V$ are principal directions, the singular values $\sigma_i$ are the standard deviations along them.
- **Pseudoinverse** — $A^+ = V \Sigma^+ U^T$; gives least-squares solutions to overdetermined systems.
- **Low-rank approximation** — keep the top-$k$ singular values; the optimal rank-$k$ approximation in Frobenius / spectral norm (Eckart-Young theorem).

### Linear regression as linear algebra

$$
y = X\beta + \varepsilon, \qquad \hat\beta = (X^T X)^{-1} X^T y
$$

When $X^T X$ is ill-conditioned, regularise: ridge ($\beta = (X^TX + \lambda I)^{-1} X^T y$) or lasso (L1 penalty, non-closed form).

### Diffusion tensor as a 3×3 matrix

DTI fits a symmetric positive-definite tensor $D$ per voxel. Its three eigenvalues $\lambda_1 \ge \lambda_2 \ge \lambda_3$ summarise diffusion:

- **MD (mean diffusivity)** $= (\lambda_1 + \lambda_2 + \lambda_3)/3$.
- **FA (fractional anisotropy)** $= \sqrt{3/2}\,\|\lambda - \bar\lambda\|_2 / \|\lambda\|_2$.
- **Primary direction** $= v_1$, the eigenvector for $\lambda_1$.

Tractography integrates along this principal direction field.

## Calculus you actually use

### Derivatives — direction and rate of change

- **Gradient** $\nabla f$ — vector of partial derivatives; points in the direction of steepest ascent.
- **Hessian** $H$ — matrix of second partials; tells you curvature.

In ML, training = "step downhill on the loss". The gradient tells you which way; the learning rate scales how far. SGD, Adam, momentum are variations on this.

### Chain rule and backprop

For a composition $L = f(g(x))$, $\frac{dL}{dx} = f'(g(x)) g'(x)$. Backpropagation is this rule applied to a computational graph.

### Integrals — accumulation

A definite integral $\int_a^b f(x)\,dx$ is the signed area under $f$. In imaging:

- Smoothing = convolution with a kernel = integral.
- Probability totals = $\int p(x)\,dx = 1$.
- The BOLD HRF is a parametric integral over a hemodynamic impulse response.

### Multivariable calculus and the Jacobian

For a vector field $F: \mathbb{R}^n \to \mathbb{R}^m$, the Jacobian $J_{ij} = \partial F_i / \partial x_j$. The Jacobian's determinant tells you local volume change. **Voxel-based morphometry** uses the log-Jacobian of the warp to MNI space as a per-voxel "expansion" map.

## Optimisation

Most of statistics, ML, and image registration is "find $x$ minimising $f(x)$".

### Convex vs non-convex

- **Convex** functions have one global minimum; gradient descent works.
- **Non-convex** (most neural networks) have many local minima; SGD often finds good ones anyway. Why is an active research question.

### First-order methods (the workhorses)

- **Gradient descent** — $x \leftarrow x - \eta \nabla f(x)$.
- **Stochastic GD (SGD)** — gradient on a minibatch; cheaper, noisier.
- **Momentum** — accumulates a running gradient direction.
- **Adam / RMSProp** — adaptive per-parameter learning rates.

### Second-order methods

- **Newton's method** — uses the Hessian; super-fast convergence near a minimum, expensive.
- **L-BFGS** — limited-memory quasi-Newton; the workhorse for medium-scale optimisation (image registration, MLE fits).

## Signal processing

The BOLD timeseries, the DWI gradient train, the EPI readout — all are signals.

### Convolution and filtering

Convolution $h * x$ is a sliding inner product. A linear time-invariant filter is fully characterised by its impulse response $h$. Examples:

- Spatial smoothing = convolution with a Gaussian kernel.
- The hemodynamic response function (HRF) = convolution of stimulus train with HRF kernel.
- An FIR low-pass filter removes high frequencies via a tap-delay structure.

### Fourier transform — the bridge to k-space

The discrete Fourier transform (DFT) decomposes a signal into sinusoidal components:

$$
X[k] = \sum_{n=0}^{N-1} x[n] \, e^{-j 2 \pi k n / N}
$$

For MRI this is *physical*: the scanner samples k-space (spatial frequency domain) and the inverse DFT reconstructs the image:

$$
\text{image}(x, y) = \mathcal{F}^{-1}\{S(k_x, k_y)\}
$$

EPI fast imaging fills k-space in a single zigzag readout; spiral imaging uses spiral trajectories. Distortion happens because off-resonance shifts a fraction of $k$-space along the phase-encode direction. See [Fundamentals → MRI sequences → EPI](../sequences/epi.md).

### Sampling theorem (Nyquist)

To represent a band-limited signal of max frequency $f_{\max}$, sample at $\ge 2 f_{\max}$. Below that, **aliasing** wraps high frequencies into low ones. In fMRI, TR sets the temporal Nyquist (TR = 2 s → 0.25 Hz Nyquist), which is *under* the cardiac frequency (~1 Hz) — physiological noise aliases into your data.

### Power spectral density

$$
S_{xx}(f) = |X(f)|^2
$$

Useful for finding periodic structure (cardiac, respiratory artefact in fMRI; alpha rhythm in EEG).

## Geometry of the brain

### Manifolds and surfaces

The cortex is a 2D manifold embedded in 3D. Tools like FreeSurfer and HCP work with triangle meshes (vertices + edges + triangles). Surface-based analysis ([Analysis → Surface-based](../../analysis/surface.md)) respects geodesic distance on this mesh, not Euclidean distance through tissue.

### Diffeomorphisms — smooth invertible warps

Image registration finds a diffeomorphism $\phi: \mathbb{R}^3 \to \mathbb{R}^3$ that aligns one image to another. SyN (Symmetric Normalization), the algorithm behind ANTs, parametrises $\phi$ as a time-integrated velocity field.

### Riemannian geometry on tensors and connectomes

DTI tensors and functional connectomes live on the manifold of symmetric positive-definite matrices. Standard Euclidean metrics misbehave; affine-invariant and log-Euclidean metrics (Arsigny et al., 2007) are the principled choice for averaging and statistics.

## Information theory snippets

- **Entropy** $H(X) = -\sum p(x) \log p(x)$ — uncertainty of a distribution.
- **KL divergence** $D_{KL}(p \| q)$ — directional dissimilarity between distributions. Underlies variational inference, model evaluation.
- **Mutual information** $I(X; Y) = D_{KL}(p(x,y) \| p(x)p(y))$ — non-linear dependence. Used as a registration similarity metric ([Mattes et al., 2003](https://doi.org/10.1117/12.481048)).

## References

1. **Strang G.** *Introduction to Linear Algebra.* 6th ed. Wellesley-Cambridge Press; 2023. ISBN 978-1733146678.
2. **Trefethen LN, Bau D III.** *Numerical Linear Algebra.* SIAM; 1997. ISBN 978-0898713619.
3. **Boyd S, Vandenberghe L.** *Convex Optimization.* Cambridge University Press; 2004. ISBN 978-0521833783. Free online: [https://web.stanford.edu/~boyd/cvxbook/](https://web.stanford.edu/~boyd/cvxbook/)
4. **Oppenheim AV, Schafer RW.** *Discrete-Time Signal Processing.* 3rd ed. Pearson; 2009. ISBN 978-0131988422.
5. **Bracewell RN.** *The Fourier Transform and Its Applications.* 3rd ed. McGraw-Hill; 2000. ISBN 978-0073039381.
6. **Nocedal J, Wright SJ.** *Numerical Optimization.* 2nd ed. Springer; 2006. ISBN 978-0387303031.
7. **Bishop CM.** *Pattern Recognition and Machine Learning.* Springer; 2006. ISBN 978-0387310732.
8. **Arsigny V, Fillard P, Pennec X, Ayache N.** Geometric means in a novel vector space structure on symmetric positive-definite matrices. *SIAM J Matrix Anal Appl.* 2007;29(1):328-347. [doi:10.1137/050637996](https://doi.org/10.1137/050637996)
9. **Avants BB, Epstein CL, Grossman M, Gee JC.** Symmetric diffeomorphic image registration with cross-correlation: evaluating automated labeling of elderly and neurodegenerative brain. *Med Image Anal.* 2008;12(1):26-41. [doi:10.1016/j.media.2007.06.004](https://doi.org/10.1016/j.media.2007.06.004) — SyN.

## Where to next

[Physics](physics.md) — the MR physics that produces the signals all this math operates on.
