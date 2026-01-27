import asyncio
import json
import random
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI(title="Mock OpenAI API")

MOCK_RESPONSES = [
    "I understand your question. Based on my knowledge, here's what I can tell you about that topic.",
    "That's an interesting question! Let me break it down for you.",
    "Thanks for asking! Here's my perspective on this matter.",
    "Great question! The answer depends on several variables.",
    "I'd be happy to help with that. Here are the main points.",
]

MIN_LATENCY = 0.3
MAX_LATENCY = 1.5


async def stream_response(total_latency: float):
    response_text = random.choice(MOCK_RESPONSES)
    words = response_text.split()
    chunk_delay = total_latency / len(words)

    for word in words:
        await asyncio.sleep(chunk_delay)
        chunk = {
            "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "gpt-4-mock",
            "choices": [
                {"index": 0, "delta": {"content": word + " "}, "finish_reason": None}
            ],
        }
        yield f"data: {json.dumps(chunk)}\n\n"

    final_chunk = {
        "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": "gpt-4-mock",
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
    }
    yield f"data: {json.dumps(final_chunk)}\n\n"
    yield "data: [DONE]\n\n"


def create_completion_response():
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "gpt-4-mock",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": random.choice(MOCK_RESPONSES),
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 50, "completion_tokens": 100, "total_tokens": 150},
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    stream = body.get("stream", False)
    latency = random.uniform(MIN_LATENCY, MAX_LATENCY)

    if stream:
        return StreamingResponse(
            stream_response(latency), media_type="text/event-stream"
        )
    else:
        await asyncio.sleep(latency)
        return create_completion_response()


"""
Mock OpenAI API Server for Load Testing

Mimics OpenAI's chat completions API with simulated latency.
Run with: uvicorn tests.loadtest.mock_openai_server:app --host 0.0.0.0 --port 8100
"""

import asyncio
import json
import random
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI(title="Mock OpenAI API")

MOCK_RESPONSES = [
    "I understand your question. Based on my knowledge, here's what I can tell you about that topic.",
    "That's an interesting question! Let me break it down for you.",
    "Thanks for asking! Here's my perspective on this matter.",
    "Great question! The answer depends on several variables.",
    "I'd be happy to help with that. Here are the main points.",
]

MIN_LATENCY = 0.3
MAX_LATENCY = 1.5


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    stream = body.get("stream", False)
    latency = random.uniform(MIN_LATENCY, MAX_LATENCY)

    if stream:
        return StreamingResponse(
            stream_response(latency), media_type="text/event-stream"
        )
    else:
        await asyncio.sleep(latency)
        return create_completion_response()


async def stream_response(total_latency: float):
    response_text = random.choice(MOCK_RESPONSES)
    words = response_text.split()
    chunk_delay = total_latency / len(words)

    for word in words:
        await asyncio.sleep(chunk_delay)
        chunk = {
            "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "gpt-4-mock",
            "choices": [
                {"index": 0, "delta": {"content": word + " "}, "finish_reason": None}
            ],
        }
        yield f"data: {json.dumps(chunk)}\n\n"

    final_chunk = {
        "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": "gpt-4-mock",
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
    }
    yield f"data: {json.dumps(final_chunk)}\n\n"
    yield "data: [DONE]\n\n"


def create_completion_response():
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "gpt-4-mock",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": random.choice(MOCK_RESPONSES),
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 50, "completion_tokens": 100, "total_tokens": 150},
    }


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [{"id": "gpt-4-mock", "object": "model", "owned_by": "mock"}],
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "mock": True}
