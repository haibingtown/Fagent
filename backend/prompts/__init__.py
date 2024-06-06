from typing import List, NoReturn, Union

from openai.types.chat import ChatCompletionMessageParam, ChatCompletionContentPartParam

from prompts.imported_code_prompts import IMPORTED_CODE_SYSTEM_PROMPTS
from prompts.screenshot_system_prompts import SYSTEM_PROMPTS, Fabric_SYSTEM_PROMPT
from prompts.types import Stack


USER_PROMPT = """
拆解图层，逐层生成 fabric.js 能渲染的 json 内容，使得最后 canvas 渲染后与图片一致
"""

SVG_USER_PROMPT = """
拆解图层，逐层生成 fabric.js 能渲染的 json 内容，使得最后 canvas 渲染后与图片一致
"""


def assemble_imported_code_prompt(
    code: str, stack: Stack, result_image_data_url: Union[str, None] = None
) -> List[ChatCompletionMessageParam]:
    system_content = IMPORTED_CODE_SYSTEM_PROMPTS[stack]

    user_content = (
        "Here is the code of the app: " + code
        if stack != "svg"
        else "Here is the code of the SVG: " + code
    )
    return [
        {
            "role": "system",
            "content": system_content,
        },
        {
            "role": "user",
            "content": user_content,
        },
    ]
    # TODO: Use result_image_data_url


def assemble_prompt(
    image_data_url: str,
    stack: Stack,
    result_image_data_url: Union[str, None] = None,
) -> List[ChatCompletionMessageParam]:
    system_content = Fabric_SYSTEM_PROMPT
    user_prompt = USER_PROMPT if stack != "svg" else SVG_USER_PROMPT

    user_content: List[ChatCompletionContentPartParam] = [
        {
            # "type": "image_url",
            # "image_url": {"url": image_data_url, "detail": "high"},
            "image": "https://img.alicdn.com/bao/uploaded/i1/2833669746/O1CN01lvLZNc2LrinthPm60_!!2833669746.jpg"
        },
        {
            # "type": "text",
            "text": user_prompt
        },
    ]

    # Include the result image if it exists
    if result_image_data_url:
        user_content.insert(
            1,
            {
                "type": "image_url",
                "image_url": {"url": result_image_data_url, "detail": "high"},
            },
        )
    return [
        {
            "role": "system",
            "content": [
                {"text": system_content}
            ],
        },
        {
            "role": "user",
            "content": user_content,
        },
    ]
