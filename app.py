import os

import httpx
from sanic import Request, Sanic
from sanic.response import ResponseStream, HTTPResponse

HOST = os.getenv("HOST", "::")
PORT = int(os.getenv("PORT", 8000))
PROXY_URL = os.getenv("PROXY_URL", None)
URL = os.getenv("TARGET_URL", "https://api.groq.com/openai/v1/chat/completions")
TIMEOUT = int(os.getenv("TIMEOUT", 60))

app = Sanic("GroqProxy")
client = httpx.AsyncClient(proxy=PROXY_URL, timeout=TIMEOUT)


@app.post("v1/chat/completions")
async def completions(request: Request):
    headers = {"Content-Type": "application/json"}
    if auth := request.headers.get("Authorization"):
        headers["Authorization"] = auth

    if request.json.get("stream", False):

        async def _streaming_fn(response):
            async with client.stream("POST", URL, headers=headers, json=request.body) as resp:
                async for chunk in resp.aiter_bytes():
                    await response.write(chunk)

        return ResponseStream(streaming_fn=_streaming_fn, content_type="text/event-stream")

    return HTTPResponse(
        body=(await client.post(URL, headers=headers, data=request.body)).content,
        content_type="application/json",
    )


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, single_process=True, debug=True)
