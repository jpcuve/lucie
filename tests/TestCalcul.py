from unittest import TestCase

import numpy as np

from lucie.calcul import multiplication


class TestCalcul(TestCase):

    def test_multiplication(self):
        self.assertListEqual(list(np.array([2.0, 4.0, 6.0])), list(multiplication(np.array([1.0, 2.0, 3.0]), 2.0)))
