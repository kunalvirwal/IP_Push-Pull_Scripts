import public_ip as ip
import time
import argparse
import socket
from git import Repo
import os

run=True  
delay=5  # seconds        # A 10 sec delay will on average consume 450 mb of data in a day   (0.05 MB/request)
mode="local"   #mode can be "public" or "local"
side_dir=os.listdir("./PushingFolder")
id="kunalvirwal"
backlog = False    #This variable becomes True when change in IP has be detected and committed but is not pushed to remote


def IP_collector(mode):
    
    if mode == "public":
        try:
            a=ip.get()
            
            if len(a)<7 or len(a)>15:   # the length of an IPV4 address is 13. This way if it returns an IPV6 address it will not be pushed
                return None
            return a


        except Exception as e:
           

            if str(e)=="all server queries failed":
                print("Unable to fetch IP")
                return None
            
            else: 
                k=str(e).split()
                if len(k[2])>len(k[4]):              #In the exception statements the 2nd and the 4th index words are the IPV4 and IPV6 addresses in random order so we check the lengths to find the smaller one
                    a=k[4]
                else:
                    a=k[2]
                return(a)
            

    if mode == "local":
        s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.0.0.0',0))
        return (s.getsockname())[0]







# parser=argparse.ArgumentParser()
# parser.add_argument('id', help='The github ID to be used')
# args=parser.parse_args()
# print(args.id)



if ".git" not in side_dir:
    print("IPfile git history not found!\nCloning",f"https://github.com/{id}/IPHistory.git...")
    while True:
        try:
            repo=Repo.clone_from(f"https://github.com/{id}/IPHistory.git","./PushingFolder")
            print("Repo cloned successfully!")
            break
        except Exception as e:
            print("Unable to clone repo!")

else:
    print("Git History detected!")
    repo=Repo("./PushingFolder")

if "IPFile" not in side_dir:
    while True:
        print("IPfile not found!\nGenerating IPFile...")
        f=open("./PushingFolder/IPFile",'w')
        a=IP_collector(mode)
        if a==None:
            continue
        else:
            f.seek(0)
            f.write(a)
            f.close()
            break

origin = repo.remotes["origin"]
repo.git.branch("--set-upstream-to=origin/main", "main")
print("Remote origin set.")

# Accessing the last IP
f=open("./PushingFolder/IPFile",'r')
f.seek(0)



while run:

    # Gets the current Public IP
    a=IP_collector(mode)
    if(a==None):
        continue  
    f.seek(0)
    lastIP=f.read()
    print(a,"\t",lastIP,end="\t")

    if a==lastIP:
        print("same")
    else:
        origin.fetch()
        origin.pull()
        # Clears the old IP and adds the new IP
        rf=open("./PushingFolder/IPFile",'w')
        rf.write(a)
        rf.close()

        # This code should push the text file to github or firebase
        curr=time.ctime()
        base_dir=os.getcwd()
        file=os.path.join(base_dir,"PushingFolder","IPFile")
        
        add_files=[file]
        repo.index.add(add_files)
        msg="Updating IP: "+curr
        repo.index.commit(msg)
        try:
            origin.push()
        except Exception as e:
            print("Unable to push changes to origin")
            backlog=True
        print("Different")

    if backlog:
        try:
            origin.push()
            backlog=False
        except Exception as e:
            print("Unable to push changes to origin")
      
    time.sleep(delay)
        