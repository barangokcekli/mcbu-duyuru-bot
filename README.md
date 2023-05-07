# MCBU Announcements Checker
This Python script checks the latest announcement on the websites listed in the URLS dictionary and sends an email notification to the email addresses listed in the EMAIL_INFO dictionary.

### Prerequisites
- Python 3.x
- `requests` module
- `beautifulsoup4` module
- `smtplib` module
- `email-to` module
- `dotenv` module
- A Gmail account with "App password" turned on

### Installation
1. Clone this repository to your local machine.
2. Install the required modules:
  ```python
  pip3 install -r requirements.txt
  ````
3. Create a `.env` file in the same directory as the `announcement.py` file, and add the following lines:
  ```python
  sender_password=your_gmail_app_password
  ```

### Customization

#### `EMAIL_INFO` Dictionary
The EMAIL_INFO dictionary contains the email information for sending the notifications. You can customize the sender email, sender password, and receiver emails by modifying this dictionary.

Example:
```python
EMAIL_INFO = {
    "sender_email": "your_email@gmail.com",
    "sender_password": "your_gmail_password",
    "receiver_emails": ["receiver1@example.com", "receiver2@example.com"]
}

```
  
