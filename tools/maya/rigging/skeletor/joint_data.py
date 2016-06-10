__all__ = ['JointData']

# standard library imports
import abc

# core imports
from ..transform import Transform


class JointData(Transform):
    def __init__(self, node=None):
        """ Constructor
        """
        super(JointData, self).__init__()

        self._name = ''
        self._mirrored_joint = None
        self._mirror = False
        self._node = node
        self._group = ''
        self._custom_attributes = dict()

    def __str__(self):
        return 'JointData({0})'.format(self.name)

    def __repr__(self):
        return 'JointData({0})'.format(self._name)

    def as_json(self):
        """ Returns a dictionary to be saved out for jSON

        Returns:
            (dict)
        """
        # create a copy of the dictionary representation
        # and make sure that the children and parent
        # are represented as dictionaries in the json data
        return_dict = self.__dict__.copy()

        return_dict['_node'] = None

        return return_dict

    def from_json(self, data):
        """ Loads data from a dictionary

        Args:
            data (dict): The dictionary data for the joint
        """

        self.__dict__ = data

    @property
    def name(self):
        """ Gets the name of the joint

        Returns:
            (str)
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Sets the name to the current value

        Args:
             value (str): The name to set
        """
        if not value:
            raise ValueError("Please pass a string for the name of the joint.")

        self._name = value

    @property
    def mirrored_joint(self):
        """ Gets the mirrored joint

        Returns:
            JointData
        """
        return self._mirrored_joint

    @property
    def mirror(self):
        """ True or False whether to mirror the joint

        Returns:
            True or False
        """
        return self._mirror

    @mirror.setter
    def mirror(self, value):
        """ Sets mirror to True or False

        Args:
            value: True or False
        """
        if not isinstance(value, bool):
            raise ValueError("Please pass a boolean for the mirror value.")

        self._mirror = value

    @property
    def group(self):
        """ Returns the current group

        Returns:
            (str)
        """
        return self._group

    @group.setter
    def group(self, value):
        """ Sets the group to the current value

        Args:
            value (str): The group the joint belongs to
        """
        self._group = value

    @property
    def custom_attributes(self):
        """ Returns the dictionary of custom attributes

        Returns:
            dict
        """
        return self._custom_attributes

    def add_attribute(self, key, value=None):
        """ Add a custom attribute to the attribute dictionary

        Args:
            key: The key or attribute name
            value: The attribute value or information
        """
        self._custom_attributes[key] = value

    @abc.abstractmethod
    def create(self):
        """ Create a joint based on the current data
        """
        return
