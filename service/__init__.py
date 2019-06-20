from boto3.session import Session
from boto3.dynamodb.conditions import Key
import boto3
from flask import Flask
from flask_restful import Resource,  Api, reqparse
from flask_dynamo import Dynamo
import markdown
import os

# create an instance of flask
app = Flask(__name__)

# Create the API
api = Api(app)

# define boto session for dynamo
boto_session = Session(
    region_name=os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)
app.config['DYNAMO_SESSION'] = boto_session

# define db
dynamodb_table = os.environ['DYNAMODB_TABLE']
app.config['DYNAMO_TABLES'] = [
    dict(
        TableName=dynamodb_table,
        KeySchema=[dict(AttributeName='identifier', KeyType='HASH')],
        AttributeDefinitions=[
            dict(AttributeName='identifier', AttributeType='S')],
        ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    ),
]
dynamo = Dynamo(app)
with app.app_context():
    dynamo.create_all()

for table_name, table in dynamo.tables.items():
    print(table_name, table)

# put documentation on service root
@app.route("/")
def hello():
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


class ItemsList(Resource):
    def get(self):
        response = dynamo.tables[dynamodb_table].scan()
        return {'message': 'success', 'data': response['Items']}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)

        args = parser.parse_args()

        dynamo.tables[dynamodb_table].put_item(Item=args)

        return {'message': 'Item recorded', 'data': args}, 201


class Items(Resource):
    def get(self, identifier):
        try:
            query = dynamo.tables[dynamodb_table].query(
                KeyConditionExpression=Key('identifier').eq(identifier)
            )['Items'][0]['identifier']
            return {'message': 'Item found', 'data': query}, 200
        except:
            return {'message': 'Item not found', 'data': {}}, 404

    def delete(self, identifier):
        delete = dynamo.tables[dynamodb_table].delete_item(
            Key={'identifier': identifier}
        )
        return {'message': 'Item deleted', 'data': {}}, 204


# add routes
api.add_resource(ItemsList, '/items')
api.add_resource(Items, '/item/<string:identifier>')
