import os
import panel as pn
import openai
from dotenv import load_dotenv

load_dotenv()

pn.extension()
openai.api_key = os.getenv("OPENAI_API_KEY")
panels = []

F_messages = [{"role": "system", "content": """You are OrderBot, an automated Serviced to collect order for a restuarnt called ChopMoney
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

inp = pn.widgets.TextInput(value='Hi', placeholder='Enter your message')

# title = pn.widgets.StaticText(value='MEFA ChatBot')
button_conversation = pn.widgets.Button(name='Submit')

def get_completion_from_messages(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

def collect_messages(_):
    prompt = inp.value_input
    inp.value=''
    F_messages.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(F_messages)
    F_messages.append({'role':'assistant', 'content':f"{response}"})
    user_row = pn.Row('<b>User:</b>', pn.pane.Markdown(prompt, width=600))
    assistant_row = pn.Row('<b>Assistant:</b>', pn.pane.Markdown(response, width=600))
    user_row[0].css_classes.append('user-label')
    assistant_row[0].css_classes.append('assistant-label')
    panels.extend([user_row, assistant_row])
    return pn.Column(*panels)

interactive_conversation = pn.bind(collect_messages, button_conversation)

custom_style = {
        "border": "1px solid #ccc",
        "padding": "10px",
        "overflow": "auto",
        "max-height": "500px",  # Adjust as needed
}
output_panel = pn.panel(interactive_conversation,styles=custom_style, loading_indicator=True)

pn.config.raw_css.append('.user-label { color: blue; }')
pn.config.raw_css.append('.assistant-label { color: red; }')

title = pn.widgets.StaticText(value='<h1>MEFA ChatBot</h1>', align='center')

dashboard = pn.Column(
    title,
    output_panel,
    pn.Row( inp, button_conversation)

)

dashboard.servable()
pn.serve(dashboard)