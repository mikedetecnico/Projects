__author__ = "Michael Graessle"
__copyright__ = "Copyright 2017"

__all__ = ["ExporterUI"]

# standard library imports
import sys

# PySide imports
from PySide2 import QtWidgets
import shiboken2

# Maya imports
import maya.OpenMayaUI as mui


def get_maya_window():
    """ Get the main Maya window as a Qt instance.
    """
    ptr = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(ptr), QtWidgets.QDialog)


class ExporterUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """ Constructor.
        """
        super(ExporterUI, self).__init__(parent=parent)

        self.setWindowTitle("Fbx Exporter")
        self.setFixedSize(400, 200)

        self.main_layout = QtWidgets.QVBoxLayout()

        self.input_path = None

        self.output_path = None

        self.setup_ui()

    def setup_ui(self):
        """ Setup the layout of the UI.
        """

        self.setup_input_layout()

        self.setup_output_layout()

        self.setup_buttons()

        self.setLayout(self.main_layout)

    def setup_input_layout(self):
        """ Setup the layout for the input folder information.
        """

        input_layout = QtWidgets.QHBoxLayout()

        input_folder_label = QtWidgets.QLabel("Source Folder:")

        input_layout.addWidget(input_folder_label)

        self.input_path = QtWidgets.QLineEdit()

        input_layout.addWidget(self.input_path)

        self.main_layout.addLayout(input_layout)

    def setup_output_layout(self):
        """ Setup the layout for the output folder information.
        """

        output_layout = QtWidgets.QHBoxLayout()

        output_folder_label = QtWidgets.QLabel("Output Folder:")

        output_layout.addWidget(output_folder_label)

        self.output_path = QtWidgets.QLineEdit()

        output_layout.addWidget(self.output_path)

        self.main_layout.addLayout(output_layout)

    def setup_buttons(self):
        """ Setup the buttons for running the export process and canceling the process.
        """

        button_layout = QtWidgets.QHBoxLayout()

        ok_button = QtWidgets.QCommandLinkButton("OK")

        ok_button.setFixedHeight(60)

        ok_button.clicked.connect(self.on_export)

        button_layout.addWidget(ok_button)

        cancel_button = QtWidgets.QCommandLinkButton("Cancel")

        cancel_button.setFixedHeight(60)

        cancel_button.clicked.connect(self.close)

        button_layout.addWidget(cancel_button)

        self.main_layout.addLayout(button_layout)

    def on_export(self):
        """ Run the export process.
        """
        pass


def main(standalone=False):
    if not standalone:
        ui = ExporterUI(get_maya_window())
    else:
        ui = ExporterUI()

    ui.show()
    return ui

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_ui = main(True)
    sys.exit(app.exec_())
