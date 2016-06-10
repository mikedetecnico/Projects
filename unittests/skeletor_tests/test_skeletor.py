# standard library imports
from unittest import TestCase

# tools imports
from tools.maya.rigging.skeletor.skeletor import Skeletor, Skeleton


class SkeletorTests(TestCase):
    """ Tests the Skeletor class object.
    """

    def setUp(self):
        """ Setup for the test cases
        """

        self._skeletor = Skeletor("test")

    def test_build_skeletons(self):
        """ Test the building of skeletons in Mock situation
        """

        self._skeletor = Skeletor("test")

        # test that this is a skeleton object
        self.assertIsInstance(self._skeletor, Skeleton)

        # test the this raises a value error if not list is passed
        self.assertRaises(ValueError, Skeletor.build_skeletons, self._skeletor)

        self.assertEquals(Skeletor.build_skeletons([self._skeletor]), True)
