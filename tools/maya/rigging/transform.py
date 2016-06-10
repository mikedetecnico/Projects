__all__ = ['Transform']


class Transform(object):
    def __init__(self):
        """ Constructor
        """

        self._translation = [0.0, 0.0, 0.0]
        self._rotation = [0.0, 0.0, 0.0]
        self._scale = [1.0, 1.0, 1.0]
        self._orientation = [0.0, 0.0, 0.0]
        self._parent = None
        self._children = []

    @property
    def translation(self):
        """ Gets the current translation value

        Returns:
            list(float)
        """
        return self._translation

    @translation.setter
    def translation(self, value):
        """ Sets the translation value

        Args:
            value (list(float)): The value to set the translation to
        """
        if not value or not isinstance(value, list):
            raise ValueError("Please pass a valid list for translation")

        self._translation = value

    @property
    def rotation(self):
        """ Gets the current rotation value

        Returns:
            list(float)
        """
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        """ Sets the rotation to the current value

        Args:
            value (list(float)): The value to set the rotation to
        """
        if not value or not isinstance(value, list):
            raise ValueError("Please pass a valid list for rotation")

        self._rotation = value

    @property
    def scale(self):
        """ Gets the current scale value

        Returns:
            list(float)
        """
        return self._scale

    @scale.setter
    def scale(self, value):
        """ Sets the scale to the current value

        Args:
            value (list(float)): The value to set the scale to
        """
        if not value or not isinstance(value, list):
            raise ValueError("Please pass a valid list for scale")

        self._scale = value

    @property
    def orientation(self):
        """ Gets the current orientation

        Returns:
            list(float)
        """
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        """ Sets the orientation to the current value

        Args:
            value (list(float)): The current orientation value
        """
        if not value or not isinstance(value, list):
            raise ValueError("Please pass a valid list for scale")

        self._orientation = value

    @property
    def parent(self):
        """ Gets the parent of the joint

        Returns:
            JointData
        """
        return self._parent

    @parent.setter
    def parent(self, value):
        """ Sets the parent of the joint

        Args:
            value (JointData): The parent of the joint
        """
        self._parent = value

    @property
    def children(self):
        """ Gets the list of children of this joint

        Returns:
            list(JointData)
        """
        return self._children
