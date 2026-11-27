import numpy as np
from scipy.optimize import minimize

TRADING_DAYS = 252
MAX_ALLOCATION = 0.50   # Max 50% allocation per asset
MIN_ALLOCATION = 0.05   # Min 5% allocation per asset


def optimize_portfolio(data, risk_tolerance):
    """
    Mean-variance (Modern Portfolio Theory) optimisation along the efficient frontier.

    The risk tolerance picks a point between the lowest-volatility portfolio
    (risk_tolerance = 0) and the highest-return portfolio (risk_tolerance = 1)
    that is possible under the allocation limits. The returned weights give the
    highest expected return for that level of volatility.

    Args:
        data (pandas.DataFrame): DataFrame containing historical stock prices.
        risk_tolerance (float): Risk tolerance between 0 and 1 (higher means more risk).

    Returns:
        dict: Optimised asset weights, or None if the optimisation fails.
    """
    try:
        risk_tolerance = min(max(float(risk_tolerance), 0.0), 1.0)

        # Annualised returns & covariance matrix
        returns = data.pct_change().dropna()
        mean_returns = returns.mean().values * TRADING_DAYS
        cov_matrix = returns.cov().values * TRADING_DAYS

        num_assets = len(mean_returns)
        if num_assets < 2:
            print("Error optimising portfolio: at least 2 assets are needed.")
            return None

        # Bounds: per-asset limits (the lower limit is relaxed if there are many assets)
        lower = min(MIN_ALLOCATION, 1 / num_assets)
        bounds = tuple((lower, MAX_ALLOCATION) for _ in range(num_assets))
        weights_sum_to_one = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
        initial_weights = np.full(num_assets, 1 / num_assets)

        def portfolio_return(w):
            return float(np.dot(mean_returns, w))

        def portfolio_variance(w):
            return float(np.dot(w, np.dot(cov_matrix, w)))

        def solve(objective, constraints, x0):
            result = minimize(
                objective, x0, method="SLSQP",
                bounds=bounds, constraints=constraints,
            )
            if not result.success:
                raise ValueError(f"optimiser did not converge: {result.message}")
            return result.x

        # Lowest-risk portfolio (risk tolerance = 0)
        min_var_weights = solve(portfolio_variance, [weights_sum_to_one], initial_weights)
        min_vol = np.sqrt(portfolio_variance(min_var_weights))

        # Highest-return portfolio (risk tolerance = 1)
        max_ret_weights = solve(lambda w: -portfolio_return(w), [weights_sum_to_one], initial_weights)
        max_vol = np.sqrt(portfolio_variance(max_ret_weights))

        # Target volatility chosen by the risk tolerance
        target_vol = min_vol + risk_tolerance * (max_vol - min_vol)
        target_variance = target_vol ** 2 + 1e-10  # tiny tolerance for numerical stability

        # Best expected return that stays within the target volatility
        constraints = [
            weights_sum_to_one,
            {"type": "ineq", "fun": lambda w: target_variance - portfolio_variance(w)},
        ]
        optimal_weights = solve(lambda w: -portfolio_return(w), constraints, min_var_weights)

        return dict(zip(data.columns, optimal_weights))

    except Exception as e:
        print(f"Error optimising portfolio: {e}")
        return None
