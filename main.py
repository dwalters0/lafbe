from call_llm import generate

from lxml import etree

import base64

from configuration import get_config

from call_codex import auth_codex








def print_hi():
    generate("Hi My name is Dan, What is yours?",True)

def load_burp_file():
    with open("burp.xml") as f:
        root = etree.parse(f)

    return root
    # for item in root.xpath("//item"):
    #     print(item.findtext("url"))
    #     print(item.findtext("method"))
    #     print(item.findtext("request"))
    #     print(item.findtext("response"))

def format_for_LLM(burp_data):
    items = []
    for item in burp_data.xpath("//item"):
        decoded_request = base64.b64decode(item.findtext("request")).decode("utf-8")
        decoded_response = base64.b64decode(item.findtext("response")).decode("utf-8")
        ret = ""
        ret += "REQUEST/RESPONSE START\n"
        ret += f"URL: {item.findtext("url")}\n"
        ret += f"Method: {item.findtext("method")}\n"
        ret += f"Request (Base64): {decoded_request}\n"
        ret += f"Response (Base64): {decoded_response}\n"
        ret += "REQUEST/RESPONSE END\n"
        items.append(ret)
    return items

def get_llm_to_analyse(items):

    for item in items:
        prompt = f"""
        You are assisting a penetration tester on an authorised penetration test.
        The following traffic has been captured during normal browsing.
        Analyse the request and response and note anything that could contain a vulnerability.
        If there's nothing noteworthy, reply with "It's all good in the hood". 
        The request is as follows:
        {item}
        """
        generate(prompt,True)
        input("Press Enter to continue...")

if __name__ == '__main__':
    config = get_config()
    if config.use_codex:
        auth_codex()
    burp_data = load_burp_file()
    LLM_request_items = format_for_LLM(burp_data)
    get_llm_to_analyse(LLM_request_items)

