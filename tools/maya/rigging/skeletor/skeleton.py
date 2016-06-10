__all__ = ['Skeleton']

# standard library imports
import os.path
import json
import abc

# skeletor imports
from joint_factory import SkeletonJoint
from joint_data import JointData


class Skeleton(object):
    def __init__(self, prefix=''):
        """ Constructor
        """

        self._prefix = prefix
        self._data_path = ''
        self._joints = []

    def __str__(self):
        return "Skeleton({0})".format(self.prefix)

    def build(self):
        """ Builds the skeleton
        """

        # create all of the joints in the scene
        for joint in self._joints:
            if not isinstance(joint, JointData):
                continue

            joint.create()

    def save(self, data_path):
        """ Saves the skeleton data to a jSON file
        """
        self._data_path = data_path

        if not self._data_path:
            return

        save_dict = self.__dict__.copy()

        joint_dictionaries = [joint.as_json() for joint in self.joints]

        save_dict['_joints'] = joint_dictionaries

        full_path = r'{0}'.format(self._data_path)

        with open(full_path, 'w') as outfile:
            json.dump(save_dict, outfile, indent=4)

    def load(self, file_path):
        """ Loads the skeleton data from the jSON file

        Args:
            file_path (str): The path to the data file
        """
        if file_path and os.path.exists(file_path):
            self._data_path = file_path

        if not self._data_path:
            return

        if not os.path.exists(self._data_path):
            raise IOError('Unable to find file at path {0}'.format(self._data_path))

        with open(self._data_path) as data_file:
            data = json.load(data_file)

            # load the joint data
            if '_joints' in data:
                self._joints = []
                joint_list = data['_joints']

                for joint_dict in joint_list:
                    skeleton_joint = SkeletonJoint()
                    skeleton_joint.from_json(joint_dict)
                    self._joints.append(skeleton_joint)

            # load the prefix data
            if '_prefix' in data:
                self._prefix = data['_prefix']

    @property
    def data_path(self):
        """ Gets the current path to the jSON file

        Returns:
            (str) The path to the data file
        """
        return self._data_path

    @data_path.setter
    def data_path(self, value):
        """ Sets the path to the jSON file

        Args:
            value: The path to the jSON file
        """
        if not value or not os.path.exists(value):
            raise ValueError('Please pass a string value as the path')

        self._data_path = value

    @property
    def prefix(self):
        """ Gets the name of the skeleton

        Returns:
            (str)
        """
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        """ Sets the prefix for the skeleton

        Args:
            value (str): The prefix for the skeleton
        """
        if not value:
            raise ValueError("Please pass a valid string for the prefix.")

        self._prefix = value

    @property
    def joints(self):
        """ Returns the current list of joints

        Returns:
            list(JointData)
        """
        return self._joints

    @abc.abstractmethod
    def from_selection(self):
        """ Initializes the skeleton data based on the currently selected joints
        """
        return
