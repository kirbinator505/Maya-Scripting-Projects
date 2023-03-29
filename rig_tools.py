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

def Create_Controlls():
    '''
    Create control at selected object(s) transformation
    returns: [controls]
    '''
    sels = cmds.ls(sl=True)
    ctrls = []

    for sel in sels:
        cmds.select(cl=True)
        ctrl = cmds.circle(center=[0,0,0], normal=[1,0,0], sweep=360, radius=1, degree=3, ut=0, tolerance=.01, sections=8, ch=True)[0]
        Xform_Data = Get_Xform(sel)

        cmds.xform(ctrl, worldSpace=True, translation=Xform_Data[0], rotation=Xform_Data[1], scale=Xform_Data[2])

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
    return: [obj, group]
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

def Create_Grps():
    sels = cmds.ls(sl=True)
    for sel in sels:
        Create_Group(sel)

def AutoRenamer(name):
    selection = cmds.ls(sl=True)
    parents = cmds.listRelatives(selection, parent=True, fullPath=True)
    occurance = name.count("#")
    split = name.split("|")
    instance = 1
    for index in range(len(selection)):
        num = "0"*(occurance-len(str(instance))) + str(instance)
        newName = split[0] + "_" + num + "_" + split[2]
        cmds.rename(selection[index], newName)
        instance += 1
    instance = 1
    for index in range(len(parents)):
        num = "0" * (occurance - len(str(instance))) + str(instance)
        newName = split[0] + "_" + num + "_" + split[2] + "_Grp"
        cmds.rename(parents[index], newName)
        instance += 1

def MakeWindow():
    window = 'rigToolUI'

    if cmds.window(window, q=True, exists=True):
      cmds.deleteUI(window)

    window = cmds.window('rigToolUI', widthHeight=(400, 300), sizeable=True, title='Rig Tools')
    m_column = cmds.columnLayout(parent=window, adjustableColumn=True)
    cmds.button(parent=m_column, label='Create Joint', command='Create_Joints()')
    cmds.button(parent=m_column, label='Create Control', command='Create_Controlls()')
    cmds.button(parent=m_column, label='Parent Group', command='Create_Grps()')
    ColumnLayout = cmds.columnLayout("Column_Layout", adj = True, p = window)
    NameField = cmds.textField("Text_Field", p = ColumnLayout, pht = "enter in format \"Name|##|NodeType\"")
    cmds.button("ReNameButton", l = "Rename", p = ColumnLayout, c = 'AutoRenamer(cmds.textField("Text_Field", query = True, tx = True))')

    cmds.showWindow(window)

MakeWindow()