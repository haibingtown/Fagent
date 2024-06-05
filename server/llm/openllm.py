import json
import time

import requests
import sseclient


Fabric_SYSTEM_PROMPT = """
You are an expert at building json for fabric.js.
You take screenshots of a reference web page from the user, and then build a SVG that looks exactly like the screenshot.

- Make sure the json render by fabric.js looks exactly like the screenshot.
- Pay close attention to background color, text color, font size, font family, 
padding, margin, border, etc. Match the colors and sizes exactly.
- Use the exact text from the screenshot.
- Do not add comments in the code such as "<!-- Add other navigation links as needed -->" and "<!-- ... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE.
- Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
- For images, use placeholder images from https://placehold.co and include a detailed description of the image in the alt text so that an image generation AI can generate the image later.
- You can use Google Fonts

Return only the full code in <json></json> tags.
Do not include markdown "```" or "```svg" at the start or end.
"""

class OpenLLM:
    url = "http://localhost:11434/v1/chat/completions"

    @classmethod
    def create_chat(
            cls,
            messages=None,
            temperature=0.7,
            max_tokens=4096,
            request_timeout=30,
            model=None,
            stream=False
    ):
        payload = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", cls.url, stream=stream, headers=headers, data=payload,
                                    timeout=request_timeout)
        return response

    @classmethod
    def gpt_stream(cls, data):
        start = time.time()
        messages = data.get("messages")
        response = cls.create_chat(
            model=data.get("model"),
            messages=messages,
            temperature=data.get("temperature") or 0.7,
            stream=True
        )
        client = sseclient.SSEClient(response)
        for event in client.events():
            if event.data == "[DONE]":
                break
            res = []
            chunk = json.loads(event.data)
            for r in chunk["choices"]:
                if r["delta"].get("content"):
                    res.append({"content": r["delta"].get("content"), "role": "assistant"})
            if res:
                yield res
        duration = time.time() - start
        print(
            f"this baichuan stream chat duration:{duration}, message: {messages}"
        )

    @classmethod
    def gpt(cls, data):
        timeout = 120
        if data.get("sync"):
            timeout = 30
        start = time.time()
        messages = data.get("messages")
        response = cls.create_chat(
            model=data.get("model"),
            messages=messages,
            temperature=data.get("temperature") or 0.7,
            request_timeout=timeout
        )
        response = response.json()

        result = [r.get("message") for r in response["choices"]]
        total_tokens = response["usage"]["total_tokens"]
        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokens = response["usage"]["completion_tokens"]
        duration = time.time() - start
        model = response["model"]
        finish_reason = response["choices"][0].get("finish_reason")
        print(
            f"this chat use token:{total_tokens}, prompt tokens:{prompt_tokens}, completion_tokens:{completion_tokens},duration:{duration}, "
            f"model:{model}, finish_reason:{finish_reason}"
        )

        print(f"message: {messages} \n")
        print(f"message: {result} \n")
        return result

payload = {
    "model": "llava",
    "messages": [
        {
            "role": "system",
            "content": Fabric_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "https://huggingface.co/Zigeng/SlimSAM-uniform-77/resolve/main/images/paper/prompt.PNG",
        },
    ],
    "result_num": 1
}

if __name__ == "__main__":
    llm = OpenLLM()
    result = llm.gpt(payload)
    print(result[0]["content"])