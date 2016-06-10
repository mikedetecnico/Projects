__all__ = ['SkeletonJoint']

# skeletor imports
from joint_data import JointData
from maya_joint_data import MayaJointData
from ..Utils import using_maya


class SkeletonJoint(object):
    def __new__(cls, node=None):
        if using_maya():
            return MayaJointData(node)

        return JointData(node)
