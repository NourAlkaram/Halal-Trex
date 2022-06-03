from tools import *
import telegram
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext import *

TOKEN = ""
bot = telegram.Bot(token=TOKEN)
updater = Updater(TOKEN, use_context=True)

#This queue is ment to store the incoming messages orderd by sending time
#responseQueue = [] 
#This dic stores an InlineKeyboardMarkup of the current unplayed cards
inlineCards = {}
#This set stores the update.message.from_user.id of each player 
#idSet = set()
id = list() 
usernames = {}
#No need to discribe this integer :3
playersCnt = 0
currentKing = 0
gamesButtons = [
            [
                telegram.InlineKeyboardButton("بنات" , callback_data="/girls"), 
                telegram.InlineKeyboardButton("ختيار" , callback_data="/oldman")
            ],
            [
                telegram.InlineKeyboardButton("لطوش" , callback_data="/hits"), 
                telegram.InlineKeyboardButton("دينار" , callback_data="/money")
            ], 
            [
                telegram.InlineKeyboardButton("تريكس" , callback_data="/trex")
            ]
        ]
games = [
            ["بنات", "ختيار"],
            ["لطوش", "دينار"], 
            ["تريكس"]
        ]
currentKingdom = games
currentKingdomButtons = gamesButtons
whereAmIKingdoms = 0
whereAmIGames = 6

def start(update: Update, context: CallbackContext):
    if(update.message.chat_id == update.message.from_user.id):
        bot.send_message(chat_id=update.message.chat_id , text = "Start from a group, Please 😄")
    else:
        bot.send_message(chat_id=update.message.chat_id , text = "Welcome to Halal-Trex 😄\nGame Developer: @Nour_Alkaram")
        bot.send_message(chat_id=update.message.chat_id , text = "تعليمات بداية اللعب:\n☝🏼 للانضمام إلى هذه اللعبة اكتب /register ثم اكتب اسمك\n✌🏼 الرجاء الانتباه إلى أن عدد اللاعبين يجب أن يكون 3 أو 4.\n👌🏼 عندما يكتمل تسجيل كل اللاعبين اضغط على  /done.\nبالتوفيق 😁")

def register(update: Update , context: CallbackContext):
    if(update.message.chat_id == update.message.from_user.id):
        bot.send_message(chat_id=update.message.chat_id , text = "Register from a group, Please 😄")
    else:
        if(len(id)==4):
            bot.send_message(chat_id=update.message.chat_id, text="لقد بلغ عدد اللاعبين الحد الأعظم")    
        else:
            username = " ".join(context.args)
            #idSet.add(update.message.from_user.id)
            id.append(update.message.from_user.id)
            usernames[update.message.from_user.id] = username
            messageid = update.message.message_id
            #idSet
            #bot.send_message(chat_id=update.message.chat_id , reply_to_message_id = messageid ,text="تم تسجيل "+username+"\n"+" عدد اللاعبين المسجلين حتى الآن هو: "+str(len(idSet)))
            #id
            bot.send_message(chat_id=update.message.chat_id , reply_to_message_id = messageid ,text="تم تسجيل "+username+"\n"+" عدد اللاعبين المسجلين حتى الآن هو: "+str(len(id)))
            
def done(update: Update, context: CallbackContext):
    #for player in idSet:
    #    id.append(player)
    global whereAmIGames
    global currentKing
    global whereAmIKingdoms
    global playersCnt
    if(len(id)<3):
        bot.send_message(chat_id=update.message.chat_id, text="عدد اللاعبين المسجلين غير كاف!")    
    else:
        bot.send_message(chat_id=update.message.chat_id, text=".بدأت المملكة الأولى، سأقوم من الآن فصاعداً بالتواصل مع كل منكم عبر رسائل خاصة")
        playersCnt = len(id)
        whereAmIKingdoms = 0
        whereAmIGames = 0
        currentKing = id[whereAmIKingdoms]
        gameProcess()
    pass

def echo(update: Update, context: CallbackContext):
    #responseQueue.append((update.message.text , update.message.from_user.id))
    #print(responseQueue)
    pass

#The output of this function is InlineCards
def sendCards(playersCnt):
    cardsDst(playersCnt)
    x=1
    for i in id:
        button_list = []
        cnt = 0
        for j in distCards[str(x)]:
            _ = []
            __ = str(j[1])+' '+str(j[0])
            _.append(telegram.InlineKeyboardButton(__ ,callback_data=(str(cnt)+','+str(x))))
            button_list.append(_)
            cnt+=1
        reply_markup = telegram.InlineKeyboardMarkup(button_list)
        inlineCards[str(x)] = button_list
        bot.send_message(chat_id=i , text= "بطاقاتك الحالية هي:", reply_markup=reply_markup)
        x=x+1  
    pass

def callAGame(king):
    sendCards(playersCnt)
    for i in id:
        if (i==king):
            gamesMarkup = telegram.InlineKeyboardMarkup(currentKingdomButtons)
            bot.send_message(chat_id = i , text="اختر اللعبة: " , reply_markup=gamesMarkup)        
    pass

def gameProcess():
    #Let the king call a game
    global whereAmIGames
    global whereAmIKingdoms
    global currentKing
    global playersCnt
    whereAmIGames +=1
    if whereAmIGames == 6:
        whereAmIKingdoms+=1
        whereAmIGames = 0
        #Changing the king 
        if whereAmIKingdoms < playersCnt:
            currentKing = id[whereAmIKingdoms]
            #Say who is the new King
            for player in id:
                if player != currentKing:
                    bot.send_message(chat_id = player , text = "مملكة "+usernames[currentKing])
            callAGame(currentKing)
        else: 
            endTheGame()
    else:
        callAGame(currentKing)
    pass

def girls(update: Update, context: CallbackContext):

    print("girls")
    pass
def oldman(update: Update, context: CallbackContext):
    print("oldman")
    pass
def hits(update: Update, context: CallbackContext):
    print("hits")
    pass
def money(update: Update, context: CallbackContext):
    print("money")
    pass
def trex(update: Update, context: CallbackContext):
    print("trex")
    pass

def endTheGame():
    pass

def callback_query_handler(update: Update, context: CallbackContext):
    input = update.callback_query.data
    if input == '/girls':
        del currentKingdom[0][0]
        del currentKingdomButtons[0][0]
        gamesMarkup = telegram.InlineKeyboardMarkup(currentKingdomButtons)
        #update.callback_query.edit_message_reply_markup(gamesMarkup)
        update.callback_query.delete_message()
        for i in id:
            bot.send_message(chat_id = i , text="اللعبة بنات")
            bot.send_message(chat_id = i , text="نعتبر لعبنا وخلصنا")
        girls()
    elif input == '/oldman':
        if(len(currentKingdom[0]) == 2):
            del currentKingdom[0][1]
            del currentKingdomButtons[0][1]
        else:
            del currentKingdom[0][0]
            del currentKingdomButtons[0][0]
        gamesMarkup = telegram.InlineKeyboardMarkup(currentKingdomButtons)
        #update.callback_query.edit_message_reply_markup(gamesMarkup)
        update.callback_query.delete_message()
        for i in id:
            bot.send_message(chat_id = i , text="اللعبة ختيار") 
            bot.send_message(chat_id = i , text="نعتبر لعبنا وخلصنا")       
        oldman()
    elif input == '/hits':
        del currentKingdom[1][0]
        del currentKingdomButtons[1][0]
        gamesMarkup = telegram.InlineKeyboardMarkup(currentKingdomButtons)
        #update.callback_query.edit_message_reply_markup(gamesMarkup)      
        update.callback_query.delete_message()  
        for i in id:
            bot.send_message(chat_id = i , text="اللعبة لطوش")  
            bot.send_message(chat_id = i , text="نعتبر لعبنا وخلصنا")      
        hits()
    elif input == '/money':
        if(len(currentKingdom[1]) == 2):
            del currentKingdom[1][1]
            del currentKingdomButtons[1][1]
        else:
            del currentKingdom[1][0]
            del currentKingdomButtons[1][0]
        gamesMarkup = telegram.InlineKeyboardMarkup(currentKingdomButtons)
        #update.callback_query.edit_message_reply_markup(gamesMarkup)            
        update.callback_query.delete_message()        
        for i in id:
            bot.send_message(chat_id = i , text="اللعبة دينار")
            bot.send_message(chat_id = i , text="نعتبر لعبنا وخلصنا")
        money()
    elif input == '/trex':
        del currentKingdom[2]
        del currentKingdomButtons[2]
        gamesMarkup = telegram.InlineKeyboardMarkup(currentKingdomButtons)
        #update.callback_query.edit_message_reply_markup(gamesMarkup)        
        update.callback_query.delete_message()    
        for i in id:
            bot.send_message(chat_id = i , text="اللعبة تريكس")
            bot.send_message(chat_id = i , text="نعتبر لعبنا وخلصنا")   
        trex()
    else:
        x = int(input[len(input)-1])
        cnt = -1
        if(input[1]==','):
            cnt = int(input[0])
        else:
            cnt = 10 + int(input[1])
        del inlineCards[str(x)][cnt]
        del distCards[str(x)][cnt]
        reply_markup = telegram.InlineKeyboardMarkup(inlineCards[str(x)])
        update.callback_query.edit_message_reply_markup(reply_markup)
        if (len(inlineCards[str(x)]) == 0):
            update.callback_query.delete_message()
    pass



dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("register", register))
dp.add_handler(CommandHandler("r", register))
dp.add_handler(CommandHandler("done", done))
dp.add_handler(MessageHandler(Filters.regex(r""), echo))
dp.add_handler(CallbackQueryHandler(callback_query_handler))
updater.start_polling()