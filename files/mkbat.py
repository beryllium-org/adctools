rename_process("mkbat")
vr("opts", be.api.xarg())
if len(vr("opts")["w"]) or ("help" in vr("opts")["o"] or "h" in vr("opts")["o"]):
    if "m" in vr("opts")["o"]:
        vr("mul", float(vr("opts")["o"]["m"]))
    elif "multiplier" in vr("opts")["o"]:
        vr("mul", float(vr("opts")["o"]["multiplier"]))
    else:
        vr("mul", 1)
    if "v" in vr("opts")["o"]:
        vr("max_volt", float(vr("opts")["o"]["v"]))
    elif "max_volt" in vr("opts")["o"]:
        vr("max_volt", float(vr("opts")["o"]["max_volt"]))
    else:
        vr("max_volt", 4.2)
    if "s" in vr("opts")["o"]:
        vr("samples", int(vr("opts")["o"]["v"]))
    elif "samples" in vr("opts")["o"]:
        vr("samples", int(vr("opts")["o"]["max_volt"]))
    else:
        vr("samples", 30)
    if vr("opts")["w"][0] in pv[0]["analogio_store"]:
        vr("adcobj", pv[0]["analogio_store"][vr("opts")["w"][0]])
    else:
        vr("adcobj", be.devices["gpiochip"][0].adc(vr("opts")["w"][0]))
        if vr("adcobj") is not None:
            pv[0]["analogio_store"][vr("opts")["w"][0]] = vr("adcobj")
    if vr("adcobj") is not None:

        class battery:
            def __init__(self, adcobj, multiplier, max_volt, samples, pin_name):
                self._bat = adcobj
                self._samples = samples
                self._max_volt = max_volt
                self._multiplier = multiplier
                self._pin = pin_name

            @property
            def voltage(self) -> float:
                samples = []
                samples_taken = 0
                while samples_taken < self._samples:
                    val = self._bat.value
                    if val is not None:
                        samples.append(val / 65535 * self._bat.reference_voltage)
                        samples_taken += 1
                val = (sum(samples) / self._samples) * self._multiplier
                return val

            @property
            def percentage(self) -> int:
                return max(0, min(100, int((self.voltage / self._max_volt) * 100)))

            @property
            def pin_name(self) -> str:
                return self._pin

        be.based.run("mknod bat")
        vr("node", be.api.getvar("return"))
        be.api.subscript("/bin/stringproccessing/devid.py")
        be.devices[vr("dev_name")][vr("dev_id")] = battery(
            vr("adcobj"),
            multiplier=vr("mul"),
            max_volt=vr("max_volt"),
            samples=vr("samples"),
            pin_name=vr("opts")["w"][0]
        )
        del battery
        dmtex("Battery sensor registered at /dev/" + vr("dev_name") + str(vr("dev_id")))
    else:
        term.write("Could not allocate pin.")
else:
    be.based.run("cat /usr/share/help/mkbat.txt")
