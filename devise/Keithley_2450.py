from .source_measure_units import SMU
from .base import register_deviceclass
import pyvisa


class Keithley_2450(SMU):

    def datasheet(self):
        pass

    def connect(self):
        self.transport.connect()

    def disconnect(self):
        self.transport.disconnect()

    def check(self):
        if "KEITHLEY INSTRUMENTS,MODEL 2450" in self.transport.query("*IDN?"):
            print("Device KEITHLEY INSTRUMENTS,MODEL 2450 has been checked")
        else:
            raise Exception(f"Device KEITHLEY INSTRUMENTS,MODEL 2450 NOT have verified connection")

    def reset(self):
        self.transport.write("*RST")
        self.transport.write("SOUR:DEL MIN")
        self.transport.write(":ROUTe:TERM REAR")
        self.transport.write("VOLT:UNIT VOLT")
        self.transport.write("CURR:UNIT AMP")

    def set_voltage(self, channel, value, compliance):
        self.transport.write("SOUR:FUNC VOLT")
        self.transport.write(f"SOUR:volt {value}")
        self.transport.write(f"SOURce:VOLT:ILIM {compliance}")

    def set_current(self, channel, value, compliance):
        self.transport.write("SOUR:FUNC curr")
        self.transport.write(f"SOUR:curr {value}")
        self.transport.write(f"SOURce:CURRent:VLIM {compliance}")

    def get_current(self, channel):
        self.transport.write(":FUNC 'CURR'")
        return float(self.transport.query(":MEAS?"))

    def get_voltage(self, channel):
        self.transport.write(":FUNC 'VOLT'")
        return float(self.transport.query(":MEAS?"))

    def enable(self, en: bool, channel=1):
        if en:
            self.transport.write(":OUTPut:STATe ON")
        else:
            self.transport.write(":OUTPut:STATe OFF")

    def trigger_in_mode(self, mode, channel):
        pass

    def define_trigger_model(self, mode, line, n_cycles=None):
        if mode == "ebic_bottom":
            start_event = f"DIG{line}"
            self.transport.write(f":DIG:LINE{line}:MODE TRIG, IN")
            self.transport.write(f":TRIG:DIG{line}:IN:EDGE RIS")

            self.transport.write('TRIG:LOAD "Empty"')
            self.transport.write("TRIG:BLOC:BUFF:CLEAR 1")
            # self.transport.write(f'TRIG:BLOC:CONF:RECALL 2, "VoltCustomSweepList"')
            self.transport.write('TRIG:BLOC:SOUR:STAT 2, ON')
            self.transport.write(f"TRIG:BLOC:WAIT 3, {start_event}, enter")
            self.transport.write('TRIG:BLOC:MEAS 4')
            self.transport.write(f"TRIG:BLOC:BRAN:COUN 5, {n_cycles}, 3")
            self.transport.write("TRIG:BLOC:SOUR:STAT 6, OFF")


    def trigger(self):
        pass

    def setup_sense(self, int_time=0, autorange=False, compl=1e-3, i_range=1e-2, counts=1):
        nplc_time = int_time / (1 / 50)  # 50 Hz power supply
        self.transport.write(f'SENS:AZER:ONCE')
        self.transport.write(f'SENS:CURR:AZER OFF')
        self.transport.write(f'SENS:CURR:NPLC {max(0.01, nplc_time)}')

        if autorange:
            self.transport.write(f'SENS:CURR:RANG:AUTO 1')
        else:
            self.transport.write(f'SENS:CURR:RANG:AUTO 0')
            self.transport.write(f'SENS:CURR:RANG {i_range}')

        self.transport.write(f'SOUR:VOLT:ILIM {compl}')
        if counts != 1:
            self.transport.write(f'SENS:COUNT {counts}')

    def setup_source(self, v_range=20, autorange=False, readback=False, delay=0):
        self.transport.write(f'SOUR:FUNC VOLT')
        if autorange:
            self.transport.write(f'SOUR:VOLT:RANG:AUTO ON')
        else:
            self.transport.write(f'SOUR:VOLT:RANG:AUTO OFF')
            self.transport.write(f'SOUR:VOLT:RANG {v_range}')

        if delay is not None:
            self.transport.write(f'SOUR:VOLT:DEL:AUTO OFF')
            self.transport.write(f'SOUR:VOLT:DEL 0.01')
            self.transport.write(f'SOUR:VOLT:DEL {delay}')
        else:
            self.transport.write(f'SOUR:VOLT:DEL:AUTO ON')

        if readback:
            self.transport.write(f'SOUR:VOLT:READ:BACK ON')
        else:
            self.transport.write(f'SOUR:VOLT:READ:BACK OFF')

    def set_terminal(self, name):
        if name == "rear":
            self.transport.write('ROUT:TERM REAR')
        elif name == "front":
            self.transport.write('ROUT:TERM FRON')
        else:
            raise Exception(f"Expected 'rear' or 'front', found {name}")

    def get_traces(self, buffer="defbuffer1"):
        self.transport.write(f':TRACe:ACTual:END? "{buffer}"')
        ending_index = int(self.transport.read())
        self.transport.write(f':TRAce:DATA? 1, {ending_index}, "{buffer}", RELative, SOURce, READing')
        result = self.transport.read()
        result = result.split(',')
        result = list(map(float, result))
        data = {
            'time': result[::3],
            'source': result[1::3],
            'reading': result[2::3]
        }
        return data

    def close(self):
        self.transport.disconnect()

    def wait(self):
        """
            Waiting for the device to finish.
        """
        self.transport.write('*OPC?')
        while True:
            try:
                self.transport.read()
                break
            except pyvisa.errors.VisaIOError:
                continue

    def initiate(self):
        self.transport.write('INIT')


register_deviceclass("Keithley_2450", Keithley_2450)