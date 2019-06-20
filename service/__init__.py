from boto3.dynamodb.conditions import Key, Attr
import boto3
from flask import Flask
from flask_restful import Resource,  Api, reqparse
import markdown
import os

# create an instance of flask
app = Flask(__name__)

# Create the API
api = Api(app)

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    endpoint_url=os.environ['AWS_ENDPOINT_DYNAMODB'])


def create_table():
    try:
        response = dynamodb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'identifier',
                    'AttributeType': 'S'
                },
            ],
            TableName=os.environ['DYNAMODB_TABLE'],
            KeySchema=[
                {
                    'AttributeName': 'identifier',
                    'KeyType': 'HASH'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
        )
        print(response)
        return response
    except:
        response = dynamodb.tables.all()
        print(response)
        pass


create_table()
dynamodb_table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

# put documentation on service root
@app.route("/")
def hello():
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


class ItemsList(Resource):
    def get(self):
        response = dynamodb_table.scan()
        return {'message': 'success', 'data': response['Items']}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)

        args = parser.parse_args()

        dynamodb_table.put_item(
            Item=args)

        return {'message': 'Item recorded', 'data': args}, 201


class Items(Resource):
    def get(self, identifier):
        try:
            query = dynamodb_table.query(
                KeyConditionExpression=Key('identifier').eq(identifier)
            )['Items'][0]
            print(query)
            return {'message': 'Item found', 'data': query}, 200
        except:
            return {'message': 'Item not found', 'data': {}}, 404

    def delete(self, identifier):
        delete = dynamodb_table.delete_item(
            Key={'identifier': identifier}
        )
        return {'message': 'Item deleted', 'data': {}}, 204


# add routes
api.add_resource(ItemsList, '/items')
api.add_resource(Items, '/item/<string:identifier>')
