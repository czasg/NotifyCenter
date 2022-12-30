# coding: utf-8
import pywss


def register(app: pywss.App):
    app.view("/", NotifyView())
    app.view("/{user.id}", NotifyView())


class NotifyView:

    @pywss.openapi.docs(
        summary="获取通知列表",
        tags=["通知管理"],
        params={
            "ps": (10, "page size"),
            "pn": (0, "page num"),
        },
    )
    def http_get(self, ctx: pywss.Context):
        pass

    @pywss.openapi.docs(
        summary="新增通知列表",
        tags=["通知管理"],
    )
    def http_post(self, ctx: pywss.Context):
        pass
