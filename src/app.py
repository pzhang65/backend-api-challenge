#src/app.py
import requests
from flask import Flask, jsonify, request
from .config import app_config

def create_app(env_name):

    app = Flask(__name__)
    app.config.from_object(app_config[env_name])


    @app.route('/api/ping', methods =['GET'])
    def ping():
        return jsonify({"success":True}), 200

    @app.route('/api/posts', methods=['GET'])
    def post():

        #initialize lists for checking query params
        sort_list = ["id", "reads", "likes", "popularity"]
        dir_list = ["desc", "asc"]

        #Parse query parameters
        query_tags = request.args.get("tag", None, type=str)
        #tag parameter must exist
        if query_tags is None:
            return jsonify({"error": "Tags parameter is required"}), 400

        #check sortBy value and store for use to sort later
        sort_by = request.args.get("sortBy", "id")
        if sort_by not in sort_list:
            return jsonify({"error": "sortBy parameter is invalid"}), 400

        #check direction value and store for use in reverse flag
        direction = request.args.get("direction", "asc")
        if direction not in dir_list:
            return jsonify({"error": "direction parameter is invalid"}), 400

        tags_list = query_tags.lower().split(",")

        try:
            data=[]
            for tag in tags_list:
                req=requests.get(f"https://api.hatchways.io/assessment/blog/posts?tag={tag}").json()
                data += req["posts"]

            #Print statements for debugging, remove comment for use
            #print(f"Number of posts is: {len(data)}")

            #remove duplicates using dictionary comprehensiion, and recast into list
            unique_data = list({ post["id"] : post for post in data }.values()) #no dup IDs allowed

            #Print statements for debugging, remove comment for use
            #print(f"Removed duplicate posts. New number of posts is: {len(unique_data)}")

            #sort ascending or descending based on params stored earlier
            if direction == dir_list[0]: #dir_list[0] is "desc"
                unique_data.sort(key=lambda x: x[sort_by], reverse=True)
            else:
                unique_data.sort(key=lambda x: x[sort_by], reverse=False)

            return jsonify({"posts":unique_data}),200
        except:
            #throw error for anything else, including connection issues
            return jsonify({"error": "Something went wrong, try again!"}),400


    return app
