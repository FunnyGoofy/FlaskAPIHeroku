from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel 


class Stores(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        help="This field cannot be blank"
    )


    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "store not found"}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "store with name '{}' already exists".format(name)}, 404
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                return {"Error": "Failed to save into database"}, 500

            return store.json(), 201

    '''
    def put(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.name = name
        try:    
            store.save_to_db()
        except:
            return {"Warning": "Failed to save into database"}
    '''

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        else:
            return {"Warning": "store not exists"}

class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}