import builtins as __builtin__
import gettext
from configure import *
language = getStr("Language","lang")
circleinterpolation = getInt("Geometry","circleinterpolation")
print (language,circleinterpolation)
# __builtin__._ = gettext.translation('Lines3DCAD', None, fallback=True).gettext
__builtin__._ = gettext.translation('Lines3DCAD', localedir="./locale/",fallback=True,languages=[language]).gettext
# __builtin__._ = gettext.translation('bCNC', os.path.join(prgpath,'locale'),
#                     fallback=True, languages=["fr"]).gettext
# class CADWindowStates():
#     Idle = 0
#     Select = 1
#     drawLine = 2
#     drawArc = 3
#     Move =4
#     Rotate = 5
def to_zip(*args, **kwargs):
    return list(zip(*args, **kwargs))

class ColorClass():
    default = 0
    erase = 1
    select = 2
    fromActiveLayer = 3
    fromElementLayer = 4

class StateMachineList():
    lineStateMachine = 0
    parallelStateMachine = 1
    selectStateMachine =2
    translateStateMachine= 3
    rotateStateMachine = 4
    circleStateMachine = 5
    ArcStateMachine = 6
    ellipticArc = 7

class SingletonIdGenerator(object):
    __instance = None
    def __new__(cls,*args,**kwargs):#, val):
        if SingletonIdGenerator.__instance is None:
            SingletonIdGenerator.__instance = object.__new__(cls)
        return SingletonIdGenerator.__instance

class IdGenerator(SingletonIdGenerator):
    def __init__(self):
        SingletonIdGenerator.__init__(self)
        if not hasattr(self, "id"):
            self.id =0
    def getNewId(self):
        result =self.id
        self.id +=1
        return result

