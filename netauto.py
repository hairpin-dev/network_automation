import automation
from getpass import getpass


def connect_telnet():
    # Connect to the device using telnet protocol
    n1 = automation.t_cisco('192.168.1.10', 'Router1')
    user = input('Username: ')
    password = getpass()
    n1.telnet(user, password)

    # Create vlans on the device
    n1.create_vlan([10, 11, 21, 22, 31, 99])

    # Remove vlans from the deivce
    n1.remove_vlan([99])

    # Display running configuration on device
    run_cfg = n1.show_running_config()
    print(run_cfg)

    # Terminate connection
    n1.close()


def connect_ssh():
    # Connect to the device using SSH protocol
    n1 = automation.s_cisco('192.168.1.10', 'Router1')
    user = input('Username: ')
    password = getpass()
    n1.ssh(user, password)

    # Create vlans on the device
    n1.create_vlan([32, 41, 42, 51, 52, 199])

    # Remove vlans from the deivce
    n1.remove_vlan([199])

    # Display running configuration on device
    run_cfg = n1.show_running_config()
    print(run_cfg)

    # Terminate connection
    n1.close()


def main():
    """
    """
    connect_telnet()
    connect_ssh()


if __name__ == 'main':
    main()
