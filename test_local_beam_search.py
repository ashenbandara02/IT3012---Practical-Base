import random
import unittest
from unittest.mock import patch

from local_beam_search import local_beam_search


class LocalBeamSearchTests(unittest.TestCase):
    def test_pooled_selection_can_keep_two_successors_of_one_parent(self):
        # Both best successors come from state 10, so independent searches
        # or selecting one successor per parent would produce a different result.
        offsets = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] + [0] * 10
        evaluated = []

        def objective(state):
            evaluated.append(state)
            return state

        with patch('local_beam_search.random.uniform', side_effect=offsets):
            result = local_beam_search([0, 10], 2, 2, objective)
        self.assertEqual(result, 20)
        self.assertEqual(evaluated[10:20], [20] * 5 + [19] * 5)

    def test_seeded_parabola(self):
        random.seed(42)
        result = local_beam_search([0, 25, 100], 3, 100,
                                   lambda x: -(x - 50) ** 2 + 100)
        self.assertLess(abs(result - 50), 2)


if __name__ == '__main__':
    unittest.main()
