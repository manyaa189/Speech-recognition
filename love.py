import pyttsx3
import speech_recognition as sr
import datetime
import smtplib
import webbrowser
import time
import json
import os
import sqlite3
import urllib.request, urllib.parse, urllib.error
import ssl
import random
import wikipediaapi


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def speak(ip):
    engine.say(ip)
    engine.runAndWait()

def encodes(query,site,sign):
    lst = query.split()
    if sign == None:
        sign = '+'
    for j in range(len(lst)):
        if j == len(lst) - 1:
            site = site + lst[j]
            continue
        site = site + lst[j] + sign
    return site
def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')

    except Exception as e:
        # print(e)
        print("Say that again please...")   #Say that again will be printed in case of improper voice
        return None #None string will be returned
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@email.com', 'yourpassword')
    server.sendmail('youremail@email.com', to, content)
    server.close()

def google_classroom(query):
    if 'vivek' in query or 'instrumentation' in query:
        webbrowser.open('https://classroom.google.com/c/MjQ5NTM0ODA1NzU5')
    elif 'hari' in query or 'electrical machines' in query or 'em' in query or 'e m' in query:
        webbrowser.open('https://classroom.google.com/c/MjQ5NDUyMDQzNjkw')
    elif 'kailash' in query or 'gep' in query or 'power' in query:
        webbrowser.open('https://classroom.google.com/c/MjQ5NzEwODM4ODg1')
    elif 'geeta' in query or 'nm' in query or 'numerical methods' in query:
        webbrowser.open('https://classroom.google.com/c/MjQ5NDIxMjczNzgx')
    elif 'hcmi' in query or 'jagvinder' in query or 'economics' in query:
        webbrowser.open('https://classroom.google.com/c/MjQ5NTQxOTIxMDI0')
    else:
        return None
        return 0
def meet(query):
    if 'jagvinder' in query or 'hcmi' in query or 'economics' in query:
        os.startfile('C:\\Users\\Manish\\Desktop\\Microsoft Teams.lnk')
        #EM_class
    elif 'hari' in query or 'harimurugan' in query or 'em' in query :
        webbrowser.open('meet.google.com/ewf-cxby-ajf')
        #KC_class
    elif 'gep' in query or 'kailash' in query or 'jeep' in query:
        webbrowser.open('https://meet.google.com/lookup/asc3hiwjv5?authuser=0&hs=179')
        #geeta mam's class
    elif 'geeta' in query or 'nm' in query or 'numerical methods' in query:
        webbrowser.open('meet.google.com/hhs-bnwt-ysz')
        #vikvek Sir
    elif 'vivek' in query or 'instrumentation' in query:
        webbrowser.open('https://meet.google.com/mjj-xzsi-zsm')
    else:
        return False
        exit()
    return True
def timetable(what):
    con = sqlite3.connect('tt.sqlite')
    cur = con.cursor()
    day = datetime.datetime.now().strftime("%A")
    hour = int(datetime.datetime.now().strftime("%I"))+1
    minute = int(datetime.datetime.now().strftime("%M"))
    if hour < 8 and hour > 5 and what in ['lect','whose']:
        return('Not a class right now')
    m = 25
    if what == 'lect':
        ej = 'SELECT lect_table.lect'
    elif what == 'whose':
        ej = 'SELECT teachers_table.teacher'
    elif what == 'next_c':
        ej = 'SELECT lect_table.lect'
        hour += 1
        m = 30
    elif what == 'next_t':
        ej = 'SELECT teachers_table.teacher'
        hour += 1
        m = 30
    if minute <m:
        try:
            x = ej +'''
            FROM time_table JOIN day_table JOIN lect_table JOIN teachers_table
            ON time_table.day_id = day_table.id AND teachers_table.id = lect_table.teacher_id AND time_table.lect_id = lect_table.id AND day_table.day = \''''+day+'''\' AND time_table.time = \''''+str(hour-1)+'''\'
            '''
            s = cur.execute(x).fetchone()[0]
        except:
            s = 'No class exist right now!'
    else:
        try:
            x = ej + '''
            FROM time_table JOIN day_table JOIN lect_table JOIN teachers_table
            ON time_table.day_id = day_table.id AND teachers_table.id = lect_table.teacher_id AND time_table.lect_id = lect_table.id AND day_table.day = \''''+day+'''\' AND time_table.time = \''''+str(hour)+'''\'
            '''
            s = cur.execute(x).fetchone()[0]
        except:
            s = 'No class exist right now!'
    return s

def kindings(daytime,kind):
    ej = ''
    day = datetime.datetime.now().strftime("%w")
    if kind == 2 :
        if daytime == 1:
            ej += 'SELECT teachers_table.teacher FROM time_table JOIN teachers_table ON teachers_table.id = time_table.teacher_id AND time_table.day_id = '+str(day)
        if daytime == 2:
            ej += 'SELECT teachers_table.teacher FROM time_table JOIN teachers_table ON teachers_table.id = time_table.teacher_id AND time_table.day_id = '+str(int(day)+1)
    if kind == 3 :
        if daytime == 1:
            ej += 'SELECT lect_table.lect FROM time_table JOIN lect_table ON lect_table.id = time_table.lect_id AND time_table.day_id = '+day
        if daytime == 2:
            ej += 'SELECT lect_table.lect FROM time_table JOIN lect_table ON lect_table.id = time_table.lect_id AND time_table.day_id = '+str(int(day)+1)
    if kind == 1:
        cur = sqlite3.connect('tt.sqlite').cursor()
        if daytime == 1:
            cur.execute('SELECT time_table.time FROM time_table WHERE time_table.day_id = ?',day)
        if daytime == 2:
            print('yes')
            cur.execute('SELECT time_table.time FROM time_table WHERE time_table.day_id = ?',str(int(day)+1))
        c = 0
        for i in cur:
            c += 1
        if c == 0:
            print('No class today')
            return
        print('today there are',c,'classes')
        return 0
    cur = sqlite3.connect('tt.sqlite').cursor()
    cur.execute(ej)
    c = 0
    for i in cur:
        c+=1
        print(i[0])
    if c == 0:
        print('No class today, take a chill pill')

def anyday(kind,day):
    cur = sqlite3.connect('tt.sqlite').cursor()
    if kind == 3:
        ej = 'SELECT lect_table.lect FROM time_table JOIN lect_table JOIN day_table ON lect_table.id = time_table.lect_id AND day_table.id = time_table.day_id AND day_table.day = \''+day+'\''
    if kind == 2:
        ej = 'SELECT teachers_table.teacher FROM time_table JOIN lect_table JOIN teachers_table JOIN day_table ON lect_table.id = time_table.lect_id AND teachers_table.id = lect_table.teacher_id AND day_table.id = time_table.day_id and day_table.day = \''+day+'\''
    if kind == 1:
        ej = 'SELECT time_table.time FROM time_table JOIN day_table ON time_table.day_id = day_table.id and day_table.day = \''+day+'\''
    cur.execute(ej)
    c = 0
    for i in cur:
        c +=1
        if kind == 1:
            continue
        print(i[0])
    if kind == 1:
        print('There are total',c,'classes on',day)
    else:
        if c == 0:
            print('No classes on selected day!')

def confusion(day,lect):
    cur = sqlite3.connect('tt.sqlite').cursor()
    if day == 'today':
        m = int(datetime.datetime.now().strftime('%w'))
    if day == 'tomorrow':
        m = int(datetime.datetime.now().strftime('%w'))+1
    if day == 'today' or day == 'tomorrow':
        cur.execute('SELECT time_table.time FROM time_table JOIN lect_table WHERE lect_table.id = time_table.lect_id AND time_table.day_id = '+str(m)+' AND lect_table.lect = \''+lect+'\'')
        if cur.fetchone() != None:
            print('YES')
        else:
            print('NO')
        return
    else:
        cur.execute('SELECT time_table.time FROM time_table JOIN lect_table JOIN day_table WHERE lect_table.id = time_table.lect_id AND day_table.id = time_table.day_id AND day_table.day = \''+day+'\' AND lect_table.lect = \''+lect+'\'')
        if cur.fetchone() != None:
            print('YES')
        else:
            print('NO')
        return
def dictionary(string):
    word = string.replace('of','')
    word=word.replace('meaning','')
    word=word.replace('mean','')
    word=word.replace('means','')
    word=word.replace('the','')
    word=word.replace('what','')
    word=word.replace('is','')
    word=word.replace('word','')
    word=word.replace(' a ','')
    word = word.strip()
    site = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'+word
    try:
        fhand = urllib.request.urlopen(site, context=ctx)
        info = json.loads(fhand.read().decode())
    except:
        print('Sorry I couldn\'t find this word')
        speak('Sorry I couldn\'t find this word')
        quit()
    meaning = info[0]['meanings'][0]['definitions'][0]['definition']
    example =info[0]['meanings'][0]['definitions'][0]['example']
    print('Meaning of '+word+' is :'+meaning)
    speak('Meaning of '+word+' is :'+meaning)
    print('For example, '+example)
    speak('For example, '+example)
if __name__ == "__main__":

    speak('Sir, I am love, How may I help you')
    while True:
        query = takeCommand()
        if query is None:
            continue
        query = query.lower()
        print(query)
#Tells_time
        if 'time' in query :
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print('Sir, the time is ',strTime)
            speak('Sir, the time is ')
        elif 'sing a song' in query:
            speak('Give Me Freedom, Give me Fire, Give me reason, Take me higher, See the champions, Take the feild now, You define us, make us feel proud')
#GOOGLE CLASSROOMS
        elif 'google classroom' in query:
                m = google_classroom(query)
                if m == None:
                    speak('which one? Here are some options...\n')
                    print("Vivek sir, instrumentation\nHari sir, electrical machines\nkailash sir, gep, generation of electrical power\ngeeta mam, numerical methods, nm\n jagvinder sir, hcmi, economics in engineering")
                    query = takeCommand().lower()
                    n = google_classroom(query)
                    if n == None:
                        speak('opening google classroom...')
                        webbrowser.open('https://classroom.google.com/h')

#complaints
        elif query.strip() == 'open':
            speak('Open what?')
            ip = takeCommand()
            while ip is None:
                continue
            ip = ip.lower()

#meaning of word
        elif 'meaning' in query or 'means' in query:
            dictionary(query)

#Timetable begins here
        elif 'which' in query and 'class' in query and 'now' in query:
            dia = timetable('lect')
            print(dia)
        #    speak(dia)
        elif 'whose' in query and 'class' in query and 'now' in query:
            dia = timetable('whose')
            print(dia)
        #    speak(dia)
        elif 'which' in query and 'class' in query and 'next' in query:
            dia = timetable('next_c')
            print(dia)
        elif 'whose' in query and 'class' in query and 'next' in query:
            dia = timetable('next_t')
            print(dia)
        elif 'what' in query and 'class' in query and 'today' in query:
            cur = sqlite3.connect('tt.sqlite').cursor()
            day = datetime.datetime.now().strftime("%A")
            ej = 'SELECT time_table.time FROM time_table JOIN day_table ON time_table.day_id = day_table.id AND day_table.day = \''+day+'\''
            s = cur.execute(ej)
            for i in s:
                print(i[0])
        elif 'how many' in query and 'class' in query and 'tomorrow' in query:
            kindings(2,1)
        elif 'how many' in query and 'class' in query and 'today' in query:
            kindings(1,1)
        elif 'whose' in query and 'class' in query and 'today' in query:
            kindings(1,2)
        elif 'which' in query and 'class' in query and 'tomorrow' in query:
            kindings(2,3)
        elif 'whose' in query and 'class' in query and 'tomorrow' in query:
            kindings(2,2)
        elif 'which' in query and 'class' in query and 'today' in query:
            kindings(1,3)
        elif 'which' in query and 'class' in query and 'day' in query and 'today' not in query:
            for i in query.split():
                if 'day' in i:
                    x = i
            anyday(3,x.lower())
        elif 'whose' in query and 'class' in query and 'day' in query and 'today' not in query:
            for i in query.split():
                if 'day' in i:
                    x = i
            anyday(2,x.lower())
        elif 'how many' in query and 'class' in query and 'day' in query and 'today' not in query:
            for i in query.split():
                if 'day' in i:
                    x = i
            anyday(1,x.lower())
        elif ('is there' in query or 'will there' in query or 'was there')and ('class' in query or 'tut' in query):
            cur = sqlite3.connect('tt.sqlite').cursor()
            lect = ''
            day = ''
            for i in query.split():
                if 'tomorrow' == i:
                    day = i
                if i == 'today':
                    day = i
            for j in query.split():
                cur.execute('SELECT lect FROM lect_table WHERE lect = \''+j+'\'')
                x = cur.fetchone()
                if x != None:
                    lect = x[0]
                    break
            confusion(day,lect)
#open(whatsapp)
        elif 'open whatsapp' in query:
            to = 'C:\\Users\\Manish\\AppData\\Local\\WhatsApp\\Whatsapp.exe'
            os.startfile(to)
            speak('I think i should leave now...May i go sir?')
            lis = takeCommand().lower()
            if lis in ['ok','ok go','yes','yes go','ok you may go','yes you should go','yes you may go']:
                exit()
            else:
                speak('Okay, how may i help you sir?')
                continue
#Wikipedia
        elif 'search' in query and 'on wikipedia' in query:
            query = query.replace("search","")
            query = query.replace("wikipedia","")
            site = 'https://en.wikipedia.org/wiki/'
            site = encodes(query,site,'_')
            webbrowser.open(site)
#GoogleSearch
        elif 'search'in query and 'on google' in query:
            query = query.replace("search","")
            query = query.replace("on google","")
            site = 'https://www.google.com/search?q='
            site = encodes(query,site,None)
            webbrowser.open(site)
#YoutubeSearch
        elif 'open' in query and 'on youtube' in query:
            query = query.replace ("open","")
            query = query.replace("on youtube","")
            site = 'https://www.youtube.com/results?search_query='
            site = encodes(query,site,None)
            webbrowser.open(site)
#My_channel
        elif 'open my youtube channel' in query:
            speak('Opening your channel')
            webbrowser.open('https://www.youtube.com/channel/UCUNvfBwUnbme1W7J544CeVQ')
            time.sleep(10)
#Youtube
        elif 'open youtube' in query:
            speak('Opening youtube...')
            webbrowser.open('www.youtube.com')
            time.sleep(10)
#Hello_command
        elif 'hello' in query:
            speak ('Hello sir, Would you like to listen a joke?')
            s = takeCommand()
            if 'yes' in s:
                speak('a joke LOL')
                print('A JOKE LOL')
            else:
                print('No issues sir')
                speak('No issues sir')
#THANKYOU
        elif 'thank you' in query:
            ty = ['Thankyou for opting me','may i need to do something else','Most welcome, How may I help you?']
            speak('Thank you sir for opting me')
#HOW_are_you_love
        elif 'how are you' in query:
            speak('I am Good sir, What about you?')
#exit
        elif 'leave' in query:
            speak('Sionara sir')
            exit()
#email
        elif 'email' in query:
            speak('To whom sir? here are some contacts of your')
            fhand = open('cont.json')
            info = json.loads(fhand.read())
            for item in info['contacts']:
                print(item['name'])
            time.sleep(2)
            who = takeCommand().lower()
            for i in info["contacts"]:
                if who == i["name"]:
                    to = i["email"]
                    print(who)
                    break
            try:
                speak("What to write in email")
                content = takeCommand()
                if 'cancel this email' in content:
                    speak('canceling the email...')
                    time.sleep(2)
                    continue
                print('\n\n\n',content)
                speak('Are you sure you want to send this email?, you can take time for 10 seconds')
                s = takeCommand()
                if 'no' in query:
                    continue
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                speak("Sorry sir. I am not able to send this email")
            time.sleep(2)
#pause
        elif 'pause' in query:
            speak('Okay sir, 2 minutes pause')
            time.sleep(120)
        elif 'play' in query or 'song' in query:
            query = query.replace('play','')
            query = query.replace('song','')
            query = query.replace('a','')
            query = query.replace('random','')
            query = query.replace('one','')
            query = query.strip()
            music_dir = 'M:\\Songs'
            songs = os.listdir(music_dir)
            n = len(songs)
            if query == '':
                dir = music_dir+'\\'+songs[random.randint(0,n-1)]
                speak('Playing a song')
                os.startfile(dir)
                print('Leaving...')
                quit()
            else:
                check = ''
                c = 0
                for i in query.split():
                    for j in songs:
                        if i in j:
                            speak('Playing '+ query)
                            os.startfile(music_dir+'\\'+j)
                            c += 1
                            break
                    if c == 1:
                        break
                print('Leaving...')
                quit()
        elif 'do you love me' in query or 'do you like me' in query:
            a = 'Sorry I am commited to alexa, go see your face in mirror and then talk to me'
            print(a)
#if_none_of_above
        elif query == None:
            speak('Sorry sir, could you please repeat yourself')
#if didn't recognize
        else:
            query = query.replace('what','')
            query = query.replace('is','')
            query = query.replace('the','')
            query = query.replace('are','')
            query = query.replace('who','')
            query = query.replace('will','')
            query = query.replace('shall','')
            query = query.replace('be','')
            query = query.strip()
            wiki_wiki = wikipediaapi.Wikipedia('en')
            page_py = wiki_wiki.page(query)
            if page_py.exists() == True:
                sentence = page_py.summary[:4000]
                c = 0
                m = 0
                for i in range(500):
                    if sentence[i] == '.' and sentence[i+1] != '.' and sentence[i+2] != '.':
                        c += 1
                        if c == 2:
                            m = i
                            break
                result = 'According to wikipedia,' + sentence[:m+1]
                print(result)
                speak(result)
            else:
                speak('Sorry sir I don\'t know about this. Do you want me to search this on google?')
                try:
                    dec = takeCommand().lower()
                except:
                    speak('didn\'t get it sir. How can I help you')
                    continue
                    if 'yes' in dec or 'yeah' in dec:
                        speak('sure sir...')
                        to = 'https://www.google.com/search?q='
                        webbrowser.open(encodes(query,to,None))
                        time.sleep(20)
                        speak('I am back do you need any other help??')
                    else:
                        speak('Okay, so how may I help you?')
                        fhand = open('complaints.txt','a')
                        fhand.write('-> '+ query+'\n')
                        fhand.close()
