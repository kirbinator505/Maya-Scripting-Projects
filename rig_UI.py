import maya.cmds as cmds

def btn_jnt():
    import rig_tools
    rig_tools.Create_Joints()

def btn_grp():
    import rig_tools
    #rig_tools.Create_Group()

window = 'rigToolUI'

if cmds.window(window, q=True, exists=True):
    cmds.deleteUI(window)

window = cmds.window('rigToolUI', widthHeight=(400, 300), sizeable=True, title='Rig Tools')
m_column = cmds.columnLayout(parent=window, adjustableColumn=True)
cmds.button(parent=m_column, label='Create Joint', command=btn_jnt())
cmds.button(parent=m_column, enable=false, label='Parent Group', command=btn_grp())

cmds.showWindow(window)