def versionCodeGen(mainV,subV,patchV,modeFlag,buildCode):
    return f"v{mainV}.{subV}.{patchV} [{modeFlag}](build:{buildCode})".replace("\r","").replace("\n","")