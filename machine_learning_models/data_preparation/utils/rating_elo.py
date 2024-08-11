import numpy as np

# Elo update function


def update_elo(rating1, rating2, result):
    if rating1 > 2400:
        k1 = 16
    elif rating1 > 2100:
        k1 = 24
    else:
        k1 = 32

    if rating2 > 2400:
        k2 = 16
    elif rating2 > 2100:
        k2 = 24
    else:
        k2 = 32

    transformed_rating1 = 10 ** (rating1 / 400)
    transformed_rating2 = 10 ** (rating2 / 400)

    expected_outcome1 = transformed_rating1 / \
        (transformed_rating1 + transformed_rating2)
    expected_outcome2 = transformed_rating2 / \
        (transformed_rating1 + transformed_rating2)

    new_rating1 = rating1 + k1 * (result - expected_outcome1)
    new_rating2 = rating2 + k2 * ((1 - result) - expected_outcome2)

    return int(new_rating1), int(new_rating2)
