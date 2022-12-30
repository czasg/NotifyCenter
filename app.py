# coding: utf-8
import api
import pywss

from middleware.trace import trace
from middleware.jwt import auth


def swagger(app: pywss.App):
    app.openapi()
    app.get("/", lambda ctx: ctx.redirect("/docs"))


def main():
    app = pywss.App()
    app.openapi()
    app.get("/", lambda ctx: ctx.redirect("/docs"))
    app.use(trace, auth)
    api.register(app.party("/api"))
    app.run()


if __name__ == '__main__':
    main()
