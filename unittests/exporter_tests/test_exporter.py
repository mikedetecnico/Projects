# standard library imports
from unittest import TestCase

# tools imports
from tools.maya.exporter.exporter import Exporter


class ExporterTests(TestCase):
    def test_export_fbx(self):
        """ Test exporting a basic FBX file.
        :return:
        """
        Exporter.export_fbx(r'C:\temp\test.fbx')
