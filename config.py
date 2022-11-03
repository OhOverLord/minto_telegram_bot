#Я вынес сюда все тексты кнопок, так как не знал в каком виде они будут храниться на сервере, можно читать их из файла, но на хероку это не сработает

BUTTONS = {
    "competition": "I have won the Minto competition",
    "code": "I have a code from Minto card",
    "valid_data": "The data is correct",
    "not_valid_data": "There is something wrong with the data",
    "minto_about": "📚Minto about📚",
    "free_tokens": "🤑Get free tokens🤑",
    "support": "support",
}

INFO = {
    "competition_info": """
Congratulations!

Please send us following data:
— a link to the competition you participated in
—  your nickname from the social media where you won
— your wallet number on BSC chain
Example message:
https://t.me/btcmtofficial/527 @example 0xD984b7b3A92753f74c9e2025de7902a5ABb74df4
    """,
    "code_info": """
Cool that you decided to try mining with Minto! We need quite a bit of data to send you tokens.
In the booklet, on the card under the erasable layer, you should have a code. Please send it along with your wallet number on BSC chain.
    """,
    "info_answ": "Thanks! Give me up to one hour to check the data.",
    "failed_answ": """
        Sorry, it seems that your data is not accurate and we couldn’t verify it.
        If you want more details or have any questions — we can kindly connect you with our support team
    """,
    "correct_answ": """
        Cool! Tokens are already on your wallet. 
        All you need to do is stake them to receive an everyday reward in BTC. Here are detailed instructions on how to do it.
        To receive a new info about the project please follow us on:
        telegram | discord |  twitter
        Do you have any questions?
    """,
    "welcome_text": "Hello sir, Welcome to the mitno bot. Please write /help to see the commands available.",
    "token_text": "Wow! You can take your tokens! Choose the button!",
    "not_valid_data": "Data isn't valid, send in one more time",
}