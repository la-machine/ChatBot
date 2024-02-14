# ChopMoney OrderBot Panel App

This Panel app implements an automated order collection system for a restaurant called ChopMoney. It interacts with users in a conversational manner to collect their orders, clarify options, and process payments.

## Features

- Automated conversation with users.
- Collection of orders for pickup or delivery.
- Clarification of menu options and sizes.
- Calculation of final order summary and total price.
- Integration with OpenAI's GPT-3.5 model for natural language processing.

## Getting Started

### Prerequisites

Before running the app, ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/chopmoney-orderbot-panel.git
    ```

2. Navigate to the project directory:

    ```bash
    cd chopmoney-orderbot-panel
    ```

3. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running the App

To run the Panel app, use the following command:

```bash
python3 -m panel serve test.py --host=0.0.0.0
```
### Usage
 - Access the app through a web browser by navigating to http://localhost:5006 (or the appropriate address if hosted elsewhere).
 - Interact with the app by entering messages in the text input field and clicking "Submit".
 - Follow the prompts to place an order and complete the conversation flow.
### Acknowledgments
 - This app utilizes the OpenAI GPT-3.5 model for natural language processing.
 - Inspired by the need for automated order collection systems in restaurants
### Contributors
 - **Developer**
   - **Name:**  *Youaleu TCHOUASSI Frank Loic*  
   - **Email:** *frankpythagore@gmail.com*  
 - **Surpervisor**
   - **Name:** *Mr NWAL Franck*  
   - **Email:** *franck.nwal@mobilehub.com*