import telebot
from telebot import types
import time
import tok
from time import sleep
import Files
import jn
import json
import os


TOKEN= tok.token
bot=telebot.TeleBot(TOKEN)

adress=r'PathOfYourDataDirectory'+"\\"


                              # ВЫВОД в консоль
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot.set_update_listener(listener)

Fname="cheloveki"
knownUsers = []  
userStep = {} 
userColl={}
userImages={}

commands = { 
              'start': 'Начало работы с сово-ботом',
              'help': 'Информация о доступных командах',
              
              'addCollection': 'Тут, тип, коллекция. Ну, в названии видно, да',
             # 'showсollection': 'Редактирование',
              'showCollection': 'Тут можно посмотреть все добавленные коллекции'
}




                              #   ПРОВЕРКА : есть ли юзер в списке
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        
        userStep[uid] = 0
        print( "Новый пользователь, не использовавший \"/start\" yet")
        return 0

Files.WriteF(Fname)

                              #   СТАРТ
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    
    if  Files.inF(cid,Fname):  
        bot.send_message(cid, "Я тебя уже знаю, спасибо")
    else:
        Files.addF(cid,Fname) 
        userStep[cid] = 0  
        bot.send_message(cid, "Доброе утро, незнакомец позволь мне просканировать тебя...")
        bot.send_message(cid, "Сканирование завершено, теперь я знаком с тобой")
        jn.NewDir(adress+str(cid))
        command_help(m) 

                              #   ПОМОЩЬ
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    userStep[cid] = 0
    help_text = "Доступны следующие команды: \n"
    for key in commands:  
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)



                              #  КОЛЛЕКЦИЯ
@bot.message_handler(commands=['addCollection'])
def collection(m):
    cid=m.chat.id
    userStep[cid] = 0
    bot.send_message(cid, "Создать коллекцию (на любом этапе, ошибка - прислать 'радиокнопка') \nПришли название")
    userStep[cid] = 1

                              #  КОЛЛЕКЦИЯ, шаг 2: создание + запрос названия и описания
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def name_and_decsc(m):
    cid = m.chat.id
    text = m.text
    if text!="радиокнопка"  :
       papka=adress+str(cid)+"\\"+text
       jn.NewDir(papka)   # создание папки коллекции
       Files.Create(papka+"\\string")    # создание строки, которая потом перейдет в json-файл
       Files.Create(papka+"\\jn")         # создание  json-файла, в которій перейдет строка
       Files.AddFn("{", papka+"\\string") 
       userImages[cid]=1;
       bot.send_message(cid, "Океей, пришли название элемента и его описание в формате  название*описание")
       userColl[cid]=papka
       userStep[cid]=2
    else : userStep[cid]=0

                                     #  КОЛЛЕКЦИЯ, шаг 3: название + описание
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def real_name_desc(m):
    cid = m.chat.id
    text = m.text
    if text!="радиокнопка"  :
        te=text.split("*")
        bot.send_message(cid, "Океей, название: "+te[0]+", а описание: "+te[1])
        Files.AddFn('"'+str(userImages[cid])+'":{"name":"'+te[0]+'","disc":"'+te[1]+'",', userColl[cid]+"\\string")
        bot.send_message(cid, "А теперь самое сложное - картинкаа")
        userStep[cid]=3
    else : userStep[cid]=0

                                     #  КОЛЛЕКЦИЯ, шаг 4: картинка
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3, content_types=['photo'])
def image_get(m):
    cid = m.chat.id
    try:
         
         file_info = bot.get_file(m.photo[len(m.photo)-1].file_id)
         downloaded_file = bot.download_file(file_info.file_path)
         Files.AddFn('"img":"'+str(m.photo[len(m.photo)-1].file_id)+'"}', userColl[cid]+"\\string")
         src=userColl[cid]+"\\"+str(m.photo[len(m.photo)-1].file_id)  # название картинки - по номеру
         userImages[cid]+=1                          # увеличение номера следующей картинки в списке
         with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)
         bot.reply_to(m,"Фото добавлено!!") 
        
         # да\нет
         keyboard = types.InlineKeyboardMarkup()
         kb1 = types.InlineKeyboardButton(text="Да", callback_data="Да")
         kb2 = types.InlineKeyboardButton(text="Нет", callback_data="Нет")
         keyboard.add(kb1, kb2)
         msg = bot.send_message(cid, "Все просто восхитительно! Еще один элементик?)", reply_markup=keyboard)
         userStep[cid]=4
    except Exception as e:
         bot.reply_to(m,e )
         bot.send_message(cid, "ошибочка... обратись к @owlet_Eleo")
         userStep[cid]=0


                                     #  КОЛЛЕКЦИЯ, шаг 5: Ответочка на да/нет    

@bot.callback_query_handler( func= lambda call: get_user_step( call.message.chat.id)==4)
def ans(m):
    cid = m.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    if m.data == "Да":
        bot.send_message(cid, "Оки)  Пришли название*опиание снова", reply_markup=keyboard)
        Files.AddFn(',', userColl[cid]+"\\string")   #  запятая в джейсон между элементами
        userStep[cid]=2
    elif m.data == "Нет":
        bot.send_message(cid, "Ну ладно...", reply_markup=keyboard)
        Files.AddFn('}', userColl[cid]+"\\string")
        jn.StrToJson( Files.ToStr(userColl[cid]+"\\string"), userColl[cid]+"\\jn")
        # количество элементов записывается в отдельный
        Files.Create(userColl[cid]+"\\col")
        Files.addF(str(userImages[cid]),userColl[cid]+"\\col" )
        bot.send_message(cid, "Вроде добавил, хз. Спроси у @owlet_Eleo", reply_markup=keyboard)
        userColl[cid]=''     #  все по нулям
        userStep[cid]=0
        userImages[cid]=1  


adree=r'D:\Documents_D\PythonApplication3\PythonApplication3\371968080\Асины фотографии\\jn'  
with open(adree) as json_dataa:
         json_objj = json.load(json_dataa)
         json_objj['1']['name']='Получилось?'
         jn.ObjToJson(json_objj, adree)

                              #  РЕДАКТИРОВАНИЕ КОЛЛЕКЦИИ: Шаг 1



                              #  ПРОСМОТР КОЛЛЕКЦИИ: Шаг 1

@bot.message_handler(commands=['showCollection'])
def collection(m):
     cid=m.chat.id
     userStep[cid] = 0
     keyboard = types.InlineKeyboardMarkup()
     files=os.listdir(adress+str(cid))
     
     if os.listdir(adress+str(cid)):
         a=1
         for line in files:
             k=types.InlineKeyboardButton(text=line, callback_data=line)
             keyboard.add(k)
             a+=1
         msg = bot.send_message(cid, "Какую коллекцию хочешь посмотреть?)", reply_markup=keyboard)
         userStep[cid] = 11
     else:
         bot.send_message(cid, "К сожалению, у тебя еще нет ни одной коллекции. Хочешь создать - /addCollection")

 #  ПРОСМОТР КОЛЛЕКЦИИ: Шаг 2 :  Все вместе или о элементу
@bot.callback_query_handler( func=lambda c: get_user_step(c.message.chat.id) == 11)
def how(call):

         cid = call.message.chat.id
         keyboard = types.InlineKeyboardMarkup()

         userColl[cid]=adress+str(cid)+"\\"+call.data

         kb1 = types.InlineKeyboardButton(text="Все вместе", callback_data="в")
         kb2 = types.InlineKeyboardButton(text="По элементу", callback_data="э")
         keyboard.add(kb1, kb2)
         msg = bot.send_message(cid, "Просмотр коллекцией или по элемету?", reply_markup=keyboard)
         userStep[cid]=12


@bot.callback_query_handler( func=lambda c: get_user_step(c.message.chat.id) == 12)
def ans(c):
   cid = c.message.chat.id
   
    
   keyboard = types.InlineKeyboardMarkup()
   adr=userColl[cid]+"\\jn"
   with open(adr) as json_data:
         json_obj = json.load(json_data)

    #  КОЛЛЕКЦИЕЙ

   if c.data=="в":
    media = []
    kol=int(Files.ToStr(userColl[cid]+"\\col"))
    a=0
    while kol>0 :
      i=1
      media=[]
      while (i<kol and i<11):
        media.append(types.InputMediaPhoto(json_obj[str(i+a)]['img'], caption=str(json_obj[str(i+a)]['name'])+": "+str(json_obj[str(i+a)]['disc']) ))
        i+=1
      bot.send_media_group(cid, media)
      kol-=10
      a+=10

    userStep[cid] = 0
    userColl[cid]=''
 
   #  ПО ЭЛЕМЕНТУ
   elif c.data=="э":
       keyboards = types.InlineKeyboardMarkup() 
       i=1
       while i<int(Files.ToStr(userColl[cid]+"\\col")):
         k=types.InlineKeyboardButton(text=str(json_obj[str(i)]['name']), callback_data=str(json_obj[str(i)]['name']))
         keyboards.add(k)
         i+=1
       msg = bot.send_message(cid, "Какуой элемент хочешь посмотреть?)", reply_markup=keyboards) 
       userStep[cid]=13

   
       
       
       #  ПО ЭЛЕМЕНТУ:  вывести и да\нет
@bot.callback_query_handler( func=lambda c: get_user_step(c.message.chat.id) == 13)
def answe(c):
    cid = c.message.chat.id
    adr=userColl[cid]+"\\jn"
    with open(adr) as json_data:
         json_obj = json.load(json_data)
    keyboard = types.InlineKeyboardMarkup()
    i=1
    while i<int(Files.ToStr(userColl[cid]+"\\col")):
        if (str(json_obj[str(i)]['name'])==c.data) :
            bot.send_photo(cid, json_obj[str(i)]['img'], caption=str(json_obj[str(i)]['name'])+": "+str(json_obj[str(i)]['disc']) )
            i+=1
        else: i+=1
    
            #  да\нет
    keyboard = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton(text="Да", callback_data="Да")
    kb2 = types.InlineKeyboardButton(text="Нет", callback_data="Нет")
    keyboard.add(kb1, kb2)
    msg = bot.send_message(cid, "Ну как? Еще один элементик?)", reply_markup=keyboard)
    userStep[cid]=14

@bot.callback_query_handler( func= lambda call: get_user_step( call.message.chat.id)==14)
def ans(m):
    cid = m.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    if m.data == "Да":
        adr=userColl[cid]+"\\jn"
        with open(adr) as json_data:
         json_obj = json.load(json_data)
        keyboards = types.InlineKeyboardMarkup()
        i=1
        while i<int(Files.ToStr(userColl[cid]+"\\col")):
          k=types.InlineKeyboardButton(text=str(json_obj[str(i)]['name']), callback_data=str(json_obj[str(i)]['name']))
          keyboards.add(k)
          i+=1
        msg = bot.send_message(cid, "Какуой элемент хочешь посмотреть?)", reply_markup=keyboards) 
        userStep[cid]=13
        
    elif m.data == "Нет":
        bot.send_message(cid, "Ну ладно...", reply_markup=keyboard)
        
        userColl[cid]=''     #  все по нулям
        userStep[cid]=0
            






                              #  РАЗГОВОР

non={"lol","Fine?","Как ты?","ФИЗИКА ТОП","норм", "отлично", "жив" ,"все", "ок" ,"плохо"}
@bot.message_handler(func=lambda message: message.text in non)
def command_text_hi(m):
    if (m in hiiii): return
    bot.send_chat_action(m.chat.id, 'typing')
    time.sleep(2)
    if m.text == "lol": 
        tx="Ha-ha, really lol"
    elif m.text == "Fine?":
        tx="Yeap. And you?"
    elif m.text == "Как ты?":
        tx="Неплохо. А у тебя как жизнь? Будешь тут что-то делать?"
    elif m.text == "ФИЗИКА ТОП":
        tx="++++++++++++++++++++++++++++++++++++++"
    else: tx = "Я тоже жив"
    bot.send_message(m.chat.id, tx)



                              # СООБЩЕНИЕ  ПРИВЕТСТВИЯ
hiiii={"hi","Hi","HI", "Привет","привет","доброе утро","Доброе утро","Здравствуй","здравствуй","хай","ку"}
@bot.message_handler(func=lambda message: message.text in hiiii)
def command_text_hi(m):
    bot.send_chat_action(m.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(m.chat.id, "Доброе утро)  ")



if __name__ == '__main__':
     bot.polling(none_stop=True)
    
         