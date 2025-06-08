from jax.scipy.stats import norm as jnorm
import jax.numpy as jnp
from jax import grad

def black_scholes(S, K, T, r, sigma, q=0.0, otype="call"):

    d1 = (jnp.log(S/K) + ((r - q + ((jnp.square(sigma))/2))*(T)))/((sigma)*(jnp.sqrt(T)))
    d2 = d1 - ((sigma) * (jnp.sqrt(T)))

    if otype == "call":
        call = S * jnp.exp(-q * T) * jnorm.cdf(d1, 0, 1) - K * jnp.exp(-r * T) * jnorm.cdf(d2, 0, 1)
        return call
    else:
        put = K * jnp.exp(-r * T) * jnorm.cdf(-d2, 0, 1) - S * jnp.exp(-q * T) * jnorm.cdf(d1, 0, 1)
        return put

def loss(S, K, T, r, sigma_guess, price, q, otype="call"):
    theoretical_price = black_scholes(S, K, T, r, sigma_guess, q, otype="call")
    print(theoretical_price)
    market_price = price

    return theoretical_price - market_price

loss_grad = grad(loss, argnums=4)


def solve_for_iv(S, K, T, r, price, sigma_guess, q, otype="call", N_iter = 20, epsilon = .001, verbose = False):
    sigma = sigma_guess

    for i in range(N_iter):

        loss_val = loss(S, K, T, r, sigma, price, q, otype)

        if verbose:
            print("Current Error in theoretical vs market price:")
            print(loss_val)
        
        if abs(loss_val) < epsilon:
            break
        else:
            loss_grad_val = loss_grad(S, K, T, r, sigma, price, q, otype)
            print(loss_grad_val)
            sigma = sigma - loss_val / loss_grad_val
            print(sigma)

    
    return sigma


def main():
    S = 100.0
    K = 110.0
    T = 1.0
    r = 0.05
    sigma = 0.2
    q = 0
    otype = "call"

    x = black_scholes(S, K, T, r, 0.2, q, otype="call")
    calculate_implied_volatility = solve_for_iv(S, K, T, r, x)
    print(calculate_implied_volatility)

if __name__ == "__main__":
    main()