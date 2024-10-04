#log
import datetime 
import logging 
#.env
from decouple import config 
#json
import json
#tele
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

#đọc data file sukien.json
def load_sukien_data():
    file_path = config('SUKIEN')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
#đọc data file trucnhat.json
def load_trucnhat_data():
    file_path = config('TRUCNHAT')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
#đọc data file trucnhat.json
def load_btvn_data():
    file_path = config('BTVN')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id
    await update.message.reply_html(
        rf"Xin chào {user.mention_html()}!!!",
        # reply_markup=ForceReply(selective=True),
    )
    help_text = """
    Trung tâm trợ giúp
    /start - Hướng dẫn sử dụng
    /sukien - Xem sự kiện tháng hiện tại
    -- ví dụ /sukien 11 để xem sự kiện tháng 11
    /trucnhat - Xem thông tin trực nhật 
    -- ví dụ /trucnhat to1 để xem thông tin trực nhật tổ 1
    /baitapvenha - Xem thông tin bài tập về nhà
    -- ví dụ /baitapvenha 19/04/2024 để xem bài tập về nhà ngày 19/04/2024
    """
    await update.message.reply_text(help_text)

def log_command(parameter, user_id, command):
    """Log the executed command to a text file."""
    log_file_path = 'command_log.txt'
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{current_time} - User ID: {user_id}, Command: {command}, Parameter: {parameter}\n")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)
async def sukien(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show events for a specific month, based on the argument."""
    try:
        # Load event data from JSON
        data = load_sukien_data()
        
        # Get the command argument (month number)
        if context.args:
            try:
                month = int(context.args[0])
                if month < 1 or month > 12:
                    raise ValueError("Tháng không hợp lệ! Vui lòng chọn tháng từ 1 đến 12.")
            except ValueError as ve:
                await update.effective_message.reply_text(str(ve))
                return
        else:
            # If no argument is provided, default to current month
            month = datetime.datetime.now().month

        command_key = f"sukien{month}"

        # Fetch corresponding data from JSON
        event_info = data.get(command_key, "Không có sự kiện cho tháng này.")
        await update.effective_message.reply_text(event_info)
    except Exception as e:
        await update.effective_message.reply_text(f"Error: {e}")
async def trucnhat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond with the task associated with the given key (e.g., to1, to2)."""
    try:
        # Load task data from JSON
        data = load_trucnhat_data()
        
        # Get the command argument (toX)
        if context.args:
            task_key = context.args[0]  # e.g., 'to1', 'to2'
            task = data.get(task_key, "Không tìm thấy nhiệm vụ.")
            await update.message.reply_text(task)
        else:
            await update.message.reply_text("Vui lòng nhập một mã nhiệm vụ hợp lệ, ví dụ: /trucnhat to1.")
    
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
async def baitapvenha(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond with the homework based on the given date."""
    try:
        # Load homework data from JSON
        data = load_btvn_data()
        
        # Get the current date in dd/mm/yyyy format
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")

        # Check if a date argument is provided
        if context.args:
            date_query = context.args[0]  # e.g., '19/04/2024'
        else:
            date_query = current_date  # Default to the current date

        # Fetch the homework for the specified date
        homework = data.get(date_query)

        if homework:
            # Format the response
            formatted_response = f"Ngày: {date_query},\n\t Các môn:\n"
            for subject, task in homework.items():
                formatted_response += f"\t\t\t- {subject}: {task}\n"
        else:
            formatted_response = "Không tìm thấy bài tập cho ngày này."

        await update.message.reply_text(formatted_response.strip())
    
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config('TELEGRAM_BOT_TOKEN')).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sukien", sukien))
    application.add_handler(CommandHandler("trucnhat", trucnhat))
    application.add_handler(CommandHandler("baitapvenha", baitapvenha))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
