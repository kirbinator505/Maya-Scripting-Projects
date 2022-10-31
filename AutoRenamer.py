import maya.cmds as cmds

def AutoRenamer(name):
    selection = cmds.ls(sl=True)
    for index in range(len(selection)):
        newName = name + "_" + str(index)
        cmds.rename(selection[index], newName)

AutoRenamer("lmao")
