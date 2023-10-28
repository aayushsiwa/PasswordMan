import csv
from ende import encode
from ende import decode
import os.path as o
from random import random
import keyboard
from time import gmtime, strftime

c=3

fields=['user','password']
def check_file_spec(filename,content,command,content2):
    if not o.isfile(f'{filename}.csv'):
        print(f"\nNo {content} Found...\n")
        a=input(f"Do you want to save a {content2}-")
        if 'y' in a:
            command()
        else:
            print("\nExiting...")
            exit()

if not o.isfile('imp.txt'):
    print("Imp file does not exist...\nCreating new key")
    with open("imp.txt", "w") as f:
        f.write(str(random()))
        f.close()
else:
    with open("imp.txt", "r") as f:
        r=f.read()
        f.close()  

def write_status(user_name,line0,line1):
    with open(f"{user_name}_status.txt","r") as fin, open(f'{user_name}_status.txt') as fout:
        if line0==0:
            for line in fin:
                fout.write(line)
        f.writelines(str(line0)+"\n"+str(line1))
        f.close()
#use dictionary in csv for status very hard in txt file
def read_status(user_name,lines):
    if verify_username(user_name):
        with open(f"{user_name}_status.txt","r") as f:
                content=f.readlines()
                if content==[]:
                    return 0
                else:
                    if lines==0:
                        return content[lines]
                    elif lines==1:
                        return content[lines]

def write_data(user_name,password):
    data={fields[0]:f'{encode(r,user_name)}',fields[1]:f'{encode(r,password)}'}
    with open("users.csv","a+") as file:
        f=csv.DictWriter(file,fieldnames=fields)
        try:
            f.writerow(data)
            print(f"\nNew User >{user_name}< created\n")
        except:
            print("Try Again!")

def verify_username(user_name):
    file=open("users.csv","r")
    f=csv.DictReader(file,fieldnames=fields)
    for i in f:
        if not o.isfile(f'{user_name}_status.txt'):
            d=open(f'{user_name}_status.txt','w')
            d.close()
        if i['user']==encode(r,user_name):
            return True
    file.close()

def create_user():
    global user_name
    r=0
    print("Creating New User...\n")
    print("Do not add spaces")
    while True:
        print("Name-",end="")
        if keyboard.read_key() == "esc":
            print()
            main()
            break
        else:
            user_name=input("")
            if ' ' in user_name or user_name=='':
                print("\nFound blank character in name\nTry Again!")
                r=1
                create_user()
            break
    if o.isfile('users.csv'):
        if verify_username(user_name):
            print("User Already Exists")
            c=input("Would you like to create a New User with a different Name-")
            if 'y' in c or 'Y' in c:
                print("Alright",end=" ")
                create_user()
            elif 'N' in c or 'n' in c:
                c=input("Then would you like to Login as Existing User-")
                if 'y' in c or 'Y' in c:
                    print("Alright",end=" ")
                    existing_user()
                else:
                    print("Then",end=" ")
                    main()
    password=input("Password-")
    cp=input("Confirm Password-")
    if ' ' in password or password=='':
        print("\nFound blank character in password\nTry Again!")
        r=1
        create_user()
    if cp!=password:
        print("\nPasswords do not match\nTry Again!")
        r=1
        create_user()

        if r==0:
            write_data(user_name,password)
            __init__()



def existing_user():
    global c
    global user_name
    check_file_spec("users","Users",create_user,"user")
    file=open("users.csv","r")
    f=csv.DictReader(file,fieldnames=fields)
    user_name=input("\n\nName-")
    c=int(read_status(user_name,1))
    if c>0:
        for i in f:
            if i==[]:
                continue
            elif i['user']!=encode(r,user_name):
                print("This User does not exist\nPlease enter the correct Name")
                break
            if i['user']==encode(r,user_name):
                t1=int(read_status(user_name,0))
                t2=int(strftime("%H%M%S",gmtime()))
                if t2>=t1+500 or t1==0:
                    password=input("Password-")
                    if i['password']==encode(r,password):
                        print("\nSuccessfull\n")
                        __init__()
                        write_status(user_name,0,3)
                        break
                    elif i['password']!=encode(r,password):
                        while c>0:
                            print("Please enter the correct password\nChances Left:%d"%c)
                            c-=1
                            write_status(user_name,0,c)
                            existing_user()
                            break
                else:
                    t1+=500
                    s=(t1-t2)%60
                    m=(t1-t2-s)/60
                    print("Wait for another %d minutes %d seconds"%(m,s))
                break  
    if c==0:
        print("You Entered Wrong Password 3 times\nPlease Try Again Later!")
        write_status(user_name,0,c)
        exit()
    file.close()      # print(f"{decode(r,i['user'])} || {decode(r,i['password'])}")
    print()

def main():
    global c
    try:
        n=input("Enter your choice\n0-Sign Up\n1-Login\n2-Exit\n:")
        while n=='':
            if c>0: 
                print(c)
                print("Don't leave the choice blank")
                c-=1
                main()
            else:
                print("Exiting...")
                exit()
        if n=='0' or 'S' in n or 's' in n:
            create_user()
        elif n=='1' or 'l' in n or 'L':
            existing_user()
        elif n=='2' or 'e' in n or 'E':
            exit()

    except KeyboardInterrupt:
        print("\nExiting...")
        exit()

def get_key(user_name):
    r2=''
    if not o.isfile(f'{user_name}_secret.txt'):
        print("Imp file does not exist...\nCreating new key")
        with open(f"{user_name}_secret.txt", "w") as f:
            f.write(str(random()))
            f.close()
    else:
        with open(f"{user_name}_secret.txt", "r") as f:
            r2=f.read()
            f.close()  
    return r2



def send_data():
    r2=get_key(user_name)
    web=input("Enter the name of the website-")
    username=input("Enter the username-")
    password=input("Enter the password-")
    fields=['website','username','password']
    data={fields[0]:f'{encode(r2,web)}',fields[1]:f'{encode(r2,username)}',
          fields[2]:f'{encode(r2,password)}'}
    with open(f"{user_name}pass.csv","a") as file:
        f=csv.DictWriter(file,fieldnames=fields)
        f.writerow(data)
        file.close()
        print("\nPassword Saved Successfully\n")

def get_data():
    r2=get_key(user_name)
    check_file_spec(f"{user_name}pass","Passwords",send_data,"password")
    fieds=['website','username','password']
    with open(f"{user_name}pass.csv","r") as file:
        f=csv.DictReader(file,fieldnames=fieds)
        print("\n\n\nWebsite || Username || Password")
        for i in f:
            if i==[]:
                continue
            else:
                print(f"{decode(r2,i['website'])} || {decode(r2,i['username'])} || {decode(r2,i['password'])}")
        print()
                
def get_specdata():
    check_file_spec(f"{user_name}pass","Passwords",send_data,"password")
    w=input("Enter the name of the website:")
    fieds=['website','username','password']
    with open(f"{user_name}pass.csv","r") as file:
        f=csv.DictReader(file,fieldnames=fieds)
        print("\n\n\nWebsite || Username || Password")
        for i in f:
            if i==[]:
                continue
            elif (w in decode(r,i['website'])):
                print(f"{decode(r,i['website'])} || {decode(r,i['username'])} || {decode(r,i['password'])}")
        print()

def __init__():
    while True:
        n=input("What do you want to do:\n0-New Password\n1-View Passwords\n2-View Specific Password\n3-Switch User\n4-Exit\n:")
        if 'new' in n or n=='0' or 'N' in n:
            send_data()
        elif n=='1' or 'v' in n or 'V' in n:
            get_data()
        elif n=='2' or (('V' in n or 'v' in n) and ('s' in n or 'S' in n)):
            get_specdata()
        elif n=='3' or 'switch' in n or 'S' in n:
            main()
            break
        elif n=='4' or 'exit' in n or 'E' in n:
            exit()

# try:
#     main()
# except FileNotFoundError:
#         print("No Passwords Found\n")
main()