from scapy.all import *
import pygeoip
from IPy import IP as IPLIB
from socket import *
import time

# 1-Download/Install pygeoip: #easy_install pygeoip
# 2-Download/Extract GeoIP locations dat file at:
# wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz

conversations = {}
exclude_ips = ['10.0.2.133', '127.0.0.1']


def save_to_file(trace_info):
    try:
        # create the file log object
        filename = 'network_monitor_log_' + time.strftime("%d_%m_%Y") + '.txt'
        fileLog = open(filename, 'a')
        # write  the trace information to the file 
        fileLog.write(trace_info)
        # write a separator
        fileLog.write('\r\n')
        fileLog.write('--------------------------------')
        fileLog.write('\r\n')
        # close the file log object
        fileLog.close()
    except:
        pass


def get_info(ip_address):
    try:
        # try to resolve the IP address
        hostName = gethostbyaddr(ip_address)[0]
    except:
        # could not resolve the address
        hostName = ""

        # convert the IP to a valid IP object
    ip = IPLIB(ip_address)
    # do not proceed if the IP is private
    if ip.iptype() == 'PRIVATE':
        return 'private IP, Host Name: ' + hostName

    try:
        # initialize the GEOIP object
        geoip = pygeoip.GeoIP('GeoIP.dat')
        # get the record info
        ipRecord = geoip.record_by_addr(ip_address)
        # extract the country name
        country = ipRecord['country_name']
        # return the string results
        return 'Country: %s, Host: %s' % (country, hostName)
    except Exception as ex:
        # GeoIP could not locate the IP address
        return "Can't  locate " + ip_address + " Host:" + hostName


def print_packet(source_ip, destination_ip):
    # assemble the message that we need to print and save
    traceInfo = '[+] Source (%s): %s ---> Destination (%s): %s ' % (
        source_ip, get_info(source_ip), destination_ip, get_info(destination_ip))
    # print it to the console
    print(traceInfo)
    # save it to a file
    save_to_file(traceInfo)


def start_monitoring(pkt):
    try:
        if pkt.haslayer(IP):
            # get the source IP address
            sourceIP = pkt.getlayer(IP).src
            # get the destination IP address
            destinationIP = pkt.getlayer(IP).dst

            if destinationIP in exclude_ips:
                return;

            # generate a unique key to avoid duplication
            uniqueKey = sourceIP + destinationIP

            # if we already processed the packet, then don't proceed further
            if not conversations.has_key(uniqueKey):
                # store a flag in the array to avoid duplication
                conversations[uniqueKey] = 1
                # call the print packet function
                print_packet(sourceIP, destinationIP)
    except Exception as ex:
        print("Exception:" + str(ex))
        pass


def main():
    # start sniffing by filtering only the IP packets without storing anything inside the memory.
    sniff(prn=start_monitoring, store=0, filter="ip")


if __name__ == '__main__':
    main()
