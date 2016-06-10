__all__ = ['MayaSkeleton']

# skeletor imports
from skeleton import Skeleton
from ..Utils import using_maya
from joint_factory import SkeletonJoint

if using_maya():
    # maya imports
    import pymel.core as pm


class MayaSkeleton(Skeleton):
    def __init__(self, prefix=''):
        """ Constructor
        """
        super(MayaSkeleton, self).__init__(prefix)

    def build(self):
        """ Builds the skeleton
        """

        super(MayaSkeleton, self).build()

        pm.select(cl=True)

    def from_selection(self):
        """ Initializes the skeleton data based on the currently selected joints
        """

        selection_list = pm.ls(sl=True, type='joint')

        if not selection_list:
            return

        for node in selection_list:
            if isinstance(node, pm.nodetypes.Joint):
                self._joints.append(SkeletonJoint(node))
