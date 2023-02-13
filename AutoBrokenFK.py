import maya.cmds as cmds

#make viewport selection, parent control and then child control

#get selection, separate parent control and child control
sels = cmds.ls(sl=True) #only two selections, parent control and child control
parent_ctrl = sels[0]
child_ctrl = sels[1]

#get the parent group of the child control
child_ctrl_grp = cmds.listRelatives(child_ctrl, parent=True)[0] #[child controls parent node]

#create constraints
p_constraintT = cmds.parentConstraint(parent_ctrl, child_ctrl_grp, mo=True, skipRotate=['x','y','z'], weight=1)[0]
p_constraintR = cmds.parentConstraint(parent_ctrl, child_ctrl_grp, mo=True, skipTranslate=['x','y','z'], weight=1)[0]
cmds.scaleConstraint(parent_ctrl, child_ctrl_grp, weight=1)

#create attributes on the child control
if not cmds.attributeQuery('FollowTranslate', node=child_ctrl, exists=True):
    cmds.addAttr(child_ctrl, ln='FollowTranslate', at='double', min=0, max=1, dv=1)
    cmds.setAttr('%s.FollowTranslate' % (child_ctrl), e=True, keyable=True)
if not cmds.attributeQuery('FollowRotate', node=child_ctrl, exists=True):
    cmds.addAttr(child_ctrl, ln='FollowRotate', at='double', min=0, max=1, dv=1)
    cmds.setAttr('%s.FollowRotate' % (child_ctrl), e=True, keyable=True)

#connect sttributes from child control to constraint weights
cmds.connectAttr('%s.FollowTranslate' % (child_ctrl), '%s.w0' % (p_constraintT), f=True)
cmds.connectAttr('%s.FollowRotate' % (child_ctrl), '%s.w0' % (p_constraintR), f=True)