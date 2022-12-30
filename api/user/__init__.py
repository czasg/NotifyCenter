# coding: utf-8
import pywss
import hashlib
import datetime

from db import Session
from db.model import User
from middleware.jwt import client
from infrastructure.http import Response


def register(app: pywss.App):
    app.view("/", UserView())
    app.view("/{user.id}", UserIdView())
    app.view("/login", LoginView())


class UserView:

    @pywss.openapi.docs(
        summary="获取用户列表",
        tags=["用户管理"],
        params={
            "ps": (10, "page size"),
            "pn": (0, "page num"),
        },
    )
    def http_get(self, ctx: pywss.Context):
        resp = Response(data=[])
        ps = int(ctx.params.get("ps", 10))
        pn = int(ctx.params.get("pn", 0))
        with Session() as session:
            for id, alias, username, created_time, updated_time in session.query(
                    User.id,
                    User.alias,
                    User.username,
                    User.created_time,
                    User.updated_time). \
                    order_by(User.id). \
                    limit(ps). \
                    offset(pn). \
                    all():
                resp.data.append({
                    "id": id,
                    "alias": alias,
                    "username": username,
                    "created_time": str(created_time),
                    "updated_time": str(updated_time),
                })
            ctx.write(resp)

    @pywss.openapi.docs(
        summary="注册新用户",
        tags=["用户管理"],
        request={
            "alias": "别名",
            "username": "用户姓名",
            "password": "用户密码",
        },
    )
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        req: dict = ctx.json()
        alias = req.get("alias")
        username = req.get("username")
        password = req.get("password")
        if not all((alias, username, password)):
            resp.code = 40000
            resp.msg = "must provide an alias & username & password"
            ctx.write(resp)
            return
        sha256 = hashlib.sha256()
        sha256.update(password.encode())
        password = sha256.hexdigest()
        with Session() as session:
            if session.query(User.id).filter(User.username == username).count() > 0:
                resp.code = 40000
                resp.msg = f"username[{username}] exists"
                ctx.write(resp)
                return
            user = User(alias=alias, username=username, password=password)
            session.add(user)
            session.commit()
            ctx.log.update(alias=alias).info("用户注册成功")
            ctx.write(resp)


class UserIdView:

    @pywss.openapi.docs(
        summary="修改用户信息",
        tags=["用户管理"],
        request={
            "alias": "别名",
        },
    )
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        req: dict = ctx.json()
        try:
            uid = int(ctx.paths.get("user.id"))
        except:
            resp.code = 40000
            resp.msg = "invalid user id"
            ctx.write(resp)
            return
        with Session() as session:
            user = session.query(User).filter(User.id == uid).first()
            if not user:
                resp.code = 40000
                resp.msg = f"user not exists"
                ctx.write(resp)
                return
            alias = req.get("alias")
            if alias:
                user.alias = alias
            user.updated_time = datetime.datetime.now()
            session.commit()
            ctx.log.update(alias=alias).info("用户更新成功")
            ctx.write(resp)


class LoginView:

    @pywss.openapi.docs(
        summary="用户登录",
        tags=["用户管理"],
        request={
            "username": "用户姓名",
            "password": "用户密码",
        },
    )
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        req: dict = ctx.json()
        username = req.get("username")
        password = req.get("password")
        sha256 = hashlib.sha256()
        sha256.update(password.encode())
        password = sha256.hexdigest()

        with Session() as session:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                resp.code = 40000
                resp.msg = f"user not exists"
                ctx.write(resp)
                return
            if user.password != password:
                resp.code = 40000
                resp.msg = f"password error"
                ctx.write(resp)
                return
            ctx.set_cookie("jwt_token", client.generate(user), maxAge=7200)
            ctx.log.update(username=username).info("用户登录成功")
            ctx.write(resp)
