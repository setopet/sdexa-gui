from unittest import TestCase
from backend import Projection
from tests.helpers import *


class RegistrationTest(TestCase):
    def test_registration(self):
        file = get_txt_from_array(ones)
        image = Projection(file)
        image.register_on_image(zeros, 16)
        self.assertEqual(image.registration.shape, standard_shape)
