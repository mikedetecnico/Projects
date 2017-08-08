__author__ = "Michael Graessle"
__copyright__ = "Copyright 2017"

# standard library imports
import sys

# PySide imports
from PySide2.QtWidgets import *
from PySide2 import QtCore
import shiboken2

# Maya imports
import pymel.core as pm
import maya.OpenMayaUI as mui
import maya.cmds as cmds


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
    WINDOW_NAME = "UVRampTool"
    DEFAULT_MAP_NAME = "map2"

    def __init__(self, parent=None):
        """ Constructor.
        """
        super(UVRampToolUI, self).__init__(parent=parent)

        self.setWindowTitle("UV Ramp Tool")
        self.setFixedSize(400, 200)
        self.setObjectName(self.WINDOW_NAME)

        self.main_layout = QVBoxLayout()

        self.u_direction_radio = None

        self.v_direction_radio = None

        self.u_direction_offset = None

        self.u_direction_offset_slider_label = None

        self.v_direction_offset = None

        self.v_direction_offset_slider_label = None

        self.direction_scale = None

        self.direction_scale_slider_label = None

        self.uv_map_name = None

        self.setup_ui()

    def setup_ui(self):
        """ Setup the layout of the UI.
        """
        self.setup_direction_radio_buttons()

        full_direction_offset_layout = QVBoxLayout()

        direction_offset_layout = QHBoxLayout()

        direction_offset_label = QLabel("U Direction Offset")

        direction_offset_layout.addWidget(direction_offset_label)

        self.u_direction_offset = DoubleSlider()
        self.u_direction_offset.setMinimum(0)
        self.u_direction_offset.setMaximum(1)

        direction_offset_layout.addWidget(self.u_direction_offset)

        self.u_direction_offset_slider_label = QLabel(str(self.u_direction_offset.value()))

        direction_offset_layout.addWidget(self.u_direction_offset_slider_label)

        self.u_direction_offset.valueChanged.connect(lambda: self.on_slider_value_changed(self.u_direction_offset,
                                                                                          self.u_direction_offset_slider_label))

        full_direction_offset_layout.addLayout(direction_offset_layout)

        direction_offset_layout2 = QHBoxLayout()

        direction_offset_label2 = QLabel("V Direction Offset")

        direction_offset_layout2.addWidget(direction_offset_label2)

        self.v_direction_offset = DoubleSlider()
        self.v_direction_offset.setMinimum(0)
        self.v_direction_offset.setMaximum(1)

        direction_offset_layout2.addWidget(self.v_direction_offset)

        self.v_direction_offset_slider_label = QLabel(str(self.v_direction_offset.value()))

        direction_offset_layout2.addWidget(self.v_direction_offset_slider_label)

        self.v_direction_offset.valueChanged.connect(lambda: self.on_slider_value_changed(self.v_direction_offset,
                                                                                          self.v_direction_offset_slider_label))

        full_direction_offset_layout.addLayout(direction_offset_layout2)

        direction_offset_layout3 = QHBoxLayout()

        direction_offset_label3 = QLabel("Direction Scale")

        direction_offset_layout3.addWidget(direction_offset_label3)

        self.direction_scale = DoubleSlider()
        self.direction_scale.setMinimum(0.01)
        self.direction_scale.setMaximum(1)
        self.direction_scale.setValue(1)

        direction_offset_layout3.addWidget(self.direction_scale)

        self.direction_scale_slider_label = QLabel(str(self.direction_scale.value()))

        direction_offset_layout3.addWidget(self.direction_scale_slider_label)

        self.direction_scale.valueChanged.connect(
            lambda: self.on_slider_value_changed(self.direction_scale, self.direction_scale_slider_label))

        full_direction_offset_layout.addLayout(direction_offset_layout3)

        self.main_layout.addLayout(full_direction_offset_layout)

        uv_map_name_layout = QHBoxLayout()

        uv_map_name_label = QLabel("UV Map Name:")

        uv_map_name_layout.addWidget(uv_map_name_label)

        self.uv_map_name = QLineEdit(self.DEFAULT_MAP_NAME)

        uv_map_name_layout.addWidget(self.uv_map_name)

        self.main_layout.addLayout(uv_map_name_layout)

        button_layout = QHBoxLayout()

        track_button = QCommandLinkButton("Select")

        track_button.setFixedHeight(50)

        track_button.clicked.connect(self.on_track_selection)

        button_layout.addWidget(track_button)

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

    def setup_direction_radio_buttons(self):
        """ Setup the radio buttons used for selecting the U or V direction
        """
        direction_layout = QHBoxLayout()

        self.u_direction_radio = QRadioButton("U Direction")

        direction_layout.addWidget(self.u_direction_radio)

        self.v_direction_radio = QRadioButton("V Direction")

        self.v_direction_radio.setChecked(True)

        direction_layout.addWidget(self.v_direction_radio)

        self.main_layout.addLayout(direction_layout)

    def on_slider_value_changed(self, current_slider, slider_label):
        """ Run when the value of the slider has changed.
        """
        clamp_value = current_slider.value()

        current_slider.setValue(float(clamp_value))

        slider_label.setText(str(clamp_value))

    def on_track_selection(self):
        """ Starts tracking selection of components
        """
        pm.mel.eval("selectPref -tso 1;")

    def on_run(self):
        """ Lays out the UVs based on the order of selection.
        """
        with pm.UndoChunk():
            orderFaceSelection = cmds.ls(os=True)

            if not orderFaceSelection:
                pm.displayWarning("No faces selected! Make sure to use the select button.")
                return

            if not ".f" in orderFaceSelection[0]:
                pm.displayWarning("No faces selected!")
                return

            mesh = pm.PyNode(orderFaceSelection[0][:orderFaceSelection[0].find(".")]).getShape()

            selectedFaces = []

            for eachSelection in orderFaceSelection:
                try:
                    index = int(eachSelection[eachSelection.find("[") + 1:eachSelection.find("]")])
                except:
                    pm.displayWarning("Unable to create face index from " + eachSelection)
                    continue

                selectedFaces.append(mesh.f[index])

            selectedFaces.reverse()

            pm.polyUVSet(create=True, uvSet=self.uv_map_name.text())

            pm.polyUVSet(currentUVSet=True, uvSet=self.uv_map_name.text())

            pm.select(clear=True)

            for i, selFace in enumerate(selectedFaces):
                selMesh = selFace.node()

                pm.select(selFace, add=True)

            melProject = "polyAutoProjection -lm 0 -pb 0 -ibd 1 -cm 0 -l 2 -sc 1 -o 1 -p 6 -ps 0.2 -ws 0"

            melProject += ";"
            pm.mel.eval(melProject)

            for i, selFace in enumerate(selectedFaces):
                for vtx in selFace.getVertices():
                    uvIndices = selMesh.vtx[vtx].getUVIndices(uvSet="map2")
                    uvIndices.sort()

                    uvIndex = uvIndices[-1]

                    pm.select(selMesh.map[uvIndex], add=True)

            pm.polyMapCut(ch=1)

            selectedFaces.reverse()

            for x, selFace in enumerate(selectedFaces):
                pm.select(selFace, r=True)

                pm.polyEditUV(pivotU=0.5, pivotV=0.5, scaleU=0.1, scaleV=0.1)

                u_offset = 0.00

                try:
                    u_offset = self.u_direction_offset.value()
                except:
                    pass

                v_offset = 0.00

                try:
                    v_offset = self.v_direction_offset.value()
                except:
                    pass

                if self.u_direction_radio.isChecked():
                    u_Value = (x + u_offset)

                    pm.polyEditUV(vValue=0, uValue=u_Value)

                    pm.polyEditUV(uValue=-0.45, vValue=-0.45)

                    pm.polyEditUV(pu=0.0, pv=0.0, su=1.0 / len(selectedFaces), sv=1.0 / len(selectedFaces))

                    pm.polyEditUV(pu=0.0, pv=0.0, scaleU=self.direction_scale.value(),
                                  scaleV=self.direction_scale.value())

                    pm.polyEditUV(relative=True, vValue=v_offset, uValue=u_offset)

                else:
                    v_Value = (x + v_offset)

                    pm.polyEditUV(vValue=v_Value, uValue=0)

                    pm.polyEditUV(uValue=-0.45, vValue=-0.45)

                    pm.polyEditUV(pu=0.0, pv=0.0, su=1.0 / len(selectedFaces), sv=1.0 / len(selectedFaces))

                    pm.polyEditUV(pu=0.0, pv=0.0, scaleU=self.direction_scale.value(),
                                  scaleV=self.direction_scale.value())

                    pm.polyEditUV(relative=True, vValue=v_offset, uValue=u_offset)

            pm.select(selectedFaces, r=True)


def main(standalone=False):
    # delete the UI if it exists already
    if pm.window(UVRampToolUI.WINDOW_NAME, exists=True):
        pm.deleteUI(UVRampToolUI.WINDOW_NAME)

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
