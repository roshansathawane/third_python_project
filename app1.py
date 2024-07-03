# from flask import Flask, send_from_directory
# import os
# from app import app as api_blueprint  # Import the Blueprint from api.py

# app = Flask(__name__, static_folder='S:/workspace/data_search/data_search_web/dataSearchWeb/dist')
# app.register_blueprint(api_blueprint, url_prefix='/app')  # Register the Blueprint with a URL prefix

# # Serve Angular static files
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def serve(path):
#     if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
#         return send_from_directory(app.static_folder, path)
#     else:
#         return send_from_directory(app.static_folder, 'index.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
