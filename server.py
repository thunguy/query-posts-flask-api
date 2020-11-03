from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/api/posts', methods=['GET'])
def get_posts():

    if request.args.get('tags'):
        tags = request.args.get('tags').split(',')
        sortBy = request.args.get('sortBy')
        direction = request.args.get('direction')

        responses = [requests.get(f'https://api.hatchways.io/assessment/blog/posts?tag={tag}&sortBy={sortBy}&direction={direction}') for tag in tags]
        posts = [r.json() for r in responses]
        posts = [post['posts'] for post in posts]
        posts = [p for post in posts for p in post]

        ids = set()
        result = [post for post in posts if post['id'] not in ids and (ids.add(post['id']) or True)]

        if direction == 'asc' or direction == 'desc' or direction == '':
            if sortBy == 'id' or sortBy == '': result = sorted(result, key=lambda x:x['id'], reverse=(direction == 'desc'))
            elif sortBy == 'reads': result = sorted(result, key=lambda x:x['reads'], reverse=(direction == 'desc'))
            elif sortBy == 'likes': result = sorted(result, key=lambda x:x['likes'], reverse=(direction == 'desc'))
            elif sortBy == 'popularity': result = sorted(result, key=lambda x:x['popularity'], reverse=(direction == 'desc'))
            else:
                return jsonify({'error': 'sortBy parameter is invalid'}), 400
        else:
            return jsonify({'error': 'direction parameter is invalid'}), 400

        return jsonify({'posts': result})

    else:
        return jsonify({'error': 'tags parameter is required'}), 400


@app.route('/api/ping', methods=['GET'])
def get_status():

    return jsonify({'success': True}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)