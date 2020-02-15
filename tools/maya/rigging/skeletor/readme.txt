This is a tool that allows for saving data such as joint position, rotation, and orientation out to a JSON file.  The data can then be read back in to rebuild the skeleton.  

To rebuild the skeleton from the data file you can use Skeletor.build_skeletons(paths)

For example:

import skeletor
skeletor.Skeletor.build_skeletons(['<path to data file>']

To save the skeleton to a file you can create a skeleton object based on selection and then save.  The skeleton object was meant to be generic and extensible enough
that functions such as from_selection() and build() could be made to work in another package other than Maya but the skeleton object could still be used by the main Skeletor 
class to rebuild the skeleton.

For example to save a skeleton from Maya:

import maya_skeleton
maya_skel = maya_skeleton.MayaSkeleton()
maya_skel.from_selection()
maya_skel.save("<path to data file>")