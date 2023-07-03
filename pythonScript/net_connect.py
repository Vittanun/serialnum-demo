from netmiko import ConnectHandler
from connect_detail import ConnectDetail1, ConnectDetail2, ConnectDetail3

def net_connect1(ip_host):
        serials_list = []
        net_connect = ConnectHandler(**vars(ConnectDetail1(ip_host)))
        hostname = net_connect.find_prompt().replace('>', '').replace('#', '')
        serial_list = net_connect.send_command('show inventory').split('\n\n')
                
        net_connect.disconnect() 
                
        print(hostname + "  " +ip_host)
        serials_list.append([hostname] + [ip_host] + ['1'])

        for serial in serial_list:
            serial_str = str((serial).replace('\n',', ')).split(', ')
            serials_list.append(serial_str)

        serials_list.pop()   

        return serials_list    

def net_connect2(ip_host):
        serials_list = []
        net_connect = ConnectHandler(**vars(ConnectDetail2(ip_host)))
        hostname = net_connect.find_prompt().replace('>', '').replace('#', '')
        serial_list = net_connect.send_command('show inventory').split('\n\n')
                
        net_connect.disconnect() 
                
        print(hostname + "  " +ip_host)
        serials_list.append([hostname] + [ip_host] + ['2'])
    
        for serial in serial_list:
            serial_str = str((serial).replace('\n',', ')).split(', ')
            serials_list.append(serial_str)

        serials_list.pop()   

        return serials_list    

def net_connect3(ip_host):
        serials_list = []
        net_connect = ConnectHandler(**vars(ConnectDetail3(ip_host)))
        hostname = net_connect.find_prompt().replace('>', '').replace('#', '')
        serial_list = net_connect.send_command('show inventory').split('\n\n')
                
        net_connect.disconnect() 
                
        print(hostname + "  " +ip_host)
        serials_list.append([hostname] + [ip_host] + ['3'])


        for serial in serial_list:
            serial_str = str((serial).replace('\n',', ')).split(', ')
            serials_list.append(serial_str)

        serials_list.pop()   

        return serials_list    

