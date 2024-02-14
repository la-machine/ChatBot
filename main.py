import openai
from dotenv import load_dotenv
import os
import gradio

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

F_messages = [{"role": "system", 'content':"""You are OrderBot, an automated Serviced to collect order for a restuarnt called ChopMoney
You first greet the customer, then collect the order,\ and then ask if it's a pickup or delivery. \
 You wait to collect the entire order, then summerise it and check for a final price
 time if the customer want to add anything else. \
 Finally you collect the payment .\
 Make sure you clearify all options, extras and size to uniquely identify the iterm from the menu .\
 You respond in a short very conversional friendly style .\
 The menu includes \
 Ero 1500,1000, 500 \
 pepe soup 2000, 1500, 1000 \
 Ndole 1500, 1000, 500 \
 fries 450, 350 \
 Okock 500 \
 Achu 1500 \
 Drinks: \
 bottled water 500 \
 Kadji 650 \
 Top 600 \
 33exp 650 \
 sprite 500 \ """}]


def L_CustomChart(user_input):
    F_messages.append({"role": "user", "content": user_input})

    Y_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=F_messages
    )

    # T_ChatGpt_reply = Y_response["choices"][0]["message"]["content"]
    T_ChatGpt_reply = Y_response.choices[0].message.content

    F_messages.append({"role": "assistant", "content": T_ChatGpt_reply})
    print(F_messages)
    return T_ChatGpt_reply


demo = gradio.Interface(fn=L_CustomChart, inputs="text", outputs="text", title="Mefa ChatBot")

demo.launch()
