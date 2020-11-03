from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/api/ping', methods=['GET'])
def get_status():
    return jsonify({'success': True}), 200


@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Define error events
    tags_error = {'error': 'tags parameter is required'}
    sort_error = {'error': 'sortBy parameter is invalid'}
    direction_error = {'error': 'direction parameter is invalid'}

    # Parse query params
    tags = request.args.get('tags', default=None, type=str)
    if not tags: return jsonify(tags_error), 400

    sort_by = request.args.get('sortBy', default='id', type=str)
    if sort_by not in ['id', 'reads', 'likes', 'popularity', '']: return jsonify(sort_error), 400

    direction = request.args.get('direction', default='asc', type=str)
    if direction not in ['asc', 'desc', '']: return jsonify(direction_error), 400

    tags = request.args.get('tags').strip().lower().split(',')

    # For every tag in tags query param, fetch all posts that have specified tag listed in object
    data = [requests.get(f'https://api.hatchways.io/assessment/blog/posts?tag={tag}').json() for tag in tags]

    # Flatten data
    posts = [p for d in data for v in d.values() for p in v]

    # Filter out duplicate posts by 'id'
    ids = set()
    posts = [post for post in posts if post['id'] not in ids and (ids.add(post['id']) or True)]

    # Sort and order results based on sortBy and direction parameters
    filter_by = lambda x: x['id'] if sort_by in ['id', ''] else x[sort_by]
    is_reversed = True if direction == 'desc' else False
    result = sorted(posts, key=filter_by, reverse=is_reversed)

    return jsonify({'posts': result}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)