import dicttoxml
from flask import Flask, render_template, request, jsonify, make_response, Response

app = Flask(__name__)
USERS = [
 {"id": 1, "name": "Ashley W. Walker", "phone": "317-769-0638", "birthday": "August 12, 1999", "email": "AshleyWWalker@dayrep.com", "username": "Joull1999"},
 {"id": 2, "name": "Martin M. Johnson", "phone": "301-962-1329", "birthday": "March 20, 1964", "email": "MartinMJohnson@teleworm.us", "username": "Youde1964"},
 {"id": 3, "name": "Justina D. Wallace", "phone": "914-819-0493", "birthday": "May 18, 1994", "email": "JustinaDWallace@rhyta.com", "username": "Donfe1994"},
 {"id": 4, "name": "Jason R. King", "phone": "608-562-1533", "birthday": "February 18, 1962", "email": "JasonRKing@dayrep.com", "username": "Ginusbact"},
 {"id": 5, "name": "Leroy T. Evans", "phone": "337-570-9574", "birthday": "January 7, 1946", "email": "LeroyTEvans@armyspy.com", "username": "Atiousaing"},
]


@app.route('/users')
def show_users():
    return render_template('users.html', users=USERS)


@app.route('/square', methods=['POST'])
def calculate_square():
    number = int(request.form['number'])
    square = number ** 2
    response = {
        'data': {
            'answer': square
        }
    }
    return response


@app.route('/users-list')
def get_users_list():
    format = request.args.get("format")

    if format == 'json':
        return USERS
    elif format == 'xml':
        xml_data = dicttoxml.dicttoxml(USERS)
        return Response(xml_data, mimetype='text/xml')
    else:
        return "Неподдерживаемый формат", 404


@app.route('/users-list-accept')
def show_users_list():
    accept_header = request.headers.get('Accept')

    if 'application/json' in accept_header:
        return USERS
    elif 'application/xml' in accept_header:
        xml_data = dicttoxml.dicttoxml(USERS)
        return Response(xml_data, mimetype='text/xml')
    else:
        return "Неподдерживаемый формат", 404


@app.route('/users', methods=['POST'])
def post_user():
    user = request.get_json()
    USERS.append(user)
    return user, 201


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_to_delete = None
    for user in USERS:
        if user.get('id') == user_id:
            user_to_delete = user
            break
    if user_to_delete:
        USERS.remove(user_to_delete)
        return "", 204
    else:
        return "Такого пользователя нет", 404


@app.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    for user in USERS:
        if user.get('id') == user_id:
            user.update(request.json)
            return user
    return "Такого пользователя нет", 404


if __name__ == '__main__':
    app.run(debug=True, port=9999)
