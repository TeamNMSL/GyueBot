import json

import gyue.gyue.plugins.Gyue.GlobalScope as gs

def getUpdateJson()->str:
    return gs.get_value(gs.key_botUpdateLogKey)

def getLatestUpdateInfo()->str:
    jo:list=json.loads(getUpdateJson())
    if len(jo)<1:
        return "No update log"
    jo.reverse()
    verName=jo[0]["versionName"]
    versions:list=jo[0]["versions"]
    if len(versions)<1:
        return "No update log"
    versions.reverse()
    vs:dict=versions[0]
    return f"v{vs["vcode"]}-{verName} ({vs["date"]})\n{vs["desc"]}"
