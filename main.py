import json, os
import re

import panel as pn
import openai
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, select
import tables
import docx2txt
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

pn.extension()
openai.api_key = ""
panels = []

engine = create_engine(f"postgresql+psycopg2://postgres:root@localhost:5432/chatbot")
if not database_exists(engine.url):
    create_database(engine.url)
tables.metadata.create_all(bind=engine, checkfirst=True)

def save_process_activity(activity):
    with engine.connect() as connection:
        new_activity = {k: v for k, v in activity.__dict__.items() if k != '_sa_instance_state'}
        stmt = tables.Procese_Activity.__table__.insert().values(new_activity)
        try:
            connection.execute(stmt)
            connection.commit()
            print("Activity saved successfully.")
        except Exception as e:
            print("Error saving activity:", e)


def save_component(component):
    with engine.connect() as connection:
        new_component = {k: v for k, v in component.__dict__.items() if k != '_sa_instance_state'}
        stmt = tables.Component.__table__.insert().values(new_component)
        try:
            connection.execute(stmt)
            connection.commit()
            print("Component saved successfully.")
        except Exception as e:
            print("Error saving component:", e)


def save_supplier(supplier):
    with engine.connect() as connection:
        new_supplier_data = {k: v for k, v in supplier.__dict__.items() if k != '_sa_instance_state'}
        stmt = tables.Supplier.__table__.insert().values(new_supplier_data)
        try:
            connection.execute(stmt)
            connection.commit()
            print("Supplier saved successfully.")
        except Exception as e:
            print("Error saving supplier:", e)

def save_employee(employee):
    with engine.connect() as connection:
        new_employee_data = {k: v for k, v in employee.__dict__.items() if k != '_sa_instance_state'}
        stmt = tables.Employee.__table__.insert().values(new_employee_data)
        try:
            connection.execute(stmt)
            connection.commit()
            print("Employee saved successfully.")
        except Exception as e:
            print("Error saving employee:", e)


def getActivities():
    with engine.connect() as connection:
        query = tables.Procese_Activity.__table__.select()
        result = connection.execute(query)
        data = {}
        for row in result:
            key = row.label
            value = row.number
            data[key] = value
        print(data)
        return data


def fetch_Activity_By_Number(number):
    with engine.connect() as connection:
        query = tables.Component.__table__.select().where(tables.Component.id_procese_activity == number)
        result = connection.execute(query)
        data = result.fetchall()
        print(data)
        return data

def fetch_Activity_Number(activity):
    data = getActivities()
    if activity in data:
        print(data.values())
    return 1

def update_Component(activity, new_value, record):
    print(activity)
    number = fetch_Activity_Number(activity)
    match record:
        case "Application / Storage":
            record = "app"
        case "Process Manager":
            record = "process_manager"
        case "information":
            record = "information"
        case "purpose":
            record = "purpose"
        case _:
            print(f"Invalid record: {record}")
    with engine.connect() as connection:
        query = tables.Component.__table__.update().where(tables.Component.id_procese_activity == number).values(**{record: new_value})
        result = connection.execute(query)
        connection.commit()
    
F_messages = [{"role": "system", "content":f"You are ChatBot, an automated Serviced to collect informations for an enterprise"
f"you first greate the user and the present a numerated list of what he can do on the system as shown bellow"
f"Welcome to the data management system! I am here to help you record and update your processing activities. "
f"The following activities have already been assigned to you:{getActivities()}"
f"Please simply enter the appropriate number with which you would like to start updating the processing activities."
f"After choosing its option you summarise what he has choose. Always say you have selected... then the option he has choose"
f"You then move on and present what is present conserning his options he has chose and ask if everything is ok or he wish to change something"
f"eg. Asuming he has choose 1, You have selected Correspondence & Invoices. I have the following information about this:"
f"Process manager: ..."
f"Application / Storage: ..."
f"Information object: ..."
f"Purpose: ..."            
f"After presenting what you have about his option he has choose You then ask Is this information still correct or have there been any changes?"
f"You then summarise the update that was make as shown bellow"
f"Thank you for the update. I have now recorded that the Application / Storage for Correspondence & Invoices is Open Office.That is Application:Open Office"}]


# F_messages = [{"role": "system", "content": """You are ChatBot, an automated Serviced to collect informations for an enterprise
# The user will first have to send the name of his enterprise then the all the informations he will enter or request for should belong
# to that enterprise. He shouldn't be able to access the informations of another enterprise (eg if he request for all the informations
# entered he should only see those for his enterprise only.) After sending the enterprise name, \
# You then greet the customer, then collect the service he wish to do,\ and then ask the detail information relative to that service. \
#  You will present all the information the user is to enter and then progessively ask him those information one after the other
#   (eg if he is to enter the fuulname, email, contact, etc you first ask him his fullname, after submiting his full name you then ask the others) \
#  You wait to collect the entire informations, then summerise it and check for a final confirmation \
#  and the summarised information for both supplier and employee shouild not be numerated nor have hiphen \
#  time if the customer want to add anything else. \
#  This are the details you are to collect to register a supplier: \
#  Supplier_Name \
#  Contact Name \
#  Email \
#  Phone Number \
#  Address \
#  Products_Services_Provided \
#  And these are that of an employee: \
#  Name
#  Email
#  Phone Number
#  Address
#  Department
#  Position
#  Salary
#  Hire Date
#  Each time you present the summary always use the phrase (Here is a summary of the details) \
#  And when presenting the summary details the attribut name should be seperated with _ not space (e.g Supplier Name: FLYT should be Supplier_Name: FLYT \
#  Finally you collect the payment .\
#  Make sure you clearify all options, extras and size to uniquely identify the iterm from the menu .\
#  You respond in a short very conversional friendly style .\
#  The service includes \
#  Register Employee \
#  Register Supplier \  """}]

inp = pn.widgets.TextInput(value='Hi', placeholder='Enter your message')

# title = pn.widgets.StaticText(value='MEFA ChatBot')
button_conversation = pn.widgets.Button(name='Submit')

con = engine.connect()

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

    # procese_data = getActivities()

    if "You have selected" in response:
        print("Testing the condiction")
        component = fetch_Activity_By_Number(prompt)
        F_messages.append({'role': 'assistant', 'content': f"{component}"})
        F_messages.append({'role': 'assistant', 'content':'What are the information that is present so far'})
        response = get_completion_from_messages(F_messages)
        print(response)

    if "Thank you for the update" in response:
        print("\n Checking if condiction was true")
        getData(response)

    user_row = pn.Row('<b>User:</b>', pn.pane.Markdown(prompt, width=600))
    assistant_row = pn.Row('<b>Assistant:</b>', pn.pane.Markdown(response, width=600))
    user_row[0].css_classes.append('user-label')
    assistant_row[0].css_classes.append('assistant-label')
    panels.extend([user_row, assistant_row])
    if "Here is a summary of the details" in response:
        summary_text = response.split("Here is a summary of the details:")[1].strip()
        print(response)
        response_json = convertToJson(summary_text)
        data = json.loads(response_json)

        if 'Supplier_Name' in response:
            new_supplier = tables.Supplier(
                name=data.get('Supplier_Name'),
                contact_name=data.get('Contact_Name'),
                email=data.get('Email'),
                phone_number=data.get('Phone_Number'),
                address=data.get('Address'),
                products_services_provided=data.get('Products_Services_Provided')
            )
            save_supplier(new_supplier)

        else:
            employee = tables.Employee(name=data.get('Name'),
                                       email=data.get('Email'),
                                       phone_number=data.get('Phone Number'),
                                       address=data.get('Address'),
                                       department=data.get('Department'),
                                       position=data.get('Position'),
                                       salary=data.get('Salary'),
                                       hire_date=data.get('Hire Date'),
                                     )
                                # termination_date=data.get('Termination Date'))
            save_employee(employee)
    return pn.Column(*panels)

def convertToJson(summary_text):
    summary_dict = {}
    for line in summary_text.strip().split("\n"):
        parts = line.split(": ", 1)
        if len(parts) == 2:
            key, value = parts
            summary_dict[key.strip()] = value.strip()

    # Convert the dictionary to JSON
    summary_json = json.dumps(summary_dict, indent=4)
    print(summary_json)
    return summary_json;

def getData(content):
    pattern = r"I have now recorded that the (.+?) for (.+?) is (.+?)\."
    match = re.search(pattern, content)

    if match:
        record = match.group(1)
        table = match.group(2)
        value = match.group(3)
        update_Component(table, value, record)
        print(f"Record: {record}, Table: {table}, Value: {value}")
    else:
        print("No match found.")

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