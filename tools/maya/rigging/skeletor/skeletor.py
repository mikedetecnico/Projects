__all__ = ['Skeletor']

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
            skeletons:  list(Skeleton) The list of skeletons to build
        """
        if not skeletons or not isinstance(skeletons, list):
            raise ValueError("Please pass a list of skeletons to build.")

        for skeleton in skeletons:
            if not isinstance(skeleton, Skeleton):
                continue

            skeleton.build()

        return True
