import numpy as np

class ClientMemory(object):
    def __init__(self, remote_connection):
        self.remote_connection = remote_connection
        try:
            self.remote_interface = remote_connection.root.mem()
        except AttributeError: # Assume a classic server
            self.remote_interface = remote_connection.modules['PyRedPitaya.raw_memory'].BoardRawMemory()

    def read(self, addr):
        return self.remote_interface.read(addr)

    def reads(self, addr, length, return_buffer=False):
        out = self.remote_interface.reads(addr, length, return_buffer=True)
        if return_buffer:
            return out
        else:
            return np.frombuffer(out, dtype='uint32')

    def write(self, addr, value):
        self.remote_interface.write(addr, value)

    def writes(self, addr, values):
        if not isinstance(values, str):
            values = np.array(values, dtype='uint32')
            values = str(values.data)
        self.remote_interface.writes(addr, values)

    def writes_many_addr(self, addrs, values):
        """Write values at each addrs

        input : addrs and values should be a list, np.array of numbers or a str (interpreted as a string buffer)"""
        if not isinstance(values, str):
            values = np.array(values, dtype='uint32')
            values = str(values.data)
        if not isinstance(addrs, str):
            addrs = np.array(addrs, dtype='uint32')
            addrs = str(addrs.data)

        self.remote_interface.writes_many_addr(addrs, values)

    def reads_many_addr(self, addrs, return_buffer=False):
        if not isinstance(addrs, str):
            addrs = np.array(addrs, dtype='uint32')
            addrs = str(addrs.data)
        out = self.remote_interface.reads_many_addr(addrs, return_buffer = True)
        if return_buffer:
            return out
        else:
            return np.frombuffer(out, dtype='uint32')

