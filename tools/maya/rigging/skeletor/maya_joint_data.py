__all__ = ['MayaJointData']

# skeletor imports
from ..Utils import using_maya
from joint_data import JointData

if using_maya():
    # maya imports
    import pymel.core as pm


class MayaJointData(JointData):
    def __init__(self, node=None):
        """ Constructor
        """
        super(MayaJointData, self).__init__(node)
        self._initialize_from_node(node)

    def _initialize_from_node(self, node):
        """ Initialize the current joint from a Maya node

        Args:
            node (str or PyNode): The node to initialize from
        """

        if not node or not using_maya():
            return

        if isinstance(node, str) or isinstance(node, unicode):
            if pm.objExists(node):
                self._node = pm.PyNode(node)

        elif isinstance(node, pm.PyNode):
            self._node = node

        else:
            raise ValueError("Please initialize with a string of a name of a node or a PyNode.")

        # initialize the name
        self._name = self._node.name()

        # initialize translation and rotation values
        node_translation = self._node.getTranslation(space='world')
        self._translation = [node_translation.x, node_translation.y, node_translation.z]

        node_rotation = self._node.getRotation(space='world')
        self._rotation = [node_rotation.x, node_rotation.y, node_rotation.z]

        # initialize the orientation values
        if pm.hasAttr(self._node, 'jointOrientX'):
            x_orientation = pm.getAttr('{0}.jointOrientX'.format(self._node.name()))
            y_orientation = pm.getAttr('{0}.jointOrientY'.format(self._node.name()))
            z_orientation = pm.getAttr('{0}.jointOrientZ'.format(self._node.name()))

            self._orientation = [x_orientation, y_orientation, z_orientation]

        # initialize the parent
        self._parent = self._node.getParent().name() if isinstance(self._node.getParent(), pm.nodetypes.Joint) else ""

        # initialize the children
        child_list = [child for child in self._node.getChildren() if isinstance(child, pm.nodetypes.Joint)]

        for each_child in child_list:
            self._children.append(each_child.name())

    @JointData.translation.setter
    def translation(self, value):
        """ Sets the translation value

        Args:
            value (list(float)): The value to set the translation to
        """
        self._translation = value

        if self._node:
            self._node.setTranslation(value)

    @JointData.rotation.setter
    def rotation(self, value):
        """ Sets the rotation to the current value

        Args:
            value (list(float)): The value to set the rotation to
        """
        self._rotation = value

        if self._node:
            self._node.setRotation(value)

    @JointData.scale.setter
    def scale(self, value):
        """ Sets the scale to the current value

        Args:
            value (list(float)): The value to set the scale to
        """
        self._scale = value

        if self._node:
            self._node.setScale(value)

    @JointData.orientation.setter
    def orientation(self, value):
        """ Sets the orientation to the current value

        Args:
            value (list(float)): The current orientation value
        """
        self._orientation = value

        if self._node:
            self._node.setOrientation(value)

    @JointData.parent.setter
    def parent(self, value):
        """ Sets the parent of the joint

        Args:
            value (JointData): The parent of the joint
        """
        self._parent = value

        if self._node:
            self._node.setParent(value)

    def create(self):
        """ Creates the current joint in the scene
        """

        parent = self._parent if self._parent and pm.objExists(self._parent) else None

        self._node = pm.joint(parent, n=self._name, p=self._translation, o=self._orientation)
