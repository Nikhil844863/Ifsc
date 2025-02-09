import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import json

# --- YOUR TELEGRAM CHANNEL USERNAME ---
CHANNEL_USERNAME = "@RtoVehicle"  # Change this to your actual channel username

# Function to check if user is a member of the channel
async def is_member(user_id, bot):
    try:
        chat_member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# Function to fetch vehicle details from API
def get_vehicle_details(registration_number):
    url = f"https://codex-ml.tech/api/rc.php?regno={registration_number}"
    response = requests.get(url)
    try:
        data = response.json()
        if data.get("data") and data["data"].get("detail"):
            return data["data"]["detail"]
        else:
            return None
    except json.JSONDecodeError:
        return None

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Welcome to Vehicle Info Bot! 🚗\n\n"
        f"To use this bot, you must first join our channel: {CHANNEL_USERNAME}\n"
        f"Then use /getdetails <REGISTRATION_NUMBER> to fetch vehicle details."
    )

# Get details command handler
async def getdetails(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot = context.bot

    # Check if the user is a member
    if not await is_member(user_id, bot):
        await update.message.reply_text(
            f"❌ You must join our channel first to use this bot!\nJoin here: {CHANNEL_USERNAME}"
        )
        return

    if len(context.args) == 0:
        await update.message.reply_text("Please provide a registration number. Example: /getdetails JH05BP9450")
        return

    registration_number = context.args[0]
    details = get_vehicle_details(registration_number)

    if details:
        message = json.dumps(details, indent=4)
        await update.message.reply_text(f"Vehicle Details:\n```{message}```", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Vehicle details not found. Please check the registration number.")

# Main function to run the bot
def main():
    application = Application.builder().token("7616068751:AAEEz9SEDfZBHdrBjNN7GI00eiXVj-EBuOM").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getdetails", getdetails))

    import asyncio
    try:
        asyncio.get_event_loop().run_until_complete(application.run_polling())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.run(application.run_polling())

if __name__ == "__main__":
    main()
