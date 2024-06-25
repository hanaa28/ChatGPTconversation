from openai import OpenAI
from django.conf import settings
from openai import AssistantEventHandler

client = OpenAI(api_key=settings.API_KEY)

class EventHandler(AssistantEventHandler):
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

def send_code_to_api(messages):
    client = OpenAI(api_key=settings.API_KEY)
    
    assistant = client.beta.assistants.create(
        instructions="You are an helpful assistant.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o",
    )
    

    formatted_messages = [{"role": "user" if msg['user'] else "assistant", "content": msg['_input']} for msg in messages]
    
    thread = client.beta.threads.create(
        messages=formatted_messages
    )
    

    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="You are an helpful assistant.",
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()

   
    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
    )
    output = messages.data if messages.data else None
    if output:
        print(output[-1])
        for message in reversed(output):
            if message.role == 'assistant':
                return message.content
    return ""