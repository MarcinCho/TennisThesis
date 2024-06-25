from math import sqrt, log, pi
# Glicko system version 1 not version 2 does not include volatility
# Glicko system constants
SCALE_FACTOR = 400
C = sqrt((350**2 - 50**2) / 365)


def g(RD):
    """Calculate the impact factor of a game result."""
    q = log(10) / SCALE_FACTOR  # ln(10) / 400
    return 1 / sqrt(1 + 3 * q**2 * RD**2 / pi**2)


def E(rating, opponent_rating, opponent_RD):
    """Calculate the expected outcome of a game."""
    return 1 / (1 + 10**(-g(opponent_RD) * (rating - opponent_rating) / SCALE_FACTOR))


def update_glicko(rating, RD, opponent_rating, opponent_RD, outcome):
    """Update the Glicko rating and RD based on a game outcome."""
    q = log(10) / SCALE_FACTOR  # ln(10) / 400
    g_RD = g(opponent_RD)
    E_rating = E(rating, opponent_rating, opponent_RD)

    d_square = 1 / (q**2 * g_RD**2 * E_rating * (1 - E_rating)
                    ) if (q**2 * g_RD**2 * E_rating * (1 - E_rating)) != 0 else 0

    new_rating = rating + q / \
        (1 / (RD**2) + 1 / d_square) * g_RD * (outcome - E_rating)
    new_RD = sqrt(1 / (1 / (RD**2) + 1 / d_square))

    return new_rating, new_RD
