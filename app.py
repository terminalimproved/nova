import requests
import json
from PIL import Image
from io import BytesIO
import time
import threading
import os
from groq import Groq

# Banner title
title = """
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▀██░█▀▄▄▀█▀███▀█░▄▄▀████████░▄▄▀█░▄▄▀███░▄▄▀█▄░▄████░██░█░██░█░▄▄▀
██░█░█░█░██░██░▀░██░▀▀░███▄▄███░▀▀░█░██░███░▀▀░██░█████░▄▄░█░██░█░▄▄▀
██░██▄░██▄▄████▄███▄██▄████████░██░█▄██▄███░██░█▀░▀████░██░██▄▄▄█▄▄▄▄
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀                                                                                                                                   
                                                      """
print(title)
print("""
01 - Sailboat | A Powerful image generator      
02 - Opus | An AI text agent ready to generate text for you.
03 - Floyd | An AI music generator
04 - Type 'exit' to end the chat.
""")

# Function to display loading animation
def loading_animation(stop_event):
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print("Generating... " + animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
    print("Generating... Done!         ")

# Function to generate images using an API
def Sailboat():
    headers = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json'
    }
    prompt = input('Enter your image prompt: ')
    data = json.dumps({'inputs': prompt})
    
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    loading_thread.start()

    try:
        response = requests.post('https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev', 
                                 headers=headers, data=data)
        
        stop_event.set()
        loading_thread.join()
        
        if response.status_code == 200:
            try:
                image = Image.open(BytesIO(response.content))
                filename = f"{prompt}.png"
                image.save(filename)
                print(f'\nImage saved as {filename}')
            except Exception as e:
                print("\nFailed to process image:", e)
        else:
            print(f'\nError: {response.status_code} - {response.text}')
    except Exception as e:
        stop_event.set()
        loading_thread.join()
        print(f"\nError occurred: {e}")

# Function to generate text using Groq
def Opus():
    client = Groq(
        api_key="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",
    )
    
    prompt = input('Enter your text prompt: ')
    
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    loading_thread.start()

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )

        stop_event.set()
        loading_thread.join()

        generated_text = chat_completion.choices[0].message.content
        print(f'\nGenerated Text:\n{generated_text}')
        
    except Exception as e:
        stop_event.set()
        loading_thread.join()
        print(f"\nError occurred: {e}")

def Floyd():
    headers = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json'
    }
    prompt = input('Enter your music prompt: ')
    data = json.dumps({'inputs': prompt})
    
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    loading_thread.start()

    try:
        response = requests.post('https://api-inference.huggingface.co/models/facebook/musicgen-small',
                                 headers=headers, data=data)
        
        stop_event.set()
        loading_thread.join()

        if response.status_code == 200:
            try:
                audio = BytesIO(response.content)
                filename = f"{prompt}.wav"
                with open(filename, 'wb') as f:
                    f.write(audio.getbuffer())
                print(f'\nMusic saved as {filename}')
            except Exception as e:
                print("\nFailed to process music:", e)
        else:
            print(f'\nError: {response.status_code} - {response.text}')
    except Exception as e:
        stop_event.set()
        loading_thread.join()
        print(f"\nError occurred: {e}")


# Main chat loop
while True:
    useranswer = input("\nChoose an option (01 for Sailboat, 02 for Opus, 03 for Floyd, or 'exit' to quit): ")
    
    if useranswer == "01":
        Sailboat()
    elif useranswer == "02":
        Opus()
    elif useranswer == "03":
        Floyd()
    elif useranswer.lower() == "exit":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
