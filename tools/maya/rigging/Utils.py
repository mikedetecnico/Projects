def using_maya():
    """ returns whether Maya is being used

    Returns:
        True if using Maya and able to import PyMel
    """

    try:
        import pymel.core as pm
        return True
    except ImportError:
        return False


class NodeVector(object):
    def __init__(self, x_value=0, y_value=0, z_value=0):
        self.x = x_value
        self.y = y_value
        self.z = z_value

    def __str__(self):
        return 'NodeVector({0}, {1}, {2})'.format(self.x, self.y, self.z)

    def x(self):
        return self.x

    def y(self):
        return self.y

    def z(self):
        return self.z
