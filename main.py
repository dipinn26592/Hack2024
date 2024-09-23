import speech_recognition as sr
import os
from openai import AzureOpenAI
import json
import pyttsx3
import requests
import pyautogui
import base64

API_KEY = "d3fb83ffdac94fe4a6d172fb364847f6"
ENDPOINT = "https://frjyhgfuyre.openai.azure.com/openai/deployments/gpt4/chat/completions?api-version=2024-02-15-preview"
IMAGE_PATH = "screenshot.png"
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1)


def listenForUserInput():
    print("----listening----")
    with sr.Microphone() as source:
        try:
            audio_data = recognizer.listen(source, timeout=3)
            text = recognizer.recognize_google(audio_data)
        except  Exception as e:
            text = "blank"
        return text

def getAzureOpenAIPromptResponse(userPrompt):
    encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
    
    print("----gettingResponse----")
    sys_msg = (
        'You are a multi-modal AI voice assistant. Your name is Onmibot. Your user may or may not have attached a photo for context'
        'Generate a response but exclude al asterisks (*) from the output to ensure compatibility with text-to-speech'
        'Do not expect or request images, just use the context if added.'
        'Use all the context of this conversations so your response is relevant to the conversation. Make'
        'your responses clear and concise, avoiding any verbosity.'
    )
    x = [
        {
            "type": "text",
            "text": "You are an AI assistant that helps admins with queries related to various Microsoft Products, tailor your responses in that tone. Also a screenshot will be provided with the issue or question that the admin will ask, refer to screenshot as currentScreen"
        },
        {
            "type": "text",
            "text" : "Only when the prompt has some referece to the screen, screenshot or what i am i working ok, screenshot function should be called, when the prompt is for generic conversation like HI, how are you. Give a enthusiastic response."
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{encoded_image}"
            }
        },
        {
            "type": "text",
            "text" : "limit your response to maximum 200 words *important*"
        },
        {
            "type": "text",
            "text" : "Make it conversational, dont give any bulleted responses, like 1, 2 etc. also response should be in plaintext and should not have any bold or similar formatting"
        }
    ]
    x.extend(userPrompt)

    if True:
         payload = {
            "messages": [
                {
                "role": "user",
                "content": x
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    res =  (response.json())
    # convert to object
    res = res['choices'][0]['message']['content']
    return res

def copilot(): 
    engine.say("Hello, How can i Help")
    engine.runAndWait() 
    context = []
    while True:
        prompt = listenForUserInput()
        print("================")
        print("USER : "+prompt)
        print("================")
        context.append({
            "type":"text",
            "text": prompt
        },)
        screenshot = pyautogui.screenshot()
        screenshot.save(IMAGE_PATH)
        if len(prompt) > 10:
            AiResponse = getAzureOpenAIPromptResponse(context)
            print("================")
            print("COPILOT : "+AiResponse)
            print("================")
            engine.say(AiResponse)
            engine.runAndWait()
