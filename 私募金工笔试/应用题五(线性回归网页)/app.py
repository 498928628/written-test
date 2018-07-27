from flask import Flask
import config

app = Flask(__name__)
app.secret_key = config.secret_key

from routes.index import main as index_routes

app.register_blueprint(index_routes)

# 运行代码
if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
        threaded=True,
    )
    app.run(**config)
