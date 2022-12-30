# coding: utf-8
import uuid
import pywss


def trace(ctx: pywss.Context):
    ctx.data.trace_id = ctx.headers.get("X-Trace-Id", str(uuid.uuid4()))
    ctx.set_header("X-Trace-Id", ctx.data.trace_id)
    ctx.log = ctx.log.update(trace=ctx.data.trace_id)
    ctx.next()
