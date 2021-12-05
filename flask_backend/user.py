from flask import (
    Blueprint,
    jsonify,
    request,
    abort,
    Response,
    make_response
)
import json
import time
from sqlalchemy.sql.expression import null
from functools import wraps
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_refresh_cookies,
    decode_token,
    get_jti,
)
from flask_cors import cross_origin

from .medicine_proc.medicine import MedicineApp
from .models import MUser
from . import db

import cv2
cap = cv2.VideoCapture(1)

user = Blueprint('user', __name__)

@user.route('/test')
def test_view():
    return "<h1>Test</h1>"

@user.route('/sign-up', methods=['GET', 'POST'])
@cross_origin()
def sign_up():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        number = data['userName']
        password = data['password']

        user = MUser.query.filter_by(number=number).first()
        if user:
            error_message = 'This User is already exist!'
            return jsonify({
                'message' : error_message,
            }), 412
        else:
            token = ''
            new_user = MUser(number=number, name=number, password=password, token=token)
            db.session.add(new_user)
            db.session.commit()


            message = 'User registered successly!'
            return jsonify({
                'message': message,
            }), 201

@user.route('/login', methods=['GET', 'POST'])
@cross_origin()
def login():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        number = data['userName']
        password = data['password']

        user = MUser.query.filter_by(number=number).first()

        if user:
            if user.password == password:

                access_token = create_access_token(identity=number)
                refresh_token = create_refresh_token(identity=number)
                user.token = refresh_token
                db.session.commit()

                resp = make_response(jsonify({
                    'user': {
                        'id' : user.id,
                        'number' : user.number,
                    },
                    'auth' : True,
                    'refresh_token': refresh_token,
                    'access_token': access_token,
                    'message': 'Logged in successfully!',
                }), 200)

                resp.set_cookie(key="refresh_token", value=refresh_token, expires=time.time()+20*60)
                #set_refresh_cookies(resp, refresh_token)

                return resp
            else:

                resp = make_response(jsonify({
                    'message': 'Incorrect password, try again.',
                    'auth' : False,
                    'refresh_token': '',
                    'access_token': '',
                }), 401)

                return resp
        else:

            resp = make_response(jsonify({
                'message': 'User does not exist.',
                'auth' : False,
                'refresh_token': '',
                'access_token': '',
            }), 404)

            return resp


@user.route('/auth_user', methods=['GET'])
@jwt_required()
def auth_user():
    if request.method == 'GET':
        current_user = get_jwt_identity()

        if current_user:
            return jsonify({
                'user_name': current_user,
                'message': 'token is valid!'
            }), 200
        else:
            return jsonify({
                'error_message': 'token is invalid!'
            }), 401


@user.route('/delete/:id', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        data = json.loads(request.data)
        print(data)


@user.route('/refresh', methods=['POST'])
def refresh():
    decode_toke = decode_token(request.cookies['refresh_token'])

    current_user = decode_toke['sub']

    if int(time.time()) < decode_toke['exp'] :
        ret = jsonify({
            'access_token': create_access_token(identity=current_user)
        })

        return ret, 200

    else:
        return jsonify({
            'error_message': 'refresh token is invalid!'
        }), 401

@user.route('/get_pre', methods=['GET'])
@cross_origin()
def getPre():
    medicine = MedicineApp()
    pre_data = medicine.getPreReg()
    res = jsonify({
        'data': pre_data,
    })
    return res, 200

@user.route('/set_select_pre', methods=['POST'])
def setSelectPre():
    if request.method == 'POST':
        data = json.loads(request.data)

        medicine = MedicineApp()
        medicine.setSelectDict(data)

        return jsonify({
            'message': 'Server successly store selectData~',
        }), 201



@user.route('/get_med', methods=['GET'])
@cross_origin()
def getMed():
    medicine = MedicineApp()
    med_data = medicine.getMedReg(cap)
    res = jsonify({
        'data': med_data,
    })
    return res, 200


@user.route('/get_result', methods=['POST'])
def getResult():
    data = json.loads(request.data)



    if data['drug_dict'] != '' and data['select_dict'] != '':
        medicine = MedicineApp()
        result_data = medicine.compare(data['drug_dict'], data['select_dict'])

        print('/n/n/n/n')
        print(result_data)
        print('/n/n/n/n')

        res = jsonify({
            'data': result_data,
        })

        return res, 200
    else:
        res = jsonify({
            'error_message': 'Something Error!',
        })

    return res, 404






'''
def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing token!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token!'}), 403
        return func(*args, **kwargs)
    return wrapped
'''


