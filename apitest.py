from flask import Flask
from flask_restful import Api, Resource, reqparse
from firebase import firebase
import matplotlib.pyplot as plt



app = Flask(__name__)
api = Api(app)

users = [
    {
        "name": "Nicholas",
        "age": 42,
        "occupation": "Network Engineer"
    },
    {
        "name": "Elvin",
        "age": 32,
        "occupation": "Doctor"
    },
    {
        "name": "Jass",
        "age": 22,
        "occupation": "Web Developer"
    }
]


firebase = firebase.FirebaseApplication('https://fir-project-20449.firebaseio.com/')

result = firebase.get('/Returns', None)

prod_name=[]

prod_name.append(result['R1']['product returned']['Name'])
prod_name.append(result['R2']['Product returned']['Name'])
prod_name.append(result['R3']['product returned']['Name'])
prod_name.append(result['R4']['Product returned']['Name'])
qty=[]
qty.append(result['R1']['product returned']['Quantity Returned'])
qty.append(result['R2']['Product returned']['Quantity returned'])
qty.append(result['R3']['product returned']['Quantity Returned'])
qty.append(result['R4']['Product returned']['Quantity Returned'])


left = [1, 2, 3, 4]
qty = map (int , qty)

class User(Resource):
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                plt.bar(left, qty, tick_label = prod_name, 
        width = 0.8, color = ['red', 'green']) 
                plt.ylabel('Returns') 
                plt.title('Monitor returns product-wise.') 
                plt.show() 
                return user, 200
                
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200
        
        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200
      
api.add_resource(User, "/user/<string:name>")

app.run(debug=True)