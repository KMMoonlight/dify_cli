#!/usr/bin/env python3
import requests
import json
import random
import sys
import time

BASE_CHAT_URL = "https://api.dify.ai/v1/chat-messages"
SECRET_KEY = "app-5yn5d8kUzMTPm8FoDt9UrUVh"
USER = "dify" + str(random.random())


def cursor_format_output(content):
    for char in content:
        print(char, end="", flush=True)
        time.sleep(0.1)


def send_chat_message(msg, conversation_id, user):
    data = {
        "inputs": {},
        "query": msg,
        "response_mode": "streaming",
        "conversation_id": conversation_id,
        "user": user,
    }

    headers = {
        "Authorization": "Bearer " + SECRET_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(BASE_CHAT_URL, json=data, headers=headers, stream=True)

    conversation_id = ""
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")[6:]
            data = json.loads(decoded_line)
            conversation_id = data["conversation_id"]
            cursor_format_output(data["answer"])
            
    print("\n")
    print("=====================================================================================================")
    print("\n")

    return conversation_id


def chat_loop(conversation_id):
    while True:
        msg = input("Any Question: ")
        if msg == ":exit" or msg == ":quit" or msg == ":q":
            sys.exit(0)
        chat_loop(send_chat_message(msg, conversation_id, "qjh123"))


if __name__ == "__main__":
    chat_loop(None)
