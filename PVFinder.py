import maya.api.OpenMaya as om
import maya.cmds as cmds

def MakePV (dist):
    sels = cmds.ls(sl=True)

    jnt01 = sels[0]
    jnt02 = sels[1]
    jnt03 = sels[2]

    arm_pos = om.MVector (cmds.xform(jnt01, q=True, rp=True, ws=True))
    elbow_pos = om.MVector (cmds.xform(jnt02, q=True, rp=True, ws=True))
    wrist_pos = om.MVector (cmds.xform(jnt03, q=True, rp=True, ws=True))

    jnt02_x = cmds.getAttr("%s.translateX" %jnt02)

    jnt03_x = cmds.getAttr("%s.translateX" % jnt03)

    totLength = jnt02_x + jnt03_x

    lenMult = jnt02_x / totLength

    arm_to_wrist = wrist_pos - arm_pos
    arm_to_wrist_scaled = arm_to_wrist * lenMult
    mid_point = arm_pos + arm_to_wrist_scaled
    mid_point_to_elbow_vec = elbow_pos - mid_point
    mid_point_to_elbow_vec_scaled = mid_point_to_elbow_vec * dist
    mid_point_to_elbow_point = mid_point + mid_point_to_elbow_vec_scaled

    ctrl = cmds.circle(center=[0,0,0], normal=[1,0,0], sweep=360, radius=1, degree=3, ut=0, tolerance=.01, sections=8, ch=True)[0]

    cmds.xform(ctrl, t=mid_point_to_elbow_point)
    cmds.matchTransform(ctrl, jnt02, rot=True)
    cmds.rotate(0, '90deg', 0, ctrl, r=True, os=True)

def GenerateWindow():
    DistWindow = "Dist_Window"
    if cmds.window(DistWindow, ex=True):
        cmds.deleteUI(DistWindow, window=True)
    DistWindow = cmds.window("Dist_Window", wh=(500, 300), t="Distance multiplier for PV", s=True)
    ColumnLayout = cmds.columnLayout("Column_Layout", adj=True, p=DistWindow)
    NumVar = cmds.intField("Int_Field", min=2, v=5, p=ColumnLayout)
    cmds.button("RecolorButton", l="Create PV control", p=ColumnLayout,
                c='MakePV(cmds.intField("Int_Field", query = True, v = True))')
    cmds.textField("Text_Field", tx="select the IK joints before continuing", ed=False, p=ColumnLayout)

    cmds.showWindow(DistWindow)
GenerateWindow()