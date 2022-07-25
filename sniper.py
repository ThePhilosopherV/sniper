#!/usr/bin/env python3

import socket, threading,sys,ipaddress,datetime,os

def countries():
    mypath = "country-ip-blocks/ipv4/"
    countries = next(os.walk(mypath), (None, None, []))[2]
    print("Available countries: ")
    for c in countries:
        print(c+',',end='')
    print('\nNumber of countries Available: '+str(len(countries)))
    quit('(Country codes as described by ISO 3166-1 alpha-2 )')
    
    
def geo(country):
    mypath = "country-ip-blocks/ipv4/"
    countris = next(os.walk(mypath), (None, None, []))[2]  # [] if no file
    if country not in countris:
        countries()
        
    file=mypath+country
    with open(file) as f:
        lines = f.read().splitlines()
    
    c=0
    
    for ip in lines:
        c+=1
        print('{'+ip+':'+str(c)+'}, ',end='')
    
    print("\nNumber of IP ranges: "+str(len(lines)))
    while 1:
        try:
            cntnmbr = int(input("Input IPs range number: "))
        except ValueError:
            print("Not a number")
            continue
        if len(lines)>= cntnmbr>=1:
            print("")
            return lines[cntnmbr-1]
        elif  cntnmbr<0 :
            print('Number must be positive')
        else:
            print('Number should be between 1 and '+str(len(lines)))
            

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]



targets=[]
def TCP_connect(ip, port, delay):
    #print(ip)
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    r=TCPsock.connect_ex((ip, port))
    if r==0:
        print(ip+':'+str(port))
        targets.append(ip+':'+str(port))
        



def scan_ports(iplist, delay,port):
    
    for ips in iplist:
        threads = []        
    
        for ip in ips:
            t = threading.Thread(target=TCP_connect, args=(ip, port, delay))
            threads.append(t)
    
        
        for i in range(len(ips)):
            threads[i].start()
    
        
        for i in range(len(ips)):
            try:
                threads[i].join()
            except KeyboardInterrupt:
                print()
                quit('CTRL+C signal')
help= """Usage:

./sniper <networkAddress/CIDR>/<Country code> <Port> <NumberOfThreads> [browser]

<Country code> : Country code represented in two alphabets,type ./sniper --countries for more info

[browser] :browser name is optinal, it activates IPs browsing; make sure [browser] is callable from any directory.

Examples: ./sniper.py 196.217.254.0/24 8080 200 firefox
         ./sniper.py us 8080 200 firefox 
         ./sniper.py  196.217.254.0/24 80 100"""
def main():
    
    if len(sys.argv)==1:
        print(help)
        quit()
        
    if sys.argv[1]=='--countries':
        countries() 
        
    global webflag
    webflag=0 
    
    if len(sys.argv[1])==2:
        netip=geo(sys.argv[1])
    
    else:netip=sys.argv[1]

    port = int(sys.argv[2])
    nthread = int(sys.argv[3])
    try:
        global webarg
        webarg = sys.argv[4]
        
        webflag=1
    except:
        pass
    try:
        ips = [str(ip) for ip in ipaddress.IPv4Network(netip)]
    except:
        print("Wrong network IP or country code")
        quit()
    print('Network IP: '+netip)
    print('number of targets: '+str(len(ips))+'\n')
    
    iplist = list(chunks(ips,nthread))
    
    delay = 3   
    scan_ports(iplist, delay,port)


t1 = datetime.datetime.now().replace(microsecond=0)
main()
t2= datetime.datetime.now().replace(microsecond=0)

#displaying time and number of positive targets

tl=str(t2-t1).split(':')
print('\nNumber of positive targets: '+str(len(targets)))
print("time elapsed: ",end='')

if tl[0] == '0' and tl[1]=='00':
    print(tl[2]+'s')
elif tl[0] != '0':
        print(tl[0]+'h'+ tl[1]+'m'+tl[2]+'s' )

elif tl[1] != '00':
        print(tl[1]+'m'+tl[2]+'s')
#browsing IPs

num = len(targets)
c=0
if webflag and num:

    print('\n<<< browsing IPs >>>>')
    
    while 1:
        cunts=int(input('How many IPs you want to browse ('+str(num)+' IP<s> left): '))
        if cunts > num :
            print('Number greater than IPs left')
            continue 
        elif cunts <= 0:
            print('Number must be a positive')
            continue
        for i in range(cunts):
            os.system(webarg+" "+targets[c])
            c+=1
      
        num -= cunts
        if num == 0:
            quit()


