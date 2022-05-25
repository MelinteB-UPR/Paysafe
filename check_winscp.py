import subprocess
import os
import datetime
from cryptography.fernet import Fernet



def write_key():
    """
    Generates a key and save it into a file
    """
    key=Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key(key):
    """
    Load the key from the current directory named 'key.key'

    """
    return open(key, "rb").read()

def check_winscp():
    x = datetime.datetime.now()
    date = str(x.day) + '-' + x.strftime("%b") + '-' + str(x.year)
    rpath = "c:/UPR/SFTP/Out/"
    local_path = os.path.join(rpath, date)

    if not os.path.exists(local_path):
        os.mkdir(local_path)
    print(f'path:{local_path}')
    process = subprocess.Popen(['C:/Program Files (x86)/WinSCP/WinSCP.com',
                           '/ini=nul',
                           '/command',
                           'open sftp://tst_svc_ro_payports_salarypayments_brci_payports:5mIKEVYGEkeCBfo0;fingerprint=ssh-rsa-khG7LgRIqD_rHE9BeLL7fPZSPBPJxLoul3YGJ4S-oQc@sftpup.birlesikodeme.com:2222/ ',
                           'ls ',
                           'cd out',
                           f'get -delete *.txt {local_path}\*.txt',
                           f'put {local_path}\*.txt  /archive/out/',
                           'cd /archive/out',
                           'ls',
                           'close',
                           'exit'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    for line in iter(process.stdout.readline, b''):
        print(line.decode().rstrip())


def load_transfer(file):

    local_path = file
    print(local_path)
    process = subprocess.Popen(['C:/Program Files (x86)/WinSCP/WinSCP.com',
                           '/ini=nul',
                           '/command',
                           'open sftp://tst_svc_ro_payports_salarypayments_brci_payports:5mIKEVYGEkeCBfo0;fingerprint=ssh-rsa-khG7LgRIqD_rHE9BeLL7fPZSPBPJxLoul3YGJ4S-oQc@sftpup.birlesikodeme.com:2222/ ',
                           'ls ',
                           'cd in',
                           # f'get -delete *.csv {local_path}\*.csv',
                           f'put {local_path}  /in/',
                           # 'cd /archive/out',
                           'ls',
                           'close',
                           'exit'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    for line in iter(process.stdout.readline, b''):
        print(line.decode().rstrip())
if __name__=="__main__":
    # write_key()
    # key = load_key()
    # message = "some secret message".encode()
    # print(message)
    # f = Fernet(key)
    # encrypted = f.encrypt(message)
    # print(encrypted)
    # decrypted = f.decrypt(encrypted)
    # print(decrypted)
    # check_winscp()
    load_transfer()