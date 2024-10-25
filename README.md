# A simple python programm that parses all your messages from telegram and prints required number of least and most common of them.


## Setup Instructions

### 1. Clone the Repository
First, clone this repository to your local machine:
```bash
git clone https://github.com/VTiganov/simple_tg_parser.git
```

### 2. (optional) Create and activate virual enviroment
```bash
cd simple_tg_parser
python -m venv venv
.\venv\Scripts\Activate
```

### 3. Install Dependencies

Install all required packages using the requirements.txt file:
```
pip install -r requirements.txt
```

### 4. Set up your .env file:
```
API_ID=<YOUR_API_ID>
API_HASH=<YOUR_API_HASH>
```

### 5. Run the programm

For parser
```bash
python telegram_parser.py
```
For main script
```bash
python main.py
```
