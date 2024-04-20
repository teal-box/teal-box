########### Cisco NSXO automation using python, netmiko, textfsm & ntc
########### Created & Maintained by CAS
###########

########### Import all Libraries ###########
from netmiko import ConnectHandler
import time
from datetime import datetime
import logging
import threading
from parseUtils import *
from myXLS import *
import concurrent.futures
from threading import Lock

######## Global Block ###############
code = "VA03"
# rsa = getpass()
# mypass =f"{code}{rsa}"
# print(mypass)
siteID = 'VA03'
lock = Lock()
inventoryfLock = Lock()
filetime = datetime.now().strftime("%b_%d_%H_%M_%S")
intstatusfilename = f"{siteID}_int_status_{filetime}.csv"
inventoryFilename = f"{siteID}_inventory_{filetime}.csv"
cdpfilename = f"{siteID}_cdp_{filetime}.csv"
######## END Global Block ###############

# cutover_Devices_sg05.xlsx
file = fr"H:\cutover\{siteID}\cutover_Devices.xlsx"
wb = fast_openpyxl(file)
cutover = wb[1]["sheet_cutover"]

############### Header Block ###########
cdpheader = "LOCAL_HOSTNAME,LOCAL_INTERFACE,REMOTE_HOSTNAME,REMOTE_INTERFACE"
intstatusheader = "HOSTNAME,PORT,NAME,STATUS,VLAN,DUPLEX,SPEED,TYPE"
intDescHeader = f"SWITCH,PORT,TYPE,SPEED,DESCRIPTION"
inventoryheader = f'HOSTNAME,IPADDR,SERIAL,PLATFORM,OS,BOOTFILE,POWER_SUPPLY,POWER_SUPPLY_MODEL,POWER_SUPPLY_STATUS,FAN,FAN_STATUS'
############### END Header Block ###########


all_devices = []

for item in cutover:
    print(f'Processing Device: {item["DeviceIP"]}')
    if item["Skip"].upper() == "YES" or "TBD" in item["DeviceIP"] or "#N/A" in item["DeviceIP"]:
        print(f'Check for Device: {item["DeviceName"]} <<>> {item["DeviceIP"]}')
        continue         
    # rsa = getpass()
    # mypass =f"{code}{rsa}"
   cisco1 = { 
        "device_type": "cisco_ios",
        "host": f"{item['DeviceIP']}",
        "username": "admin",
        "password": "hclhkO1@dmin",
        "read_timeout_override": 30
        }
    all_devices.append(cisco1)

####### open files all files for writing and put headers of files.
# with open(cdpfilename, "w") as cdpf, open(intstatusfilename, "w") as intstatusf, open(intDescFilename, "w") as intDescf:
intstatusf = open(intstatusfilename, "w")
intstatusf.write(intstatusheader)
intstatusf.write("\n")
inventoryf = open(inventoryFilename, "w")
inventoryf.write(inventoryheader)
inventoryf.write("\n")


def connect_and_fetch(device_data, file,lock,ifile,iLock):
    net_connect = ConnectHandler(**device_data)
    output = net_connect.send_command("show version")
    thishost = parseShowVersionHostname(output)
    hostInfo = parseNXShowVersion(output)
    output = net_connect.send_command('show int status')
    print(net_connect.host)
    print("*" * len(net_connect.host))
    intResults = parseIntStatus(output)
    output = net_connect.send_command("show environment")
    envResults = parseEnvStatus(output)

    # print(output)
    for item in envResults:
        environRow = f'{thishost},{net_connect.host},{hostInfo["SERIAL"]},{hostInfo["PLATFORM"]},{hostInfo["OS"]},{hostInfo["BOOT_IMAGE"]},{item["POWER_SUPPLY"]},{item["POWER_SUPPLY_MODEL"]},{item["POWER_SUPPLY_STATUS"]},{item["FAN"]},{item["FAN_STATUS"]}\n' 
        # print(environRow)
        with iLock:
            ifile.write(environRow)
    for item in intResults:
        intName = re.sub(r"[\"\']", '', item['NAME'])
        row = f"{thishost},{item['PORT']},{intName},{item['STATUS']},{item['VLAN']},{item['DUPLEX']},{item['SPEED']},{item['TYPE']}\n"
        with lock:
            file.write(row)


if __name__ == "__main__":
    threads = []
    # all_devices = [co05a, co05b]
    # for device in all_devices:
    #     print(device)
    for device in all_devices:
        # Spawn threads and append to threads list
        th = threading.Thread(target=connect_and_fetch, args=(device,intstatusf,lock,inventoryf,inventoryfLock))
        threads.append(th)
    
    # iterate through threads list and start each thread to perform its task
    for thread in threads: # Starting all threads in single, if we have many devices it will reach to limit.
        thread.start()

    #Once all threads have done the work, join the output of all threads to return the final output.
    for thread in threads:
        thread.join()


# # =================================================

# # max_workers=4 

# if __name__ == "__main__":
#     # all_devices = [co05a, co05b]
#     with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
#         executor.map(connect_and_fetch, all_devices)
