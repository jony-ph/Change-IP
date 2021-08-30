import subprocess
import random
import os
import re

from io import open

IPS_PATH = '|Direccion de ips.txt|'
DNS_PATH = '|Direccion de dns.txt|'

# Create files and extract info

try:

    get_ips = (f'arp -a > {IPS_PATH}')
    subprocess.run(get_ips, shell=True)

    get_dns = (f'ipconfig /all > {DNS_PATH}')
    subprocess.run(get_dns, shell=True)

except ValueError as e:
    print(e)

if os.path.exists(IPS_PATH) and os.path.exists(DNS_PATH):

    # Get IP's in LAN

    ips_file = open(IPS_PATH, 'r')
    text_ip = ips_file.readlines()
    ips_file.close()
    os.remove(IPS_PATH)

    ips_online = []
    expression_ip = r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    for i in text_ip:

        if not(i == '\n'):
            ip_found = re.search(expression_ip, i)
            
            if ip_found != None:
                ips_online.append(ip_found.group())


    # Get DNS's

    dns_file = open(DNS_PATH)
    text_dns = dns_file.read()
    dns_file.close()
    os.remove(DNS_PATH)

    expression_dns = r'Servidores DNS(\.\s)+:\s((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\s+((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    dns_online = re.search(expression_dns, text_dns)
    dns_sentence = dns_online.group()

    dns_split = re.split('\n', dns_sentence)
    dns_online = []

    for i in dns_split:
        dns_found = re.search(expression_ip, i)
        dns_online.append(dns_found.group())

else: 

    print('No existe alguno de los archivos')

print('Las direcciones IP de la red y los DNS fueron extraidos con exito')


# IP Configuration 

current_ip = ips_online[0]
extension = re.split('\.', current_ip)
ext = extension[3]
random_octec = str(random.randint(0, 255))
new_ip = '192.168.' + random_octec + '.' + ext

for ip in ips_online:

    while new_ip == ip:

        random_octec = str(random.randint(0, 255))
        new_ip = '192.168.' + random_octec + '.' + ext

change_ip = f'netsh interface ipv4 set address name="|interface|" static {new_ip} |mascaraRed| |puertaEnlace|'

try:
    subprocess.run(change_ip, shell=True)
except ValueError as e:
    print(e)

print('Se cambió la IP exitosamente: ', new_ip)

# DNS Configuration

PRIMARY_DNS = ['8.8.8.8', '4.2.2.5', '208.67.222.222', '1.1.1.1', '8.26.56.26']
SECONDARY_DNS = ['8.8.4.4', '4.2.2.1', '208.67.220.220', '1.0.0.1', '8.20.247.20']

random_dns = random.randint(0, (len(PRIMARY_DNS)-1))

for dns in dns_online:

    while random_dns == dns:

        random_dns = random.randint(0, (len(PRIMARY_DNS)-1))

change_dns_primary = f'netsh interface ipv4 set dnsservers "|interface|" static {PRIMARY_DNS[random_dns]} validate=no'
change_dns_secondary = f'netsh interface ipv4 add dns "|interface|" {SECONDARY_DNS[random_dns]} index=2 validate=no'

try:
    subprocess.run(change_dns_primary, shell=True)
    subprocess.run(change_dns_secondary, shell=True)

except ValueError as e:

    print(e)

print('Se cambiaron los DNS exitosamente: ', PRIMARY_DNS[random_dns], SECONDARY_DNS[random_dns])