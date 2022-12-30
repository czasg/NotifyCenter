# coding: utf-8
import pywss
import datetime

from db import Session
from db.model import Label
from infrastructure.http import Response


def register(app: pywss.App):
    app.view("/", LabelView())
    app.view("/{label.id}", LabelIdView())


class LabelView:

    @pywss.openapi.docs(
        summary="获取标签列表",
        tags=["标签管理"],
        params={
            "ps": (10, "page size"),
            "pn": (0, "page num"),
        },
    )
    def http_get(self, ctx: pywss.Context):
        resp = Response(data=[])
        ps = int(ctx.params.get("ps", 10))
        pn = int(ctx.params.get("pn", 0))
        with Session() as session, session.begin():
            for id, name, description, is_public, belong_to, created_time, updated_time in session.query(
                    Label.id,
                    Label.name,
                    Label.description,
                    Label.is_public,
                    Label.belong_to,
                    Label.created_time,
                    Label.updated_time). \
                    order_by(Label.id). \
                    limit(ps). \
                    offset(pn). \
                    all():
                resp.data.append({
                    "id": id,
                    "name": name,
                    "description": description,
                    "is_public": is_public,
                    "belong_to": belong_to,
                    "created_time": str(created_time),
                    "updated_time": str(updated_time),
                })
            ctx.write(resp)

    @pywss.openapi.docs(
        summary="新增标签类型",
        tags=["标签管理"],
        request={
            "name": "标签名字",
            "description": "标签描述",
        },
    )
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        req: dict = ctx.json()
        name = req.get("name")
        description = req.get("description")
        if not all((name, description)):
            resp.code = 40000
            resp.msg = "must provide an name & description"
            ctx.write(resp)
            return
        with Session() as session:
            if session.query(Label.id).filter(Label.name == name).count() > 0:
                resp.code = 40000
                resp.msg = f"label name[{name}] exists"
                ctx.write(resp)
                return
            label = Label(name=name, description=description, belong_to=2)
            session.add(label)
            session.commit()
            ctx.log.update(name=name).info("标签注册成功")
            ctx.write(resp)


class LabelIdView:

    @pywss.openapi.docs(
        summary="更新标签信息",
        tags=["标签管理"],
        request={
            "description": "标签描述",
            "is_public": (False, "是否公开"),
        },
    )
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        lid = ctx.paths.get("label.id")
        req: dict = ctx.json()

        with Session() as session:
            label = session.query(Label).filter(Label.id == lid).first()
            if not label:
                resp.code = 40000
                resp.msg = f"label not exists"
                ctx.write(resp)
                return
            description = req.get("description")
            if description:
                label.description = description
            is_public = req.get("is_public")
            if is_public is not None:
                label.is_public = is_public
            label.updated_time = datetime.datetime.now()
            session.commit()
            ctx.log.update(name=label.name).info("标签更新成功")
            ctx.write(resp)
