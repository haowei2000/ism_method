import re
import string

from openai import OpenAI

from ism_method.config import get_config


def parse_method(text: str) -> list:
    methods = []
    pattern = r"^\d+[\.\:]\s*(.*?)(?=[：,，。\n]|$)"

    # 提取匹配的文本
    matches = re.findall(pattern, text, re.MULTILINE)
    # 输出匹配结果
    for match in matches:
        method = match.strip(string.punctuation)
        methods.append(method)
    return methods


def get_method(abstract: str):
    client = OpenAI(api_key="0", base_url=get_config()["api"]["url"])
    template = f"这是一篇论文的摘要，请提取其研究方法，按照1、2、3、的格式输出,每个方法用一个词语{abstract}"
    messages = [{"role": "user", "content": template}]
    result = client.chat.completions.create(
        messages=messages, model="ZhipuAI/glm-4-9b-chat-hf"
    )
    return parse_method(result.choices[0].message.content)

