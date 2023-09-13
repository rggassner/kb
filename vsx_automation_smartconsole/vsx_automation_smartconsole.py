#Create a vsx virtual system based on a existing one, using 
#"ifconfig" and "netstat -rn" and "netstat -rn -A inet6" as input.
#Keyboard strokes are sent directly to smartconsole.
#Next hops can be translated using function change_routes.
#Function sort_interfaces allow you to chose wich interface
#will be the first one.
import pyautogui, time, re

int_list=[]
route4_list=[]
route6_list=[]
human_interval=10
lint=1
cint=.05
tint=.01

def create_interfaces():
    print('Creating interfaces:')
    for iface in int_list:
        pyautogui.keyDown('alt')
        pyautogui.press('a')
        pyautogui.keyUp('alt')
        time.sleep(cint)
        if iface['iftype'] == 'regular':
            create_regular(iface)
        elif iface['iftype'] == 'vswitch':
            create_vswitch(iface)

def create_regular(iface):
    pyautogui.press('r')
    time.sleep(cint)
    pyautogui.press('down')
    time.sleep(cint)
    pyautogui.press('tab')
    time.sleep(cint)
    pyautogui.write(iface['vlan'],interval=tint)
    time.sleep(cint)
    pyautogui.press('tab')
    time.sleep(cint)
    if 'v4add' in iface:
        pyautogui.write(iface['v4add'],interval=tint)
    time.sleep(cint)
    pyautogui.press('tab')
    time.sleep(cint)
    if 'v4mask' in iface:
        pyautogui.write(iface['v4mask'],interval=tint)
    time.sleep(cint)
    pyautogui.press('tab')
    time.sleep(cint)
    pyautogui.press('tab')
    time.sleep(cint)
    if 'v6add' in iface:
        pyautogui.write(iface['v6add'],interval=tint)
    time.sleep(cint)
    pyautogui.press('tab')
    time.sleep(cint)
    if 'v6mask' in iface:
        pyautogui.write(iface['v6mask'],interval=tint)        
    time.sleep(cint)            
    pyautogui.press('enter')
    time.sleep(lint)

def create_vswitch(iface):
    print("Creating vswitch.")
    pyautogui.press('s')
    time.sleep(cint)
    input("Human, please select vswitch interface for iface {} press enter and hurry back to smartconsole.".format(iface))
    time.sleep(human_interval)
    pyautogui.press('tab')
    time.sleep(cint)
    if 'v4add' in iface:
        pyautogui.write(iface['v4add'],interval=tint)
    time.sleep(cint)
    pyautogui.press('tab')
    time.sleep(cint)
    if 'v4mask' in iface:
        pyautogui.write(iface['v4mask'],interval=tint)
    time.sleep(cint)
    pyautogui.press('tab')
    time.sleep(cint)
    if 'v6add' in iface:
        pyautogui.write(iface['v6add'],interval=tint)
    time.sleep(cint)
    pyautogui.press('tab')
    time.sleep(cint)
    if 'v6mask' in iface:
        pyautogui.write(iface['v6mask'],interval=tint)        
    time.sleep(cint)            
    pyautogui.press('enter')
    time.sleep(lint)
    
def create_routes4():
    print("Creating routes v4:")
    for route in filter(lambda x: (not x['is_default']),route4_list):    
        print('net {} mask {} nexthop {}'.format(route['net'], route['mask'], route['nhop']))
        pyautogui.keyDown('alt')
        pyautogui.press('d')
        pyautogui.keyUp('alt')
        time.sleep(cint)
        pyautogui.write(route['net'],interval=tint)
        time.sleep(cint)
        pyautogui.press('tab')
        time.sleep(cint)
        pyautogui.write(route['mask'],interval=tint)    
        time.sleep(cint)        
        pyautogui.press('tab')
        time.sleep(cint)
        pyautogui.press('tab')
        time.sleep(cint)
        pyautogui.write(route['nhop'],interval=tint)    
        time.sleep(cint)
        pyautogui.press('enter')
        time.sleep(cint)

def create_default_v4():
    print("Creating default route v4:")
    for route in filter(lambda x: (x['is_default']),route4_list):    
        print('net {} mask {} nexthop {}'.format(route['net'], route['mask'], route['nhop']))
        pyautogui.keyDown('alt')
        pyautogui.press('u')
        pyautogui.keyUp('alt')
        time.sleep(cint)
        pyautogui.write(route['nhop'],interval=tint)    
        time.sleep(lint)
        pyautogui.press('enter')
        time.sleep(lint)

def create_default_v6():
    print("Creating default route v6:")
    for route in filter(lambda x: (x['is_default']),route6_list):    
        print('net {} mask {} nexthop {}'.format(route['net'], route['mask'], route['nhop']))
        pyautogui.keyDown('alt')
        pyautogui.press('u')
        pyautogui.keyUp('alt')
        time.sleep(lint)
        pyautogui.press('tab')
        time.sleep(lint)
        pyautogui.press('tab')
        time.sleep(lint)        
        pyautogui.write(route['nhop'],interval=tint)    
        time.sleep(lint)
        pyautogui.press('enter')
        time.sleep(lint)
 
def create_routes6():
    print("Creating routes v6:")
    for route in filter(lambda x: (not x['is_default']),route6_list):
        print('net {} mask {} nexthop {}'.format(route['net'], route['mask'], route['nhop']))
        pyautogui.keyDown('alt')
        pyautogui.press('d')
        pyautogui.keyUp('alt')
        time.sleep(cint)
        pyautogui.keyDown('alt')
        pyautogui.press('6')
        pyautogui.keyUp('alt')
        time.sleep(cint) 
        pyautogui.press('tab')
        time.sleep(cint)
        pyautogui.write(route['net'],interval=tint)
        time.sleep(cint)
        pyautogui.press('tab')
        time.sleep(cint)
        pyautogui.write(route['mask'],interval=tint)    
        time.sleep(cint)        
        pyautogui.press('tab')
        time.sleep(cint)
        pyautogui.press('tab')
        time.sleep(cint)
        pyautogui.write(route['nhop'],interval=tint)    
        time.sleep(cint)
        pyautogui.press('enter')
        time.sleep(cint)
 
def add_iface_list(v4add,v6add,v4mask,v6mask,iftype,vlan,ifname):
    if ifname == "lo" or ifname == "":
        return False
    else:
        this_dic={}
        if v4add != "":
            this_dic['v4add']=v4add
            this_dic['v4mask']=v4mask
        if v6add != "":
            this_dic['v6add']=v6add
            this_dic['v6mask']=v6mask  
        this_dic['iftype']=iftype
        if iftype=="regular":
            this_dic['vlan']=vlan
        this_dic['ifname']=ifname
        int_list.append(this_dic)

def read_interfaces():
    f=open('interfaces.txt','r')
    v4add=v6add=v4mask=v6mask=iftype=vlan=ifname=""
    for line in f:
        line=line.strip()
        is_if_name=re.search(r'(.*?)\s+Link encap:.*',line)
        is_v4=re.search(r'.*inet\saddr:(.*?)\s.*\sMask:(.*)',line)
        is_v6=re.search(r'.*inet6\saddr:\s(.*)/(.*?)\s+Scope:(.*)',line)        
        if is_if_name:
            add_iface_list(v4add,v6add,v4mask,v6mask,iftype,vlan,ifname)
            v4add=v6add=v4mask=v6mask=iftype=vlan=ifname=""
            is_regular=re.search(r'.*\.(.*)',is_if_name.group(1))
            ifname=is_if_name.group(1)
            if not (is_regular) and is_if_name.group(1) == "lo":
                iftype="loopback"
            elif is_regular:
                print('Interface regular: .{}. vlan: .{}.'.format(is_if_name.group(1),is_regular.group(1)))                
                iftype="regular"
                vlan=is_regular.group(1)
            else:
                print('Interface virtual switch: .{}.'.format(is_if_name.group(1)))                                
                iftype="vswitch"
        if is_v4:
            print('v4 address:.{}. mask:.{}.'.format(is_v4.group(1), is_v4.group(2)))        
            v4add=is_v4.group(1)
            v4mask=is_v4.group(2)
        if is_v6:
            if is_v6.group(3) == "Global":
                print('v6 address:.{}. mask:.{}.'.format(is_v6.group(1), is_v6.group(2)))
                v6add=is_v6.group(1)
                v6mask=is_v6.group(2)            
    f.close()
    add_iface_list(v4add,v6add,v4mask,v6mask,iftype,vlan,ifname)
    print(int_list)
 
def sort_interfaces():
    #make an interface the first, so it will be considered the main one.
    tmp_list=[]
    for iface in int_list:
        if 'v4add' in iface:
            is_main=re.search(r'^10\.10\.10\..*',iface['v4add'])
            if is_main:
                tmp_list.insert(0,iface)
            else:
                tmp_list.append(iface)
    return tmp_list
                
def change_routes4():
    tmp_list=[]
    for route in route4_list:
        if route['nhop'] == '10.10.10.2':
            route['nhop'] = '10.10.10.1'
        tmp_list.append(route)
    return tmp_list

def read_routes4():
    f=open('routesv4.txt','r')
    for line in f:
        line=line.strip()
        is_route=re.search(r'^(.*?)\s+(.*?)\s+(.*?)\s+UGH?\s.*',line)
        if is_route:
            if is_route.group(1) == '0.0.0.0' and is_route.group(3) == '0.0.0.0':
                route4_list.append({'net':is_route.group(1),'nhop':is_route.group(2),'mask':is_route.group(3), 'is_default':True})
            else:
                route4_list.append({'net':is_route.group(1),'nhop':is_route.group(2),'mask':is_route.group(3), 'is_default':False})            
def read_routes6():
    f=open('routesv6.txt','r')
    for line in f:
        line=line.strip()
        is_route=re.search(r'^(.*?)/(.*?)\s+(.*?)\s+UGH?\s.*',line)
        if is_route:
            if is_route.group(1) == '::' and is_route.group(2) == '0':
                route6_list.append({'net':is_route.group(1),'nhop':is_route.group(3),'mask':is_route.group(2), 'is_default':True})
            else:
                route6_list.append({'net':is_route.group(1),'nhop':is_route.group(3),'mask':is_route.group(2), 'is_default':False})

input('Press any key to start and switch to smartconsole.')
time.sleep(human_interval)
read_interfaces()
int_list=sort_interfaces()
read_routes4()
read_routes6()
route4_list=change_routes4()
create_interfaces()
create_routes4()
create_routes6()
create_default_v4()
create_default_v6()
