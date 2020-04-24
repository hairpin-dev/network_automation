import sys
import time
import paramiko
import telnetlib


class Device:
    """
    Generic class representing a device
    """

    def __init__(self, ipaddr=None, hostname=None, conn=None, ssh_client=None):
        if ipaddr is None and hostname is None:
            print('No IP Address or Hostname specified!')
            sys.exit()
        elif ipaddr is None and hostname is not None:
            self.ipaddr = hostname
            self.hostname = hostname
        elif hostname is None and ipaddr is not None:
            self.ipaddr = ipaddr
            self.hostname = ipaddr
        else:
            self.ipaddr = ipaddr
            self.hostname = hostname
        self.conn = conn
        self.ssh_client = ssh_client

    def ssh(self, user, password):
        print('connecting to {} using SSH'.format(self.hostname))
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=self.hostname, username=user,
                                password=password)
        self.conn = self.ssh_client.invoke_shell()

    def telnet(self, user, password):
        """
        Connects to the device using the protocol TELNET,
        username and password are passed to the method.
        This is currently based on a Cisco device.
        """
        print('connecting to {} using Telent'.format(self.hostname))
        self.conn = telnetlib.Telnet(self.hostname)
        self.conn.read_until(b'Username: ')
        self.conn.write(user.encode('ascii') + b'\n')
        if password:
            self.conn.read_until(b'Password: ')
            self.conn.write(password.encode('ascii') + b'\n')


class t_cisco(Device):
    """
    A class for Cisco devices, which inherits from the Device class.
    """

    def close(self):
        """
        Exits/Logs out of the device.
        """
        self.conn.write(b'end\n')
        self.conn.write(b'exit\n')
        self.conn.read_all()

    def show_running_config(self):
        """
        Diplays the current running configuration of the device
        """
        self.conn.write(b'terminal length 0\n')
        self.conn.write(b'show running-config\n')
        self.conn.write(b'exit\n')
        cfg_output = self.conn.read_all()
        cfg_output = cfg_output.decode('utf-8').replace("'", '').rstrip()
        return cfg_output

    def create_vlan(self, vlans=None):
        """
        Creates vlans on the device from a list passed to the
        vlans parameter.
        """
        if vlans is None:
            vlans = []
        else:
            vlans = vlans
        self.conn.write(b'conf t\n')
        for vlan in vlans:
            self.conn.write(b'vlan ' + str(vlan).encode('ascii') + b'\n')
            self.conn.write(b'name Python_Vlan_'
                            + str(vlan).encode('ascii') + b'\n')
        self.conn.write('exit\n')
        self.conn.write(b'end\n')

    def remove_vlan(self, vlans=None):
        """
        Removes vlans on the device from a list passed to the
        vlans parameter
        """
        if vlans is None:
            vlans = []
        else:
            vlans = vlans
        self.conn.write(b'conf t\n')
        for vlan in vlans:
            self.conn.write(b'no vlan ' + str(vlan).encode('ascii') + b'\n')
        self.conn.write(b'end\n')


class s_cisco(Device):
    """
    A class for Cisco devices, which inherits from the Device class.
    """

    def close(self):
        """
        Exits/Logs out of the device.
        """
        self.ssh_client.close()

    def show_running_config(self):
        """
        Diplays the current running configuration of the device
        """
        self.conn.send(b'terminal length 0\n')
        self.conn.send(b'show running-config\n')

        time.sleep(1)
        cfg_output = self.conn.recv(65535)
        cfg_output = cfg_output.decode('utf-8').replace("'", '').rstrip()
        return cfg_output

    def create_vlan(self, vlans=None):
        """
        Creates vlans on the device from a list passed to the
        vlans parameter.
        """
        if vlans is None:
            vlans = []
        else:
            vlans = vlans
        self.conn.send(b'conf t\n')
        for vlan in vlans:
            self.conn.send(b'vlan ' + str(vlan).encode('ascii') + b'\n')
            self.conn.send(b'name Python_Vlan_'
                           + str(vlan).encode('ascii') + b'\n')
            time.sleep(0.5)
        self.conn.send(b'exit\n')
        self.conn.send(b'end\n')

    def remove_vlan(self, vlans=None):
        """
        Removes vlans on the device from a list passed to the
        vlans parameter
        """
        if vlans is None:
            vlans = []
        else:
            vlans = vlans
        self.conn.send(b'conf t\n')
        for vlan in vlans:
            self.conn.send(b'no vlan ' + str(vlan).encode('ascii') + b'\n')
            time.sleep(0.5)
        self.conn.send(b'end\n')


def main():
    """
    This is a class and should be imported into your project
    and not run directly.
    """
    sys.exit(0)


if __name__ == 'main':
    main()
