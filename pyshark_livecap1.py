import pyshark
import time
import trollius
import logging

logging.basicConfig()

# define interface
networkInterface = "eth0"

cap = pyshark.LiveCapture(interface=networkInterface)
cap = pyshark.LiveCapture(output_file="pyshark.pcap")
#cap = pyshark.LiveCapture(output_file="pyshark.pcap", include_raw=True, use_json=True)
#cap = pyshark.LiveCapture(interface=networkInterface, bpf_filter='tcp port 80')
print("\n\nCapturing on eth0...\n")
for packet in cap.sniff_continuously(packet_count=5):
        #print(packet)
        # adjusted output
    try:
        # get timestamp
        localtime = time.asctime(time.localtime(time.time()))

        # get packet content
        # pdata  = packet.data.data         # packet data
        protocol = packet.transport_layer   # protocol type
        src_addr = packet.ip.src            # source address
        src_port = packet[protocol].srcport # source port
        dst_addr = packet.ip.dst            # destination address
        dst_port = packet[protocol].dstport # destination port

        # output packet info
        print ("%s IP %s:%s <-> %s:%s (%s)" % (localtime, src_addr, src_port, dst_addr, dst_port, protocol))
    except AttributeError as e:
        # ignore packets other than TCP, UDP and IPv4
        pass
    print (" ")
cap.clear()
cap.close()
