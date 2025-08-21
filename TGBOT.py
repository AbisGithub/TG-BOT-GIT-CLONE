import os
from dotenv import load_dotenv

import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = "8305217676:AAEikHa1bXQejn-WHczrgrEPv_-DCmqmBV0"
GEMINI_API_KEY = "AIzaSyCZltW4zDDVKHvdox2BkyNoCQpPkg3BKB4"

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Define the `/start` command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the command /start is issued."""
    await update.message.reply_text("Hello! I'm a bot powered by Gemini AI. How can I help you today?")

# Define the message handler for user input
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes a user's text message and gets a response from Gemini."""
    user_message = update.message.text
    
    try:
        # Generate content using the Gemini model
        response = model.generate_content(user_message)
        response_text = response.text
        
        # Send the Gemini response back to the user
        await update.message.reply_text(response_text)
    except Exception as e:
        print(f"An error occurred: {e}")
        await update.message.reply_text("Sorry, I couldn't generate a response. Something went wrong.")

def main():
    """Starts the bot."""
    # Build the Application and pass your bot's token
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Run the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()