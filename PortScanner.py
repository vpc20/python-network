#!"C:\Program Files\Python36\"

import argparse
from socket import *


def conn_scan(tgt_host, tgt_port):
    try:
        # Create the socket object
        conn_sock = socket(AF_INET, SOCK_STREAM)
        # try to connect with the target
        conn_sock.connect((tgt_host, tgt_port))
        print(f'[+] tcp port {tgt_port} open')
        # print_banner(connSock, tgt_port)
        try:
            print(f'Service name: {getservbyport(tgt_port, "tcp")}\n')
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
            for p in [25, 80, 443, 20, 21, 23, 143, 3389, 22, 53, 110, 139, 445]:
                conn_scan(host, p)
        elif '-' in port:
            ps =  port.split('-')
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
