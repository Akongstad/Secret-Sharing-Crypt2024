
### Running the 

### **Shamir Secret Sharing**

Wiki source with example calculation: [Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing)

**The key is in polynomials.**

- 2 points to identify a line
- 3 points to identify a squared polynomial
- 4 points to identify a cubic polynomial

**Intuition:**

We need to choose a large enough polynomial. With n^2, we need 3 points. Then we can sample x points, e.g., 7 from the polynomial. Now any 3 of these people can decrypt the secret.

$(x_0, y_0), … (x_n, y_n)$ → secret box = P

Secret = P[0]

|sk| = n

The x’s can be picked deterministically. → Eg: 1,2,3,4,5,6 with secret on 0.

### Protocol

**Setup**:

Dealer → input ‘s’

Dealer → choose $a_1,a_2…a_t \in Z$

Dealer → sets $f(x) = S+a_1x + a_2x^2+…a_t x^y$

t points have infinite many polynomials t+1 points fixes the polynomial.

*(Dealer can choose the number of point n st n ≤ t+1 depending on the trust assumption on the party.)*

Party i → gets $f(x_i)$

**Reconstruction**:

party i →  receives $f(x_j) → ‘t’$ many 

party i → uses Lagrange interpolation to reconstruct f(x).

party i → read s from f(0)

## Lagrange Interpolation Algorithm

---

### Example 1

---

**Points**= [(-1,0)(0,1),(1,8)]

- 3 point fix a degree=2 polynomial
- Chose by the dealer and given to users.

Polynomial for points = $3x^2+4x+1$

$f \space st \space f(x_i)=y_i$, $deg(f)=2$

**Computation:**

$$
\delta_0(x)=\frac{(x-0)*(x-1)}{-1*-2} = \frac{x(x-1)}{2}
$$

$$
\delta_1(x)=\frac{(x-1)*(x+1)}{-1}=(1+x)*(1-x)
$$

$$
\delta_2(x)=\frac{(x--1)*(x-0)}{2}=\frac{x(x+1)}{2}
$$

$$
f(x)=\delta_0(x)y_0 + \delta_1(x)y_1 + \delta_2(x)y_2 =

\frac{x(x-1)}{2}(0)+(1+x)*(1-x)(1)+\frac{x*(x+1)}{2}(8)\\
=0+-1x^2+4x^2+4x\\
=3x^2+4x+1
$$

**Notes:**

- The shares will change, but the evaluation point will not. I.e., y’s change, but x's do not.
- xs only change if we add additional parties at which point we need to recompute the Lagrange interpolation.

### Formal Algorithm

---

**Algorithm**:

$$
f(x) = \sum_{j=0}^k{\delta_j(x)*y_j} \rarr \delta_0(x)y_0+ \delta_1(x)y_1+\delta_2(x)y_2
$$

**Note**: Once we have computed the Lagrange reconstruction once. We can reuse it for all $y_j’s$

$$
\delta_j(x)=\frac{(x-x_0)*(x-x_1)...(x-x_{j-1})*(x-x_{j+1})...(x-x_k)}

{(x_j-x_0)*(x_j-x_1)...(x_j-x_{j-1})*(x_j-x_{j+1})...(x_j-x_k)}
$$

$$
\delta_j(x) = \frac{\prod_{i+j}{x-x_i}}
{\prod_{i\ne j}x_j-x_i}
$$

**Example**:

**Points**= $[(x_0,y_0)(x_1,y_1),(x_2,y_2)]$

$$
\delta_0(x)=\frac{(x-x_1)*(x-x_2)}{(x_0-x_1)*(x_0-x_2)}
$$

$$
\delta_1(x)=\frac{(x-x_0)*(x-x_2)}{(x_1-x_0)*(x_1-x_2)}
$$

$$
\delta_2(x)=\frac{(x-x_0)*(x-x_1)}{(x_2-x_0)*(x_2-x_1)}
$$

$$
\delta_0(x_0)=1, \space \delta_0(x_1)=0, \space \delta_0(x_2)=0
$$

$$
\delta_1(x_0)=0, \space \delta_1(x_1)=1, \space \delta_1(x_2)=0
$$

$$
\delta_2(x_0)=0, \space \delta_2(x_1)=0, \space \delta_2(x_2)=1
$$

**Intuition**: At $\delta_j(x_j)$ both top and bottom are the same.. I.e., $\delta_j(x_j)=1$

We want to find $f(x_0) == y_0$

$\delta_j(x_i)$ is the polynomial.

**Additional context**:

**Q1.** What fixes the secret it not the x_i shares, but the function. IE y_i values.

x_i can be fixed IE: [1,2,3,4,5,6,7]

$\delta_i$ is fixed once the domain is fixed…
