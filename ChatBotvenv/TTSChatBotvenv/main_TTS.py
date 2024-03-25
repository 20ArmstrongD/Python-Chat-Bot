#to activate the 


import json
from difflib import get_close_matches
from gtts import gTTS
import os
import platform

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent =2)

#function to find the best answer
#n has to do with the number of reponses it will return
#cutoff is for how acurate it will be so 0.6 = 60%
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) 
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("temp.mp3")
        
        if platform.system() == "Linux":
            os.system("aplay temp.mp3") #command for Linux 
        elif platform.system() == "Darwin":
            os.system("afplay temp.mp3") #command for Mac
        elif platform.system() == "Windows":
            os.system("start temp.mp3") #command for Windows
    except Exception as e:
        print(f"Error occurred during speech synthesis: {e}")


def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    
    while True:
        user_input: str = input('You: ')
        
        if user_input.lower() == 'quit':
            break
            
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
            speak(answer)
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')
            
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base) 
                print('Bot: Thank You! I learned a new response!')
                speak("Thank You! I learned a new response!")
            
    
if __name__ == '__main__':
    chat_bot()