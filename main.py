from fastapi import FastAPI
from app.llm import LLM
from app.reponse_models import AIResponseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse


app = FastAPI(title="My FastAPI Project", version="1.0.0")


@app.get("/")
def health_check():
    return {"status": "healthy", "python_version": "3.11"}


@app.get("/ai")
def health_check(text: str = "") -> AIResponseModel: 

    llm = LLM()
    response = llm.generate_response(text)

    return response

@app.get("/stream")
async def stream_endpoint(text: str = ""):
  if not text:
    raise HTTPException(status_code=400, detail="Text cannot be empty")

  llm = LLM()

  async def event_generator():
    # 1. Initialize variables to prevent NameError
    reasoning_content = ""
    final_output_content = ""

    try:
      # Await the stream creation, then use async for to iterate
      stream = await llm.send_stream(text)
      async for event in stream:

        # 1. Handle lifecycle events
        if event.type == "response.created":
          yield f"data: [SESSION_STARTED] ID: {event.response.id}\n\n"

        # 2. Handle internal reasoning / thinking deltas
        elif event.type == "response.reasoning_text.delta":
          reasoning_content += event.delta
          # Send reasoning delta to the client (or omit if hidden)
          yield f"data: {event.delta}\n\n"

        # 3. Handle final user-facing text deltas
        elif event.type == "response.output_text.delta":
          final_output_content += event.delta
          # Send final text chunk to the client
          yield f"data: {event.delta}\n\n"

        # 4. Handle completion and final usage metadata
        elif event.type == "response.completed":
          usage = event.response.usage
          yield f"data: [DONE] Tokens - Input: {usage.input_tokens}, Output: {usage.output_tokens}\n\n"

        # 5. Handle errors
        elif event.type == "error":
          yield f"data: [ERROR] {event.message}\n\n"

    except Exception as e:
      yield f"data: [ERROR] {str(e)}\n\n"

  return StreamingResponse(event_generator(), media_type="text/event-stream")
