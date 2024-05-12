import public_ip as ip
import time
import argparse
from git import Repo
import os

# parser=argparse.ArgumentParser()
# parser.add_argument('id', help='The github ID to be used')

# args=parser.parse_args()

# print(args.id)

side_dir=os.listdir("./PushingFolder")
id="kunalvirwal"


if ".git" not in side_dir:
    repo=Repo.clone_from(f"https://github.com/{id}/IPHistory.git","./PushingFolder")
else:
    repo=Repo("./PushingFolder")

if "PublicIP.txt" not in side_dir:
    f=open("./PushingFolder/PublicIP.txt",'w')
    a=ip.get()
    f.seek(0)
    f.write(a)
    f.close()

origin = repo.remotes['origin']

print(type(origin))
run=True  
delay=5  # seconds

# ####################### Accessing the last IP
# f=open("./PushingFolder/PublicIP.txt",'r')
# f.seek(0)
# lastIP=f.read()

# while run:
#     ############# Gets the current Public IP
#     a=ip.get()
#     f.seek(0)
#     lastIP=f.read()
#     print(a,"\t",lastIP,end="\t")

#     if a==lastIP:
#         print("same")
#     else:
#         # origin.fetch()
#         origin.pull()
#         ############################### Clears the old IP and adds the new IP
#         rf=open("./PushingFolder/PublicIP.txt",'w')
#         rf.write(a)
#         rf.close()

#         ############################### This code should push the text file to github or firebase
#         curr=time.ctime()
#         file="./PublicIP.txt"
#         add_files=[file]
#         repo.index.add(add_files)
#         msg="Updating IP"+curr
#         repo.index.commit(msg)

#         origin.push()
#         print("Different")

        
#     time.sleep(delay)
    