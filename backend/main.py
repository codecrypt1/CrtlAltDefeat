app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/')
def hello_world():
    return 'Hello frram Flask!'

@app.route('/test',methods=['POST','GET'])
def main():
	return 'Provide query'
	
    
if __name__ == '__main__':
    
    app.run(debug=True)
