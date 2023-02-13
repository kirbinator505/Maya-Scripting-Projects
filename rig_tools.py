import maya.cmds as cmds

def Create_Joints():
    '''
    Create a joint at each selection at world orientation
    returns: [joints]
    '''
    sels = cmds.ls(sl = True)
    joints = []

    for sel in sels:
        cmds.select(cl=True)
        Xform_Data = Get_Xform(sel)

        joints.append(cmds.joint(position=Xform_Data[0], absolute=True))

    cmds.select(joints, r=True)
    return joints

def Create_Controlls(type='circle'):
    '''
    Create control at selected object(s) transformation
    returns: [controls]
    '''
    sels = cmds.ls(sl=True)
    ctrls = []

    for sel in sels:
        cmds.select(cl=True)
        if type is 'circle':
            ctrl = cmds.circle(center=[0,0,0], normal=[1,0,0], sweep=360, radius=1, degree=3, ut=0, tolerance=.01, sections=8, ch=True)[0]
        elif type is 'triangle':
            ctrl = cmds.curve(d=1,p=[(0,0.736878,0), (0, -0.632854, -0.773593), (0, -0.632854, 0.773593), (0, 0.736878, 0)], k=[0, 1, 2, 3])
        else:
            cmds.error('%p Invalid control shape: ' % shape)
        Xform_Data = Get_Xform(sel)

        cmds.xform(ctrl, worldSpace=True, translation=Xform_Data[0], rotation=Xform_Data[1], scale=Xform_Data[2])

        prefix = sel.rpartition('_Jnt')[0]
        ctrl = cmds.rename(ctrl, '%s_Ctrl' % (prefix))

        crtl = Create_Group(ctrl)[0]
        ctrls.append(ctrl)
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

def Create_Group(obj):
    '''
    create a new parent group at transformations of selection
    return: [obj, group)
    '''
    Xform_Data = Get_Xform(obj)
    parent = cmds.listRelatives(obj, parent=True, fullPath=True)


    cmds.select(cl=True)
    grp = cmds.group(world=True, empty=True)
    grp = cmds.rename(grp, '%s_Grp' % (obj))
    cmds.xform(grp, worldSpace=True,translation=Xform_Data[0], rotation=Xform_Data[1], scale=Xform_Data[2])
    if parent:
        grp = cmds.parent(grp, parent)[0]
    obj = cmds.parent(obj, grp)[0]

    cmds.select(obj, r=True)
    return [obj, grp]
