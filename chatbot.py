import re
import random
from difflib import SequenceMatcher

from nltk.stem import PorterStemmer


# Create stemmer
stemmer = PorterStemmer()


# ==========================================================
# FAQ DATA
# ==========================================================

FAQS = [

    {
        "intent": "greeting",

        "questions": [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ],

        "responses": [
            "Hello! How can I help you today?",
            "Hi! Welcome to our customer support chatbot.",
            "Hello! What can I help you with?"
        ]
    },


    {
        "intent": "how_are_you",

        "questions": [
            "how are you",
            "how are you doing",
            "how is it going",
            "how do you feel"
        ],

        "responses": [
            "I'm doing great! How can I help you?",
            "I'm fine, thank you! How can I assist you today?",
            "I'm doing well! What can I help you with?"
        ]
    },


    {
        "intent": "working_hours",

        "questions": [
            "what are your working hours",
            "when are you open",
            "business hours",
            "office timings",
            "when can I contact support",
            "what time are you open"
        ],

        "responses": [
            "Our support team is available Monday to Friday, from 9 AM to 6 PM."
        ]
    },


    {
        "intent": "contact",

        "questions": [
            "how can I contact you",
            "contact support",
            "customer support number",
            "how do I reach support",
            "support contact",
            "how can I talk to customer support"
        ],

        "responses": [
            "You can contact our support team through support@example.com or call +91 98765 43210."
        ]
    },


    {
        "intent": "order_status",

        "questions": [
            "where is my order",
            "check my order",
            "order status",
            "track my order",
            "how can I track my order",
            "where is my package",
            "track my package"
        ],

        "responses": [
            "Please provide your order ID so you can check the latest order status."
        ]
    },


    {
        "intent": "delivery",

        "questions": [
            "how long does delivery take",
            "delivery time",
            "when will my order arrive",
            "how many days for delivery",
            "shipping time",
            "how long will shipping take"
        ],

        "responses": [
            "Standard delivery usually takes 3 to 5 business days."
        ]
    },


    {
        "intent": "return",

        "questions": [
            "how can I return a product",
            "return product",
            "I want to return my order",
            "return policy",
            "can I return a product",
            "how do I return my order"
        ],

        "responses": [
            "You can request a return within 7 days of receiving the product, provided it meets our return conditions."
        ]
    },


    {
        "intent": "refund",

        "questions": [
            "when will I get my refund",
            "refund status",
            "how long does refund take",
            "I want a refund",
            "refund policy",
            "when will my money be refunded"
        ],

        "responses": [
            "Refunds are normally processed within 5 to 7 business days after the return is approved."
        ]
    },


    {
        "intent": "payment",

        "questions": [
            "what payment methods do you accept",
            "payment options",
            "can I pay using upi",
            "do you accept credit cards",
            "payment methods",
            "how can I pay"
        ],

        "responses": [
            "We support UPI, debit cards, credit cards and online banking."
        ]
    },


    {
        "intent": "password",

        "questions": [
            "I forgot my password",
            "reset password",
            "change password",
            "how can I reset my password",
            "password recovery",
            "how do I change my password"
        ],

        "responses": [
            "You can reset your password using the 'Forgot Password' option on the login page."
        ]
    },


    {
        "intent": "thanks",

        "questions": [
            "thank you",
            "thanks",
            "thank you so much",
            "thanks for helping",
            "thank you for your help"
        ],

        "responses": [
            "You're welcome!",
            "Happy to help!",
            "You're welcome. Have a great day!"
        ]
    },


    {
        "intent": "goodbye",

        "questions": [
            "bye",
            "goodbye",
            "see you",
            "see you later"
        ],

        "responses": [
            "Goodbye! Have a great day!",
            "See you again!",
            "Thank you for chatting with us!"
        ]
    }

]


# ==========================================================
# TEXT PREPROCESSING
# ==========================================================

def preprocess(text):

    # Convert text to lowercase
    text = text.lower()

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Split into words
    words = text.split()

    # Remove very common words
    stop_words = {
        "the",
        "is",
        "a",
        "an",
        "to",
        "my",
        "me",
        "do",
        "does",
        "can",
        "i",
        "you",
        "your",
        "are"
    }

    words = [
        word for word in words
        if word not in stop_words
    ]

    # Apply stemming
    stemmed_words = [
        stemmer.stem(word)
        for word in words
    ]

    return stemmed_words


# ==========================================================
# WORD SIMILARITY
# ==========================================================

def word_similarity(user_words, question_words):

    if not user_words or not question_words:
        return 0

    matches = 0

    for user_word in user_words:

        for question_word in question_words:

            similarity = SequenceMatcher(
                None,
                user_word,
                question_word
            ).ratio()

            if similarity >= 0.80:

                matches += 1

                break

    return matches / max(
        len(user_words),
        len(question_words)
    )


# ==========================================================
# FIND BEST RESPONSE
# ==========================================================

def get_response(user_message):

    user_words = preprocess(user_message)

    best_score = 0

    best_faq = None


    for faq in FAQS:

        for question in faq["questions"]:

            question_words = preprocess(question)


            # Word-based similarity
            word_score = word_similarity(
                user_words,
                question_words
            )


            # Sentence similarity
            sentence_score = SequenceMatcher(
                None,
                user_message.lower().strip(),
                question.lower().strip()
            ).ratio()


            # Combined score
            score = (
                word_score * 0.7
                +
                sentence_score * 0.3
            )


            if score > best_score:

                best_score = score

                best_faq = faq


    # Only answer when confidence is good enough
    if best_score >= 0.55:

        return random.choice(
            best_faq["responses"]
        )


    # Unknown question
    return (
        "I'm sorry, I couldn't understand your question. "
        "You can ask me about orders, delivery, returns, "
        "refunds, payments, passwords or customer support."
    )