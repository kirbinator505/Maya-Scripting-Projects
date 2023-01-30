import maya.cmds as cmds

def Create_Joints():
    sels = cmds.ls(sl = True)
    joints = []

    for sel in sels:
        cmds.select(cl=True)
        Xform_Data = Get_Xform(sel)

        joints.append(cmds.joint(position=Xform_Data[0], absolute=True))

    cmds.select(joints, r=True)
    return joints

def Create_Controlls():
    sels = cmds.ls(sl=True)
    ctrls = []

    for sel in sels:
        cmds.select(cl=True)
        ctrl = cmds.circle(center=[0,0,0], normal=[0,1,0], sweep=360, radius=1, degree=3, ut=0, tolerance=.01, sections=8, ch=True)[0]
        ctrls.append(ctrl)
        Xform_Data = Get_Xform(sel)

        cmds.xform(ctrl, worldSpace=True, translation=Xform_Data[0], rotation=Xform_Data[1], scale=Xform_Data[2])

    cmds.select(ctrls, r=True)
    return ctrls

def Get_Xform(obj):
    """
     gets the different transforms and returns them as three vectors in a list
     returns([Position, Rotation, Scale])
    """
    pos = cmds.xform(obj, q=True, worldSpace=True, translation=True)
    rot = cmds.xform(obj, q=True, worldSpace=True, rotation=True)
    scl = cmds.xform(obj, q=True, worldSpace=True, scale=True)
    return([pos, rot, scl])

Create_Controlls()