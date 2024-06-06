rename_process("rmbat")
vr("opts", be.api.xarg())

if len(vr("opts")["w"]):
    if vr("opts")["w"][0].startswith("/dev/bat"):
        vr("dev", vr("opts")["w"][0][5:])
        vr("node", vr("dev"))
        be.api.subscript("/bin/stringproccessing/devid.py")
        if vr("dev_name") in be.devices and vr("dev_id") in be.devices[vr("dev_name")]:
            pv[0]["analogio_store"][be.devices[vr("dev_name")][vr("dev_id")].pin_name].deinit()
            del pv[0]["analogio_store"][be.devices[vr("dev_name")][vr("dev_id")].pin_name]
            be.based.run("rmnod " + vr("dev_name") + str(vr("dev_id")))
        else:
            term.write("Not a valid device.")
    else:
        term.write("Not a valid device.")
else:
    term.write("No batteries specified.\n")
    term.write("Usage: rmbat /dev/batX")
