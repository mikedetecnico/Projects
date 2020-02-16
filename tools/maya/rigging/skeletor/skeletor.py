__all__ = ['Skeletor']

import os

# skeletor imports
from skeleton import Skeleton
from maya_skeleton import MayaSkeleton
from ..Utils import using_maya


class Skeletor(object):
    def __new__(cls, prefix=''):
        if using_maya():
            return MayaSkeleton(prefix)

        return Skeleton(prefix)

    @classmethod
    def build_skeletons(cls, skeletons):
        """ Build a list of skeletons

        Args:
            skeletons:  list(str) The list of paths to the skeleton definitions to build
        """
        if not skeletons or not isinstance(skeletons, list):
            raise ValueError("Please pass a list of paths to the skeleton definitions to build.")

        skeleton_list = []

        for def_path in skeletons:
            if os.path.exists(def_path):
                char_skeleton_def = Skeleton()
                char_skeleton_def.load(def_path)
                skeleton_list.append(char_skeleton_def)

        for skeleton in skeleton_list:
            if not isinstance(skeleton, Skeleton):
                continue

            skeleton.build()

        return True
