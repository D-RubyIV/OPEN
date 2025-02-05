#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import hashlib
import subprocess
from getResultWeb import Game82VN
from callAttackResult import CallBookmaker
from docAllMessage import AllBody
from saveFileData import SaveDataWinLose

import logging, time, requests
from collections import defaultdict
from typing import DefaultDict, Optional, Set
from telegram import __version__ as TG_VER


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ExtBot,
    TypeHandler,
    MessageHandler,
    filters
   
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class ChatData:
    """Custom class for chat_data. Here we store data per message."""

    def __init__(self) -> None:
        self.clicks_per_message: DefaultDict[int, int] = defaultdict(int)


# The [ExtBot, dict, ChatData, dict] is for type checkers like mypy
class CustomContext(CallbackContext[ExtBot, dict, ChatData, dict]):
    """Custom class for context."""

    def __init__(self, application: Application, chat_id: int = None, user_id: int = None):
        super().__init__(application=application, chat_id=chat_id, user_id=user_id)
        self._message_id: Optional[int] = None

    @property
    def bot_user_ids(self) -> Set[int]:
        """Custom shortcut to access a value stored in the bot_data dict"""
        return self.bot_data.setdefault("user_ids", set())

    @property
    def message_clicks(self) -> Optional[int]:
        """Access the number of clicks for the message this context object was built for."""
        if self._message_id:
            return self.chat_data.clicks_per_message[self._message_id]
        return None

    @message_clicks.setter
    def message_clicks(self, value: int) -> None:
        """Allow to change the count"""
        if not self._message_id:
            raise RuntimeError("There is no message associated with this context object.")
        self.chat_data.clicks_per_message[self._message_id] = value

    @classmethod
    def from_update(cls, update: object, application: "Application") -> "CustomContext":
        """Override from_update to set _message_id."""
        # Make sure to call super()
        context = super().from_update(update, application)

        if context.chat_data and isinstance(update, Update) and update.effective_message:
            # pylint: disable=protected-access
            context._message_id = update.effective_message.message_id

        # Remember to return the object
        return context


async def start(update: Update, context: CustomContext) -> None:
    """Display a message with a button."""
    await update.message.reply_html(
        "This button was clicked <i>0</i> times.",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text="Click me!", callback_data="button")
        ),
    )


async def count_click(update: Update, context: CustomContext) -> None:
    context.message_clicks += 1
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        f"This button was clicked <i>{context.message_clicks}</i> times.",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text="Click me!", callback_data="button")
        ),
        parse_mode=ParseMode.HTML,
    )


async def print_users(update: Update, context: CustomContext) -> None:
    await update.message.reply_text(
        "The following user IDs have used this bot: "
        f'{", ".join(map(str, context.bot_user_ids))}'
    )


async def track_users(update: Update, context: CustomContext) -> None:
    if update.effective_user:
        context.bot_user_ids.add(update.effective_user.id)



def sendToChannel(update: Update, context: CustomContext, idChat: int, message: str) -> None:
    context.bot.send_message(idChat, text=message)
 



async def run_bot(update: Update, context: CustomContext) -> None:
    kisoHienTai = 0
    await update.message.reply_text(
        "Bot Running..."
    )
    listPhanTram = [1,2,4,8,17,36,75,150,320]
    indexPT = 0
    KqDaDuDoan = ""
    indexPhienWin = 0
    while True:

     
        

        while True:
            # try:
            listLN, kisoUpdate, blockNumber = Game82VN().getResult()
            #     break
            # except Exception as e:
            #     print(f"Lỗi Get KQ Web - Errror: {str(e)}")
            time.sleep(1)
            
        if int(kisoUpdate) > kisoHienTai:
            kisoHienTai = int(kisoUpdate)
            print("Phát Hiện Có Sự Thay Đổi Kì Số")
            

        
            ketquaDuDoan = str(CallBookmaker(listLN).callResult()).upper()
            print(f"Dự Đoán Kết Quả Kì[{int(kisoUpdate)+1}]: {ketquaDuDoan}")
            sttPhien = int(open("Data\SttPhien.txt","r").read())
            if KqDaDuDoan != "":
                print(f"Dự Đoán Kết Quả Kì Trước:[{int(kisoUpdate)}]: {KqDaDuDoan}")
                print(f"Kết Quả Kì Trước:[{int(kisoUpdate)}]: {listLN[0]}")
                if KqDaDuDoan == listLN[0]:
                    winText = open("Data/TextWin.txt","r", encoding="utf-8").read()
                    SaveDataWinLose(f"{winText}{sttPhien + 1}").saveData()
                    for i in range(500):
                        time.sleep(1)
                        try:
                            await context.bot.send_message(int(open("IDChat.txt","r").read()), text="❗️ 𝐊ế𝐭 𝐪𝐮ả🟢 THẮNG")
                            await context.bot.send_message(int(open("IDChat.txt","r").read()), text=AllBody().getAllBody())
                            break
                        except Exception as e:
                            print(e)
                            ()
                    open("Data\SttPhien.txt","w+").write(str(sttPhien + 1))
                    indexPT = 0
                    indexPhienWin += 1
                
                else:
                    for i in range(500):
                        time.sleep(1)
                        try:
                            await context.bot.send_message(int(open("IDChat.txt","r").read()), text="❗️ 𝐊ế𝐭 𝐪𝐮ả⛔️ THUA")
                            break
                        except Exception as e:
                            print(e)
                            ()
                    indexPT += 1


                if int(open("Data\GioiHanPhien.txt","r").read()) == indexPhienWin:
                    for i in range(500):
                        time.sleep(1)
                        try:
                            await context.bot.send_message(int(open("IDChat.txt","r").read()), text="✅ Đã đạt lợi nhuận ca này , đợi ca tiếp theo")
                            break
                        except Exception as e:
                            print(e)
                            ()
                    break


                if indexPT == 9:
                    loseText = open("Data/TextLose.txt","r", encoding="utf-8").read()
                    SaveDataWinLose(f"{loseText}{sttPhien + 1}").saveData()
                    for i in range(500):
                        time.sleep(1)
                        try:
                            await context.bot.send_message(int(open("IDChat.txt","r").read()), text="♦️ Phiên - THUA 🟡 - 613%")
                            await context.bot.send_message(int(open("IDChat.txt","r").read()), text="DỪNG BOT CHỐT LỖ ✋")
                            break
                        except Exception as e:
                            print(e)
                            ()
                    open("Data\SttPhien.txt","w+").write(str(sttPhien + 1))
                    break
            KqDaDuDoan = ketquaDuDoan
            
            
            KQ = "Lớn" if ketquaDuDoan == "L" else "Nhỏ"
            text = f"""
            GAME TRX-HASH 1 PHÚT\nKỳ xổ: <b>{int(kisoUpdate)+1}</b>\nVào Lệnh: <b>{KQ} {listPhanTram[indexPT]}%</b>
            """
            for i in range(500):
                time.sleep(1)
                try:
                    await context.bot.send_message(int(open("IDChat.txt","r").read()), text=text, parse_mode=ParseMode.HTML)
                    break
                except Exception as e:
                    print(e)
                    ()

        print("\n")
        time.sleep(2)


async def get_id_chat(update: Update, context: CustomContext):
    idChat = context._chat_id
    await context.bot.send_message(idChat, text=f"ID Chat: {idChat}")
 


async def handle_text(update: Update, context: CustomContext):
    text = update
    messageText = text.channel_post.text
    idChat = context._chat_id
    response_text = f"ID Chat: {idChat}"
    print(response_text)
    
async def error(update: Update, context: CustomContext):
    #Logs errors
    logging.error(f'[!!!]Error: {context.error}')
  

def main() -> None:
    """Run the bot."""
    context_types = ContextTypes(context=CustomContext, chat_data=ChatData)
    application = Application.builder().token(open("Token.txt","r").read()).context_types(context_types).build()
    application.add_handler(TypeHandler(Update, track_users), group=-1)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("runbot", run_bot))
    application.add_handler(CommandHandler("idchat", get_id_chat))
    application.add_handler(CallbackQueryHandler(count_click))
    application.add_handler(CommandHandler("print_users", print_users))
    application.add_handler(MessageHandler(filters.ALL, handle_text))
    application.run_polling(1.8)
    application.idle()

def getKey():
    Id = str(list(subprocess.Popen('systeminfo', stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=False, creationflags=subprocess.CREATE_NO_WINDOW).communicate())[0]).replace("b'",'').replace(r"\r",'').replace(" ",'')
    Id = Id.split("\\n")
    for i in Id:
        if "ProductID" in str(i):
            ID_PRODUCT = str(i.split(':')[1]).strip()
    return ID_PRODUCT

def getSerial():
    Serial_Number = str(list(subprocess.Popen('wmic bios get serialnumber', stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=False, creationflags=subprocess.CREATE_NO_WINDOW).communicate())[0]).replace("b'",'').replace(r"\r",'').replace(" ",'')
    Serial_Number  = Serial_Number.split("\\n")[1]
    return Serial_Number

def enCode(text):
    hashed_text = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return hashed_text

if __name__ == "__main__":
    key = getKey() + getSerial()
    key = enCode(key)
    result = requests.get("https://raw.githubusercontent.com/D-RubyIV/Resource-V/main/Game82/key.txt").text
    if str(key) in result:
        print(f"Key: {key}")
        print("Active: True")
        main()
    else:
        print(f"Key: {key}")
        print("Active: False")
        input("Nhập Bất Kì Để Thoát!!!")
    