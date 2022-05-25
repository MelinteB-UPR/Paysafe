import json
import ast
import subprocess
from flask import jsonify
from db import db
from sqlalchemy.dialects.postgresql import JSON


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    intermediateIBAN = db.Column(db.String(34))
    checkCode = db.Column(db.String(80), unique=True, nullable=False)
    senderId = db.Column(db.String(80))
    senderIBAN = db.Column(db.String(34))
    senderMSISDN = db.Column(db.String(80))
    senderName = db.Column(db.String(80))
    receiverId = db.Column(db.String(80))
    receiverIBAN = db.Column(db.String(34))
    receiverMSISDN = db.Column(db.String(80))
    receiverName = db.Column(db.String(80))
    description = db.Column(db.String(200))
    amount = db.Column(db.Float(precision=2))
    currencyCode = db.Column(db.String(3))
    transfer_type = db.Column(db.String(20))
    status = db.Column(db.String(20))

    def __init__(self,
                 intermediateIBAN,
                 checkCode,
                 # senderId,
                 senderIBAN,
                 # senderMSISDN,
                 senderName,
                 # receiverId,
                 receiverIBAN,
                 # receiverMSISDN,
                 receiverName,
                 description,
                 amount,
                 currencyCode,
                 transfer_type,
                 # device_id
                 status,
                 ):
        self.intermediateIBAN = intermediateIBAN
        self.checkCode = checkCode
        # self.senderId = senderId
        self.senderIBAN = senderIBAN
        # self.senderMSISDN = senderMSISDN
        self.senderName = senderName
        # self.receiverId = receiverId
        self.receiverIBAN = receiverIBAN
        # self.receiverMSISDN = receiverMSISDN
        self.receiverName = receiverName
        self.description = description
        self.amount = amount
        self.currencyCode = currencyCode
        self.transfer_type = transfer_type
        # self.device_id = device_id
        self.status = status


    def json(self):

        return {

        "checkCode": self.checkCode,
        "senderId": "",
        "senderIBAN": self.senderIBAN,
        "senderMSISDN": "",
        "senderName": self.senderName,
        "receiverId": "",
        "receiverIBAN": self.receiverIBAN,
        "receiverMSISDN": "",
        "receiverName": self.receiverName,
        "description": self.description,
        "amount": self.amount,
        "currencyCode": self.currencyCode,
        "status": self.status,

        }

    def load_transfer(file):
        local_path = file
        print(local_path)

        process = subprocess.Popen(['C:/Program Files (x86)/WinSCP/WinSCP.com',
                                    '/ini=nul',
                                    '/command',
                                    'open sftp://tst_svc_ro_payports_salarypayments_brci_payports:5mIKEVYGEkeCBfo0;fingerprint=ssh-rsa-khG7LgRIqD_rHE9BeLL7fPZSPBPJxLoul3YGJ4S-oQc@sftpup.birlesikodeme.com:2222/ ',
                                    'ls ',
                                    'cd out',
                                    # f'get -delete *.csv {local_path}\*.csv',
                                    f'put {local_path}  /out/',
                                    # 'cd /archive/out',
                                    'ls',
                                    'close',
                                    'exit'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        for line in iter(process.stdout.readline, b''):
            print(line.decode().rstrip())

    def check_transfer(checkCode):

        print(checkCode)

        process = subprocess.Popen(['C:/Program Files (x86)/WinSCP/WinSCP.com',
                                    '/ini=nul',
                                    '/command',
                                    'open sftp://tst_svc_ro_payports_salarypayments_brci_payports:5mIKEVYGEkeCBfo0;fingerprint=ssh-rsa-khG7LgRIqD_rHE9BeLL7fPZSPBPJxLoul3YGJ4S-oQc@sftpup.birlesikodeme.com:2222/ ',
                                    'ls ',
                                    'cd /archive/out',
                                    'ls',
                                    'close',
                                    'exit'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        for line in iter(process.stdout.readline, b''):
            print(line.decode().rstrip())
            if checkCode in line.decode().rstrip():
                return True

    @classmethod
    def find_by_name(cls, checkCode):
        return cls.query.filter_by(checkCode=checkCode).first()  # SELECT * FROM items WHERE name = name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
