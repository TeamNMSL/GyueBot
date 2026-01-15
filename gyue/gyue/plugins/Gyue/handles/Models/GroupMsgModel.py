from gyue.gyue.plugins.Gyue.handles.Models.BaseMsgModel import BaseMsgModel
import json


class GroupMsgModel(BaseMsgModel):
    def getMsg(self)->str:
        return self.getEvt().get_plaintext()
    def getGroupid(self)->str:
        return str(json.loads(self.getEvt().model_dump_json())["group_id"])

