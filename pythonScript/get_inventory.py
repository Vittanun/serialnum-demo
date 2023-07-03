from netmiko import ConnectHandler
from ipaddress import ip_network
from connect_detail import ConnectDetail1 ##, ConnectDetail2, ConnectDetail3
##from paramiko.ssh_exception import AuthenticationException
from pythonping import ping
import concurrent.futures
import pandas as pd
from os.path import exists as file_exists
import time
import sys

print('WELL DONE')
##ip_user = input('Enter ip_host network and subnet:')

start_time = time.perf_counter()

sheet = sys.argv[1].split('/')
##sheet = ip_user.split('/')

path = str(sys.path[0])+'\serialnum'+sheet[0]+'_'+sheet[1]+'.xlsx'

if file_exists(path) == False:
      print('No This file. Creating File at  '+sys.path[0])

      try:
            df = pd.DataFrame({'hostname': [], 'ip_addr': [], 'name': [], 'descr':[], 'pid':[], 'vid':[], 'sn':[]})
            df.to_excel(path, engine='openpyxl', sheet_name=sheet[0]+'_'+sheet[1], index=False) 
      except:
            print('Error to create file')
      else:
            print('Succesed')

elif file_exists(path) == True:
      print('File exists. Launching')

ips = list(ip_network(ip_user))

ip_hosts = []

for ip_host in ips:
       ip_hosts.append([str(ip_host)])

def getinventory(ip_hosts):    
      serials_list = []
      for ip_host in ip_hosts:
            try:
                  result = ping(ip_host, count=1)
                  if result.stats_packets_returned != 0:
                         
                        net_connect = ConnectHandler(**vars(ConnectDetail1(ip_host)))
                        net_connect.enable()
                        
                        hostname = net_connect.find_prompt().replace('#', '')
                        
                        serial_list = net_connect.send_command('show inventory', use_textfsm=True)
                        serial_list.insert(0, { 'hostname' : hostname,'ip_addr': ip_host})
                
                        net_connect.disconnect() 

                        for serial in serial_list:
                              serials_list.append(serial)

                        print(str(result._responses).replace('[', '').replace(']', '') + '   ' + ip_host + '   ' + hostname)
                
                  else:
                        print(str(result._responses).replace('[', '').replace(']', '') + '   ' + ip_host)

            except Exception as err:
                  print('!!! '+ str(err)+ '   ' + ip_host+'  !!!')
                  pass
      return serials_list

try:
      with concurrent.futures.ThreadPoolExecutor() as executor:
            summary = { executor.submit(getinventory, ip_host): ip_host for ip_host in ip_hosts }
            for future in concurrent.futures.as_completed(summary):
                  df2 = pd.DataFrame(future.result())
                  with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                        df2.to_excel(writer, sheet_name=sheet[0]+'_'+sheet[1],header=None, startrow=writer.sheets[sheet[0]+'_'+sheet[1]].max_row, index=False)
except Exception as err:
      print('Error to update file :  '+ str(err))
else:
      print('Succesed to update file')   

finish_time = time.perf_counter()

print(f'Finished in {round(finish_time - start_time, 2)} second(s)')

