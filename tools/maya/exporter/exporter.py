__author__ = "Michael Graessle"
__copyright__ = "Copyright 2017"

__all__ = ["Exporter"]

# standard library imports
import os
import sys

# Maya specific imports
import pymel.core as pm


class Exporter(object):
    @staticmethod
    def triangulate(use_triangles=True):
        """ Triangulate meshes upon export.

        Args:
            use_triangles (bool): Triangulate meshes?
        """

        mel_cmd = "FBXExportTriangulate -v "

        if use_triangles:
            mel_cmd += "true;"
        else:
            mel_cmd += "false;"

        pm.mel.eval(mel_cmd)

    @staticmethod
    def bake_animation(bake_keys=True, start=0, end=0):
        """ Set the FBX to bake the animation when exporting.

        Args:
            bake_keys (bool): True or False whether to bake the animation upon export.
            start (int): The start frame for the bake.
            end (int): The end frame for the bake.
        """

        mel_cmd = "FBXExportBakeComplexAnimation -v "

        if bake_keys:
            mel_cmd += "true;"
        else:
            mel_cmd += "false;"

        pm.mel.eval(mel_cmd)

        # set the start and end keyframe to bake if necessary.
        if start != 0 and bake_keys:
            pm.mel.eval("FBXExportBakeComplexStart -v {0};".format(start))

        if end != 0 and bake_keys:
            pm.mel.eval("FBXExportBakeComplexEnd -v {0};".format(end))

    @staticmethod
    def apply_key_reducer(use_reducer=True):
        """ Set whether to use the constant key reducer when exporting the FBX.

        Args:
            use_reducer (bool): True or False whether to use the constant key reducer.
        """

        mel_cmd = "FBXExportApplyConstantKeyReducer -v "

        if use_reducer:
            mel_cmd += "true;"
        else:
            mel_cmd += "false;"

        pm.mel.eval(mel_cmd)

    @staticmethod
    def set_export_animation_only(animation_only=True):
        """ Set the FBX settings to export animation only.

        Args:
            animation_only (bool): True or False whether to export animation only for this FBX.
        """

        mel_cmd = "FBXExportAnimationOnly -v "

        if animation_only:
            mel_cmd += "true;"
        else:
            mel_cmd += "false;"

        pm.mel.eval(mel_cmd)

    @staticmethod
    def export_fbx(output_path, selected=True, ascii=True):
        """ Export the FBX to the set path.

        Args:
            output_path (str): The path to export the FBX to.
            selected (bool): Export selected only?
            ascii (bool): Export the file as an ascii?
        """

        # check that the file is a valid FBX file path.
        if not output_path.endswith(".fbx"):
            raise IOError("Path {0} is not an FBX file.".format(output_path))

        dir_name = os.path.dirname(output_path)

        # make any necessary directories to avoid IO errors later.
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        if ascii:
            pm.mel.eval("FBXExportInAscii -v true;")

        output_path = output_path.replace("\\", "/")

        mel_export_cmd = 'FBXExport -f "{0}";'.format(output_path)

        # if export selected is chosen add the selected flag.
        if selected and pm.ls(sl=True):
            mel_export_cmd += " -s;"
        else:
            mel_export_cmd += ";"

        pm.mel.eval(mel_export_cmd)

    @staticmethod
    def get_maya_files(folder):
        """ Get the list of Maya files in a particular folder.

        Args:
            folder (str): The folder to search for Maya files.

        returns:
            list<string>
        """

        if not os.path.isdir(folder):
            raise IOError("{0} is not a folder".format(folder))

        maya_files = [os.path.join(folder, mfile) for mfile in os.listdir(folder) if
                      mfile.endswith(".ma") or mfile.endswith(".mb")]

        return maya_files

    @classmethod
    def batch_export_fbx(cls, input_folder, output_folder):
        """ Batch export a folder of Maya files as FBX files.

        Args;
            input_folder (str): The folder where the Maya files are located.
            output_folder (str): The folder to save the FBX files to.
        """

        if output_folder == "":
            return

        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        maya_files = cls.get_maya_files(input_folder)

        if not maya_files:
            return

        for i, m_file in enumerate(maya_files):
            pm.newFile(f=True)

            pm.openFile(m_file)

            file_name = os.path.basename(m_file)

            file_ext = m_file[m_file.index("."):]

            output_path = r"{0}\{1}".format(output_folder, file_name.replace(file_ext, ".fbx"))

            try:
                cls.export_fbx(output_path)
            except IOError:
                continue

            yield float(i + 1) / len(maya_files) * 100


if __name__ == '__main__':
    if len(sys.argv) == 3:
        input_path = sys.argv[1]
        fbx_path = sys.argv[2]
        Exporter.batch_export_fbx(input_path, input_path)
