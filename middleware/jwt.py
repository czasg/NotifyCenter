# coding: utf-8
import uuid
import time
import json
import pywss
import base64
import hashlib


def auth(ctx: pywss.Context):
    if ctx.route.endswith("/login"):
        ctx.next()
        return
    jwt_token = ctx.headers.get("Authorization", "")
    if not jwt_token:
        jwt_token = ctx.cookies.get("jwt_token", "").split(";", 1)[0]
    if not jwt_token:
        ctx.set_status_code(pywss.StatusForbidden)
        return
    if jwt_token.startswith(bearer):
        jwt_token = jwt_token[len(bearer):]
    payload, ok = client.verify(jwt_token)
    if not ok:
        ctx.set_status_code(pywss.StatusForbidden)
        return
    ctx.data.uid = payload.get("uid")
    ctx.data.username = payload.get("une")
    ctx.log = ctx.log.update(username=ctx.data.username)
    ctx.next()


class JWT:

    def __init__(self, secret: str):
        self.headers = {
            "alg": "HS256",
            "typ": "JWT",
        }
        self.headers_b64 = base64.b64encode(json.dumps(self.headers).encode()).decode()
        self.secret = secret

    def verify(self, token: str) -> (dict, bool):
        h, p, s = token.split(".")
        headers: dict = json.loads(base64.b64decode(h.encode()).decode())
        payload: dict = json.loads(base64.b64decode(p.encode()).decode())

        if headers.get("alg") != "HS256":
            return payload, False,

        if payload.get("exp", 0) < time.time():
            return payload, False,

        sha256 = hashlib.sha256()
        sha256.update((h + p).encode())
        sha256.update(self.secret.encode())
        if sha256.hexdigest() != s:
            return payload, False,

        return payload, True

    def generate(self, user):
        payload = {
            "uid": user.id,
            "une": user.username,
            "exp": int(time.time()) + 7200,
        }
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode()

        sha256 = hashlib.sha256()
        sha256.update((self.headers_b64 + payload_b64).encode())
        sha256.update(self.secret.encode())
        sign = sha256.hexdigest()
        return f"{self.headers_b64}.{payload_b64}.{sign}"


bearer = "Bearer "
client = JWT(str(uuid.uuid4()))
