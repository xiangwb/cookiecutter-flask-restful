from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

import mongoengine as mg
from {{cookiecutter.app_name}}.models import User
from {{cookiecutter.app_name}}.extensions import ma
from {{cookiecutter.app_name}}.commons.pagination import Pagination


class UserSchema(ma.Schema):
    id = ma.String(dump_only=True)
    password = ma.String(load_only=True, required=True)
    username = ma.String(required=True)


class UserResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user: UserSchema
        404:
          description: user does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user deleted
        404:
          description: user does not exists
    """

    method_decorators = [jwt_required]

    def get(self, user_id):
        schema = UserSchema()
        try:
            user = User.objects.get(user_id)
            return {"user": schema.dump(user)}
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            abort(401, {'msg': '用户不存在'})

    def put(self, user_id):
        schema = UserSchema(partial=True)
        try:
            user = User.objects.get(user_id)
            user = schema.load(request.json, instance=user)
            user.update(**user)
            return {"msg": "user updated", "user": schema.dump(user)}
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            abort(401, {'msg': '用户不存在'})

    def delete(self, user_id):
        try:
            User.objects.get(user_id).delete()
            return {"msg": "user deleted"}
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            abort(401, {'msg': '用户不存在'})


class UserList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user: UserSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = UserSchema(many=True)
        query = User.objects.all()
        objs, page = Pagination(query).paginate(schema)
        return {'response': objs, 'page': page}

    def post(self):
        schema = UserSchema()
        data = schema.load(request.json)
        user = User.objects.create(**data)
        return {"msg": "user created", "user": schema.dump(user)}, 201
