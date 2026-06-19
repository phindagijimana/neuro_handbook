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

The cortex is a 2D manifold embedded in 3D. Tools like FreeSurfer and HCP work with triangle meshes (vertices + edges + triangles). Surface-based analysis ([Neuroimaging Analysis → Surface-based](../../analysis/surface.md)) respects geodesic distance on this mesh, not Euclidean distance through tissue.

### Diffeomorphisms — smooth invertible warps

Image registration finds a diffeomorphism $\phi: \mathbb{R}^3 \to \mathbb{R}^3$ that aligns one image to another. SyN (Symmetric Normalization), the algorithm behind ANTs, parametrises $\phi$ as a time-integrated velocity field.

### Riemannian geometry on tensors and connectomes

DTI tensors and functional connectomes live on the manifold of symmetric positive-definite matrices. Standard Euclidean metrics misbehave; affine-invariant and log-Euclidean metrics (Arsigny et al., 2007) are the principled choice for averaging and statistics.

## Mathematics for neuroimaging AI

Modern neuroimaging ML stretches the math layer in specific directions.

### Backprop, automatic differentiation

Deep networks parametrise a function $f_\theta(x)$; training minimises a loss $L$ via gradient descent on $\theta$. Backprop is the chain rule applied to the **computational graph**: at every node, the framework caches the forward value and the local Jacobian; the backward pass multiplies them.

For a layer $z = Wx + b$, the gradients are:

$$
\frac{\partial L}{\partial W} = \frac{\partial L}{\partial z}\, x^T, \qquad
\frac{\partial L}{\partial x} = W^T\, \frac{\partial L}{\partial z}
$$

PyTorch / JAX implement this as **reverse-mode AD**; you almost never write the gradients yourself.

### Convolutions in 2D / 3D

A 3D convolution layer with kernel $K \in \mathbb{R}^{c_{out} \times c_{in} \times k \times k \times k}$ acts on a volume $X$ as:

$$
Y[o, x, y, z] = \sum_{c} \sum_{i,j,k} K[o, c, i, j, k] \cdot X[c, x+i, y+j, z+k]
$$

Cost: $O(c_{in} c_{out} k^3 \cdot H W D)$. This is why 3D U-Nets are memory-hungry; gradient checkpointing and mixed precision are essential.

### Self-attention — the modern primitive

Given query / key / value matrices $Q, K, V \in \mathbb{R}^{n \times d}$:

$$
\text{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^T}{\sqrt{d}}\right) V
$$

Cost $O(n^2 d)$ — quadratic in sequence length $n$. For a 256³ volume tokenised into 16³ patches, $n=4096$, $n^2 = 1.7 \times 10^7$, manageable on an A100. For voxel-level attention, use windowed (Swin), linear (Performer), or memory-efficient (FlashAttention) variants.

### Diffusion models

Score-based diffusion ([Ho et al., 2020](https://doi.org/10.48550/arXiv.2006.11239)) trains a network $\varepsilon_\theta(x_t, t)$ to predict noise from a noisy image; sampling iteratively denoises from Gaussian. The forward process:

$$
q(x_t \mid x_0) = \mathcal{N}\!\left(\sqrt{\bar\alpha_t}\,x_0,\, (1 - \bar\alpha_t) I\right)
$$

Loss is simply:

$$
L = \mathbb{E}_{x_0, t, \varepsilon} \left[ \| \varepsilon - \varepsilon_\theta(x_t, t) \|^2 \right]
$$

In neuroimaging: image generation, super-resolution, unconditional sampling, inverse-problem MRI reconstruction.

### Geometric deep learning on surfaces and graphs

The cortex is a graph (mesh) and the connectome is a graph; standard CNNs assume a Euclidean grid. **Graph convolutional networks** (GCN, GAT) operate on adjacency matrices:

$$
H^{(\ell+1)} = \sigma\!\left( \tilde D^{-\frac{1}{2}} \tilde A \tilde D^{-\frac{1}{2}} H^{(\ell)} W^{(\ell)} \right)
$$

where $\tilde A = A + I$ is the adjacency + self-loops and $\tilde D$ is its degree matrix.

For mesh CNNs ([MoNet, MeshCNN, SphericalCNN](https://geometricdeeplearning.com)), the analogous operation generalises convolution to non-Euclidean domains. **Equivariance** to rotations / surface diffeomorphisms is the active research direction.

### Variational autoencoders — generative + representation

VAEs ([Kingma & Welling, 2014](https://doi.org/10.48550/arXiv.1312.6114)) optimise the **evidence lower bound (ELBO)**:

$$
\log p(x) \ge \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{\mathrm{KL}}\!\left(q_\phi(z|x) \,\|\, p(z)\right)
$$

The encoder $q_\phi$ produces a Gaussian latent; the decoder $p_\theta$ reconstructs. Used in neuroimaging for anomaly detection, normative modelling, harmonisation.

### Normative modelling

Treats brain measurements as a function of age, sex, site:

$$
y_i = f(\text{age}_i, \text{sex}_i, \text{site}_i) + \varepsilon_i
$$

estimated as a Gaussian-process or Bayesian-neural-network regression ([Marquand et al., 2016](https://doi.org/10.1016/j.biopsych.2015.12.023)). Each subject's deviation from the cohort norm becomes a per-region z-score. Strong framework for psychiatric heterogeneity.

## Information theory snippets

- **Entropy** $H(X) = -\sum p(x) \log p(x)$ — uncertainty of a distribution.
- **KL divergence** $D_{KL}(p \| q)$ — directional dissimilarity between distributions. Underlies variational inference, model evaluation.
- **Mutual information** $I(X; Y) = D_{KL}(p(x,y) \| p(x)p(y))$ — non-linear dependence. Used as a registration similarity metric ([Mattes et al., 2003](https://doi.org/10.1117/12.481048)).

## Exercises

1. **SVD low-rank approximation.** Generate a 100×50 matrix with rank ~5 plus noise. Reconstruct from the top 5 singular values; report Frobenius error.
2. **Gradient check.** For `f(x) = ||Ax - b||²`, derive the gradient analytically and verify numerically via finite differences.
3. **Mutual information.** Estimate MI between two N(0,1) variables with correlation 0.5; compare against the analytic answer `-0.5 * log(1 - ρ²)`.

??? success "Solutions"
    1. `U,S,Vt = np.linalg.svd(A,full_matrices=False); A5 = U[:,:5] @ np.diag(S[:5]) @ Vt[:5]; np.linalg.norm(A - A5,'fro')`.
    2. `∇f = 2A^T(Ax - b)`; FD: `(f(x+ε e_i) - f(x-ε e_i)) / (2ε)` for each i.
    3. MI ≈ 0.144 nats; verify with `from sklearn.feature_selection import mutual_info_regression`.

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
10. **Goodfellow I, Bengio Y, Courville A.** *Deep Learning.* MIT Press; 2016. ISBN 978-0262035613. Free online: [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/)
11. **Vaswani A, Shazeer N, Parmar N, et al.** Attention is all you need. *NeurIPS.* 2017. [arXiv:1706.03762](https://doi.org/10.48550/arXiv.1706.03762)
12. **Ho J, Jain A, Abbeel P.** Denoising diffusion probabilistic models. *NeurIPS.* 2020. [arXiv:2006.11239](https://doi.org/10.48550/arXiv.2006.11239)
13. **Kingma DP, Welling M.** Auto-encoding variational Bayes. *ICLR.* 2014. [arXiv:1312.6114](https://doi.org/10.48550/arXiv.1312.6114)
14. **Bronstein MM, Bruna J, Cohen T, Veličković P.** Geometric deep learning: grids, groups, graphs, geodesics, and gauges. *arXiv.* 2021. [arXiv:2104.13478](https://doi.org/10.48550/arXiv.2104.13478)
15. **Marquand AF, Rezek I, Buitelaar J, Beckmann CF.** Understanding heterogeneity in clinical cohorts using normative models: beyond case-control studies. *Biol Psychiatry.* 2016;80(7):552-561. [doi:10.1016/j.biopsych.2015.12.023](https://doi.org/10.1016/j.biopsych.2015.12.023)
16. **Dao T, Fu DY, Ermon S, et al.** FlashAttention: fast and memory-efficient exact attention with IO-awareness. *NeurIPS.* 2022. [arXiv:2205.14135](https://doi.org/10.48550/arXiv.2205.14135)

## Where to next

[Physics](physics.md) — the MR physics that produces the signals all this math operates on.
