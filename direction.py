import random


class Direction:
    """
    Define a direction for possible excitations.
    """
    all_directions = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))

    @classmethod
    def random(cls, choices=all_directions):
        """Pick a random direction from allowed directions."""

        return random.choice(choices)
