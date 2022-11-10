from bs4 import BeautifulSoup
import requests

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler
import keys

print('Starting up bot...')


def word_lookup(word):
    url = f"https://dsal.uchicago.edu/cgi-bin/app/hayyim_query.py?qs={word}&searchhws=yes&matchtype=exact"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    entry = doc.find('div', class_='hw_result')
    if entry:
        return entry.text
    else:
        return "Sorry, I wasn't able to find this entry."


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query,
            title='Look up',
            input_message_content=InputTextMessageContent(word_lookup(query))
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I can look up Persian words for you. Just write me a word in Persian, e.g. درود, and I'll give you the definition.")


async def lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
     await context.bot.send_message(chat_id=update.effective_chat.id, text=word_lookup(update.message.text))




if __name__ == '__main__':
    application = ApplicationBuilder().token(keys.token).build()

    # Defining handlers

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    lookup_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), lookup)
    inline_caps_handler = InlineQueryHandler(inline_caps)

    # Adding handlers
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(lookup_handler)
    application.add_handler(inline_caps_handler)


    application.run_polling()
