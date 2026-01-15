from gyue.gyue.plugins.Gyue.handles.Models.BaseMsgModel import BaseMsgModel
class PrivateMsgModel(BaseMsgModel):
    def getMsg(self)->str:
        return self.getEvt().get_plaintext()
