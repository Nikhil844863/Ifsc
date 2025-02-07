import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your bot's API token
TELEGRAM_TOKEN = '7925346721:AAEnajZtvFfZlck5HNdM_Xwiy_ELqC8SktI'
API_TOKEN = '6645|8aUVZm0wEaovDsq0CTYaCxYmAm925i5wg8U9OV5j'  # API Token for Zyla Labs
API_URL = 'https://zylalabs.com/api/418/ifsc+code+validator+api/324/isfc+validator'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Send message function
async def send_message(update: Update, text: str):
    try:
        # Use update.message.chat.id to send the message
        response = await update.message.reply_text(text)
        logger.info(f"Sent message to {update.message.chat.id}: {text}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")

# Function to handle '/start' command
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    logger.info(f"User {user.id} started the bot")
    await update.message.reply_text('👋 Hi! Send me an IFSC code and I will validate it. ✨')

# Function to handle incoming messages
async def validate_ifsc(update: Update, context: CallbackContext) -> None:
    ifsc_code = update.message.text.strip()
    
    if not ifsc_code:
        await update.message.reply_text('⚠️ Please enter a valid IFSC code.')
        return

    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {'ifsc': ifsc_code}

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response_data = response.json()

        if response.status_code == 200:
            if response_data.get('data') == False:
                await send_message(update, "❌ The IFSC code is invalid.")
            else:
                bank_info = response_data['data']
                message = (
                    f"✅ **The IFSC code is valid!**\n\n"
                    f"🏦 **Bank:** {bank_info['bank']}\n"
                    f"🏢 **Branch:** {bank_info['branch']}\n"
                    f"📍 **Address:** {bank_info['address']}\n"
                    f"🌆 **City:** {bank_info['city']}\n"
                    f"🏙️ **State:** {bank_info['state']}\n"
                    f"📞 **Phone:** {bank_info['phone']}\n"
                    f"🔢 **IFSC Code:** {bank_info['ifsc']}\n"
                )
                await send_message(update, message)
        else:
            await send_message(update, '⚠️ Error: Could not validate the IFSC code.')
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await send_message(update, "❗ An error occurred while processing the request.")

# Main function to start the bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Message handler for IFSC code
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, validate_ifsc))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()