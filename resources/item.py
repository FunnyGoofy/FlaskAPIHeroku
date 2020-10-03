from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )
    #data = request.get_json()

    '''
    @jwt_required()
    def get(self, name):
        #for item in items:
        #    if item["name"] == name:
        #        return item
        
        #item = list(filter(lambda x : x["name"] == name, items))
        item = next(filter(lambda x : x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404
        #return {"item": item}, 200 if item is not None else 404
        #return {"message": "item not found"}, 404
    '''

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        
        return {'message': 'Item not found'}, 404

    @classmethod
    def post(cls, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = cls.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item not found'}, 404


    def put(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            data = Item.parse.parse_args()
            item = ItemModel(name, **data)
            #item = ItemModel(name, data['price'], data["store_id"])
        else:
            item.price = data['price']
            item.store_id = data["store_id"]
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred updating the item."}, 500

        return item.json()
        

    '''
    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        #data = request.get_json() #get_json(force=true)
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "item deleted"}

    def put(self, name):
        #data = request.get_json()
        
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        return item
    '''

class ItemList(Resource):
    def get(self):
        #return {"items": list(map(lambda x : x.json(), ItemModel.query.all()))}
        return {"items":  [item.json() for item in ItemModel.query.all()]}
