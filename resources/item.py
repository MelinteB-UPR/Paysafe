import json
import datetime
import os
from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("transfer",
                        type=dict,
                        required=True,
                        help="There is a lack of information in the transfer!"
                        )


    parser.add_argument('type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self):
        request_data = Item.parser.parse_args().get("transfer", None)

        checkCode = request_data['checkCode']
        item = ItemModel.find_by_name(checkCode)

        if item:
            if ItemModel.check_transfer(checkCode):
                item.status = 'Processing'
                item.save_to_db()
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self):
        x = datetime.datetime.now()
        date = str(x.day) + '-' + x.strftime("%b") + '-' + str(x.year)
        rpath = "c:/UPR/SFTP/IN/"
        local_path = os.path.join(rpath, date)
        if not os.path.exists(local_path):
            os.mkdir(local_path)
        print(f'path:{local_path}')
        request_data = Item.parser.parse_args()
        data = Item.parser.parse_args().get('transfer', None)
        # transfer = json.loads(data['transfer'])

        if ItemModel.find_by_name(data['checkCode']):
            return {'message': "An item with checkCode:'{}' already exists.".format(
                data['checkCode'])}, 400  # something when wrong with the request

        item = ItemModel(
            data['intermediateIBAN'],
            data['checkCode'],
            data['senderIBAN'],
            data['senderName'],
            data['receiverIBAN'],
            data['receiverName'],
            data['description'],
            data['amount'],
            data['currencyCode'],
            request_data['type'],
            "Received",  # initial status
        )  # {'name': name, 'price': request_data['price']}

        try:
            item.save_to_db()  # ItemModel.insert(item)
            try:
                item = ItemModel.find_by_name(data['checkCode'])
                print(f"Item:{item.json()}")

                f = open(os.path.join(local_path, "PaySafe_transfer_"+date+"_"+data['checkCode']+".csv"), "w", encoding='utf-8')
                f.write(str(item.json()).replace("Received", "Sent"))
                f.close()
                file = os.path.join(local_path, 'PaySafe_transfer_' + date + '_' + data['checkCode'] + '.csv')
                print(file, type(file))
                if os.path.isfile(file):
                    try:
                        ItemModel.load_transfer(file)
                        item.status = "Sent"
                        item.save_to_db()
                    except:
                        return {"message": "No able to connect to the SFTP. Try later."}, 500
                else:
                    return {"message": "The file doesn't exists."}, 500  # internal server error

            except:
                item = ItemModel.find_by_name(data['checkCode'])
                item.status = "Stiff"
                item.save_to_db()
                return {"message": "An error occurred transferring the item to SFTP."}, 500  # internal server error
        except:
            return {"message": "An error occurred inserting the item."}, 500  # internal server error

        return item.json(), 201

    # # @jwt_required()
    # def delete(self, name):
    #     item = ItemModel.find_by_name(name)
    #     if item:
    #         item.delete_from_db()
    #
    #     return {'message': 'Item deleted.'}
    #
    # # @jwt_required()
    # def put(self, name):
    #     # request_data = request.get_json()
    #     request_data = Item.parser.parse_args()
    #
    #     item = ItemModel.find_by_name(name)
    #
    #     if item is None:
    #         item = ItemModel(name, request_data['price'], request_data['store_id'])
    #     else:
    #         item.price = request_data['price']
    #         item.store_id = request_data['store_id']
    #     item.save_to_db()
    #
    #     return item.json()


class ItemList(Resource):
    def get(self):
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {'items': [item.json() for item in ItemModel.query.all()]}
