from flask import Blueprint, jsonify, request
from data import db_session
from data.users import User

blueprint = Blueprint('users_api', __name__,
                      template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                    'speciality', 'address', 'email'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                       'speciality', 'address', 'email'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(User).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['position']
    )
    user.set_password(request.json['password'])
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['GET', 'POST'])
def transform_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    for key in ['id', 'surname', 'name', 'age', 'position',
                'speciality', 'address', 'email', 'password']:
        if key in request.json.keys():
            if key == 'password':
                user.set_password(request.json['password'])
                continue
            print('user.{}={}'.format(key, request.json[key]))
            exec('user.{}="{}"'.format(key, request.json[key]))
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})
