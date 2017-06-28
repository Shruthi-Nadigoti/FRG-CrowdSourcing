from flask import Blueprint


blueprint = Blueprint('hello_world', __name__)

@blueprint.route('/hello')
def hello():
	return "hello world"
