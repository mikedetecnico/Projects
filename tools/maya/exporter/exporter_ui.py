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

# internal imports
from exporter import *


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

        self.progress_bar = QtWidgets.QProgressBar()

        self.setup_ui()

    def setup_ui(self):
        """ Setup the layout of the UI.
        """

        self.setup_input_layout()

        self.setup_output_layout()

        self.setup_buttons()

        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        self.main_layout.addWidget(self.progress_bar)

        self.setLayout(self.main_layout)

    def setup_input_layout(self):
        """ Setup the layout for the input folder information.
        """

        input_layout = QtWidgets.QHBoxLayout()

        input_folder_label = QtWidgets.QLabel("Source Folder:")

        input_layout.addWidget(input_folder_label)

        self.input_path = QtWidgets.QLineEdit()

        input_layout.addWidget(self.input_path)

        select_input_btn = QtWidgets.QToolButton()
        select_input_btn.setText("...")
        select_input_btn.clicked.connect(self.set_input_path)

        input_layout.addWidget(select_input_btn)

        self.main_layout.addLayout(input_layout)

    def setup_output_layout(self):
        """ Setup the layout for the output folder information.
        """

        output_layout = QtWidgets.QHBoxLayout()

        output_folder_label = QtWidgets.QLabel("Output Folder:")

        output_layout.addWidget(output_folder_label)

        self.output_path = QtWidgets.QLineEdit()

        output_layout.addWidget(self.output_path)

        select_output_btn = QtWidgets.QToolButton()
        select_output_btn.setText("...")
        select_output_btn.clicked.connect(self.set_output_path)

        output_layout.addWidget(select_output_btn)

        self.main_layout.addLayout(output_layout)

    def setup_buttons(self):
        """ Setup the buttons for running the export process and canceling the process.
        """

        button_layout = QtWidgets.QHBoxLayout()

        ok_button = QtWidgets.QCommandLinkButton("OK")

        ok_button.setFixedHeight(50)

        ok_button.clicked.connect(self.on_export)

        button_layout.addWidget(ok_button)

        cancel_button = QtWidgets.QCommandLinkButton("Cancel")

        cancel_button.setFixedHeight(50)

        cancel_button.clicked.connect(self.close)

        button_layout.addWidget(cancel_button)

        self.main_layout.addLayout(button_layout)

    def set_output_path(self):
        """ Set the output path based on the user choosing the directory.
        """
        self.output_path.setText(QtWidgets.QFileDialog.getExistingDirectory())

    def set_input_path(self):
        """ Set the output path based on the user choosing the directory.
        """
        self.input_path.setText(QtWidgets.QFileDialog.getExistingDirectory())

    def on_export(self):
        """ Run the export process.
        """
        output_directory = self.output_path.text()

        input_directory = self.input_path.text()

        self.progress_bar.setVisible(True)

        for progress in Exporter.batch_export_fbx(input_directory, output_directory):
            self.progress_bar.setValue(progress)

        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)


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
