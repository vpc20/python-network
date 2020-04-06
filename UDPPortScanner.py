import argparse
from socket import *

COMMON_UDP_PORTS = [53,  # DNS
                    67,  # DHCP
                    68,  # DHCP
                    137,  # NetBIOS Naming Service
                    161,  # SNMP
                    389]  # LDAP


def conn_scan(host, port):
    try:
        # Create the socket object
        conn_sock = socket(AF_INET, SOCK_DGRAM)
        conn_sock.connect((host, port))
        print(f'[+] udp port {port} open')
        try:
            print(f'Service name: {getservbyport(port, "udp")}\n')
        except:
            print('Service name: Not available\n')
    except:
        pass
    finally:
        conn_sock.close()


def port_scan(host, ports):
    print(f'\n[+]--- Scan result for: {host} ---\n')
    setdefaulttimeout(10)

    # For each port number call the connScan function
    for port in ports:
        if port == 'common':
            for p in COMMON_UDP_PORTS:
                conn_scan(host, p)
        elif '-' in port:
            ps = port.split('-')
            start = ps[0]
            end = ps[1]
            if len(ps) == 2 and start.isdigit() and end.isdigit():
                for p in range(int(start), int(end) + 1):
                    conn_scan(host, int(p))
        else:
            conn_scan(host, int(port))


def main():
    argparser = argparse.ArgumentParser('TCP Port Scanner')
    argparser.add_argument("-a", "--address", type=str, help="The target IP address")
    argparser.add_argument("-p", "--port", type=str, help="The port number to connect with "
                                                          "(port number, 'common' or range). "
                                                          "Range format is 'start-end'")
    args = argparser.parse_args()
    if args.address is None or args.port is None:
        argparser.print_help()
        exit()

    ipaddress = args.address
    ports = args.port.split(',')

    # Call the Port Scan function
    port_scan(ipaddress, ports)


if __name__ == "__main__":
    # Call the main function
    main()
