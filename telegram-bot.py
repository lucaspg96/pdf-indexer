import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from utils import elasticUtils, configUtils

config = configUtils.get_config("telegram")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:    
    user = update.effective_user
    update.message.reply_html(
        f"Bem vindo, {user.mention_html()}! Me chamo Cid, sou o mestre dos registros da Tormenta." +\
        " Se quiser me perguntar algo, basta escrever /search ou /buscar e informar o que deseja saber."
    )

def search(update: Update, context: CallbackContext) -> None:
    search = " ".join(update.message.text.split(" ")[1:])
    if len(search.strip()) == 0:
        update.message.reply_text("Perdão, mas preciso que você diga o que precisa saber.")
        return

    all_results = elasticUtils.search_documents(search)

    if len(all_results) == 0:
        update.message.reply_text("Perdão, mas não me recordo de nada relacioando a isso...")
    else:
        update.message.reply_text(f"Resultados da busca _{search}_:\n", parse_mode=ParseMode.MARKDOWN)
        for file,results in all_results.items():
            msg = f"Arquivo: *{file.split('/')[-1]}*\n\n"
            for page in results:
                msg += f"- Página {page['page']}:\n"
                msg += "\t- "+"...\n\t- ...".join(page["highlight"])+"\n\n"
            update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        
        

token = config["botToken"]

if len(token) == 0 or token is None:
    raise Exception("Token must be provided to run the telegram bot")

updater = Updater(token)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("search", search))
dispatcher.add_handler(CommandHandler("buscar", search))

updater.start_polling()
updater.idle()


