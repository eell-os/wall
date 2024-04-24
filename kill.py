import os
import psutil
import time

def get_connected_ips():
    connections = psutil.net_connections()
    ips = {}
    for connection in connections:
        if connection.laddr and connection.raddr:
            if connection.laddr.ip != '127.0.0.1':
                ip_pair = (connection.laddr.ip, connection.raddr.ip)
                if ip_pair in ips:
                    ips[ip_pair] += 1
                else:
                    ips[ip_pair] = 1
    return ips

def block_ip(ip):
    os.system(f"netsh advfirewall firewall add rule name=\"Block {ip}\" dir=in interface=any action=block remoteip={ip}")
    print(f"已经封禁 {ip}")
    time.sleep(120)  # 封禁2分钟
    os.system(f"netsh advfirewall firewall delete rule name=\"Block {ip}\"")
    print(f"已经解封 {ip}")

while True:
    ips = get_connected_ips()
    for ip, count in ips.items():
        print(f"Local IP: {ip[0]}, Remote IP: {ip[1]}, Connections: {count}")
        if count > 100:
            with open('C:/Users/Administrator/Desktop/wall.txt', 'a') as f:
                f.write(f"Local IP: {ip[0]}, Remote IP: {ip[1]}\nConnections: {count}\n")
            block_ip(ip[1])  # 封禁远程IP
    print("-------------------------------")
    time.sleep(5)  # 每5秒更新一次
