#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import random
import sys
import time

BASE_CHAT_URL = "https://api.dify.ai/v1/chat-messages"
BASE_COMPLETION_MESSAGE_URL = "https://api.dify.ai/v1/completion-messages"
CHAT_SECRET_KEY = "app-5yn5d8kUzMTPm8FoDt9UrUVh"
COMPLETION_SECRET_KEY = "app-QdE0Lro3gSwd0dPO1G32X0gG"
USER = "dify" + str(random.random())


def cursor_format_output(content):
    for char in content:
        print(char, end="", flush=True)
        time.sleep(0.1)


def send_chat_message(msg, conversation_id, type):
    data = {
        "inputs": {},
        "query": msg,
        "response_mode": "streaming",
        "conversation_id": conversation_id,
        "user": USER,
    }

    headers = {
        "Authorization": "Bearer " + CHAT_SECRET_KEY,
        "Content-Type": "application/json",
    }

    query_url = BASE_CHAT_URL


    if (type == 'completion'):
        query_url = BASE_COMPLETION_MESSAGE_URL
        headers = {
            "Authorization": "Bearer " + COMPLETION_SECRET_KEY,
            "Content-Type": "application/json",
        }

    response = requests.post(query_url, json=data, headers=headers, stream=True)

    conversation_id = ""
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")[6:]
            data = json.loads(decoded_line)
            if (type == 'chat'):
                conversation_id = data["conversation_id"]
            cursor_format_output(data["answer"])
    
    print("\n")
    print("=====================================================================================================")
    print("\n")
    return conversation_id


def chat_loop(conversation_id, type):
    while True:
        if type == 'chat':
            msg = input("有什么可以帮助你的吗: ")
        else:
            msg = input("有什么内容需要生成: ")    
        if msg == ":exit" or msg == ":quit" or msg == ":q":
            sys.exit(0)
        chat_loop(send_chat_message(msg, conversation_id, type), type)


if __name__ == "__main__":
    if (len(sys.argv) > 1 and sys.argv[1] == 'completion'):
        chat_loop(None, 'completion')
    else:
        chat_loop(None, 'chat')
