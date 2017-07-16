__author__ = "Michael Graessle"
__copyright__ = "Copyright 2017"

# PySide imports
from PySide2.QtWidgets import *
from PySide2 import QtCore
import shiboken2

# Maya imports
import pymel.core as pm
import maya.OpenMayaUI as mui


def get_maya_window():
    """ Get the main Maya window as a Qt instance.
    """
    ptr = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(ptr), QDialog)


class DoubleSlider(QSlider):
    def __init__(self):
        super(DoubleSlider, self).__init__()
        self.decimals = 5
        self._max_int = 10 ** self.decimals

        super(DoubleSlider, self).setMinimum(0)
        super(DoubleSlider, self).setMaximum(self._max_int)

        super(DoubleSlider, self).setOrientation(QtCore.Qt.Horizontal)

        self._min_value = 0.0
        self._max_value = 1.0

    @property
    def _value_range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super(DoubleSlider, self).value()) / self._max_int * self._value_range + self._min_value

    def setValue(self, value):
        super(DoubleSlider, self).setValue(int((value - self._min_value) / self._value_range * self._max_int))

    def setMinimum(self, value):
        if value > self._max_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._min_value = value
        self.setValue(self.value())

    def setMaximum(self, value):
        if value < self._min_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._max_value = value
        self.setValue(self.value())

    def minimum(self):
        return self._min_value

    def maximum(self):
        return self._max_value


class UVRampToolUI(QDialog):
    def __init__(self, parent=None):
        """ Constructor.
        """
        super(UVRampToolUI, self).__init__(parent=parent)

        self.setWindowTitle("UV Ramp Tool")
        self.setFixedSize(400, 200)

        self.main_layout = QVBoxLayout()

        self.u_direction_radio = None

        self.v_direction_radio = None

        self.direction_offset = None

        self.direction_offset_slider_label = None

        self.setup_ui()

    def setup_ui(self):
        """ Setup the layout of the UI.
        """

        direction_layout = QHBoxLayout()

        self.u_direction_radio = QRadioButton("U Direction")

        direction_layout.addWidget(self.u_direction_radio)

        self.v_direction_radio = QRadioButton("V Direction")

        self.v_direction_radio.setChecked(True)

        direction_layout.addWidget(self.v_direction_radio)

        self.main_layout.addLayout(direction_layout)

        direction_offset_layout = QHBoxLayout()

        direction_offset_label = QLabel("Direction Offset")

        direction_offset_layout.addWidget(direction_offset_label)

        self.direction_offset = DoubleSlider()
        self.direction_offset.setMinimum(0)
        self.direction_offset.setMaximum(1)

        self.direction_offset.valueChanged.connect(self.on_slider_value_changed)

        direction_offset_layout.addWidget(self.direction_offset)

        self.direction_offset_slider_label = QLabel(str(self.direction_offset.value()))

        direction_offset_layout.addWidget(self.direction_offset_slider_label)

        self.main_layout.addLayout(direction_offset_layout)

        button_layout = QHBoxLayout()

        run_button = QCommandLinkButton("Run")

        run_button.setFixedHeight(50)

        run_button.clicked.connect(self.on_run)

        button_layout.addWidget(run_button)

        cancel_button = QCommandLinkButton("Cancel")

        cancel_button.setFixedHeight(50)

        cancel_button.clicked.connect(self.close)

        button_layout.addWidget(cancel_button)

        self.main_layout.addLayout(button_layout)

        self.setLayout(self.main_layout)

    def on_slider_value_changed(self):
        """ Run when the value of the slider has changed.
        """
        value = str(self.direction_offset.value())

        clamp_value = "%.1f" % (self.direction_offset.value(),)

        self.direction_offset.setValue(float(clamp_value))

        self.direction_offset_slider_label.setText(str(clamp_value))

    def on_run(self):
        """ Lays out the UVs based on the order of selection.
        """

        selectedMeshes = pm.ls(sl=True)

        pm.select(clear=True)

        for i, selTransform in enumerate(selectedMeshes):
            selMesh = selTransform.getShape()

            for vtx in selMesh.vtx:
                pm.select(vtx, r=True)

                pm.polyEditUV(pivotU=0.5, pivotV=0.5, scaleU=-0.1, scaleV=-0.1)

                newU = -0.45
                newV = -0.45

                pm.polyEditUV(relative=True, uValue=newU, vValue=newV)

                offset = 0.00

                try:
                    offset = self.direction_offset.value()
                except:
                    pass

                print offset

                if self.u_direction_radio.isChecked():
                    pm.polyEditUV(relative=True, uValue=(i / 10.0), vValue=offset)
                else:
                    pm.polyEditUV(relative=True, vValue=(i / 10.0), uValue=offset)

        pm.select(selectedMeshes, r=True)


def main(standalone=False):
    if not standalone:
        ui = UVRampToolUI(get_maya_window())
    else:
        ui = UVRampToolUI()

    ui.show()
    return ui


if __name__ == "__main__":
    app = None
    try:
        app = QApplication(sys.argv)
    except:
        pass

    main_ui = main(True)

    if app:
        sys.exit(app.exec_())
