import maya.cmds as mc
import random

def makeGear(radius, height, thickness, sections):
    inner = mc.polyPipe(r = 3.5, h = height, t = 1)
    gear = mc.polyPipe(r = radius, h = height, t = thickness)
    mc.setAttr(gear[1] + ".subdivisionsAxis", sections)
    for i in range(sections):
        if(i % 2 == 0):
            mc.select( gear[0] + ".f[" + str(i) + "]" )
            exFace = mc.polyExtrudeFacet(gear[0] + ".f[" + str(i + sections * 2) + "]")
            mc.setAttr(exFace[0] + ".localTranslate", 0, 0, 3, type="double3")
            mc.setAttr(exFace[0] + ".localScale", .75, 1, 1)
        if(i % 4 == 0):
            mc.select( gear[0] + ".f[" + str(i) + "]" )
            exFace = mc.polyExtrudeFacet(gear[0] + ".f[" + str(i) + "]")
            mc.setAttr(exFace[0] + ".localTranslate", 0, 0, radius - thickness - 3, type="double3")
            mc.setAttr(exFace[0] + ".localScale", .8, 1, 1)
    
makeGear(10, 2, 3, 20)

