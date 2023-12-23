import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import os
import csv
import pandas as pd
from scipy.interpolate import UnivariateSpline
from PIL import Image
#from matteo3 import setup, left, plot, nw, wo, meals, check, check_setup, check_language, database_update, database_search, add_user_name, select_first_user, select_user,past_meals,simulation



# if you want to use emoji, you can find the codes here: https://www.webfx.com/tools.emoji-cheat-sheet/

st.set_page_config(page_title="Dietly", layout="wide") # normalmente il layout di una pagina e' centrato. Mettendo "wide" stai usando tutta la pagina


#--------ORA L'HEADER---
with st.container(): #serve solo per separare l'header dal resto, ma non e' necessario
    st.title("Dietly")
    st.subheader("The app to monitor your daily intake of calories.")


st.write("In this page goes the choice of the User and the Setup function.")

"""
- Try and understand why you need to press the " Add User" and "Aggiorna" buttons twice to confirm. (sono teoricamente due "submit" buttons, anche se "Add User" non lo e' propriamente)
- Try to understand how the "setup" button works: right now, if you press it for one user, it stays on for all the later users, untill you push the "update" button.
- Similarly, if you decide to upload a differen user image, make it so that the old one disappears.
- Work on the "if core not in arr" part.
- Add the connection to google translate.
- Add the possibility to take a picture to connect to the user. The command is st.camera_input("").
- Instead of simply printing "Fatto" when you accomplish something, use the st.success("Fatto!") command. It does the same thing but it looks nicer.
- insert the calories in a session_state (last lines of this script).
"""

arr = os.listdir('.')
pic_arr = os.listdir('./foto')

today = date.today()
today=today.strftime("%d_%m_%Y")
extracal=0
new_user='eMpTy'

@st.cache_data
def load_image(image_file):
    img = Image.open(image_file)
    return(img)


if 'core.npy' not in arr:
    in_core = np.rec.array([1400.0,350.0,490.0,560.0,'eng','NoNe'], names=['top','top_red','top_yellow','top_green','lang','user'])
    print('')
    first_usr = add_user_name(in_core)
    print('Welcome to Dietly, '+first_usr+'! Benvenuto/a su Dietly, '+first_usr+'! Bienvenido/a en Dietly, '+first_usr+'!')
    print('')
    core2 = np.rec.array([1400.0,350.0,490.0,560.0,'eng',first_usr], names=['top','top_red','top_yellow','top_green','lang','user'])
    usr_msk = (core2['user'] == first_usr)
    initial_top,initial_top_red,initial_top_yellow,initial_top_green=core2[usr_msk][0][0],core2[usr_msk][0][1],core2[usr_msk][0][2],core2[usr_msk][0][3]
    initial_red,initial_yellow,initial_green=0.0,0.0,0.0
    core,top,top_red,top_yellow,top_green,usr = setup(arr,core2,today,initial_top,initial_top_red,initial_top_yellow,initial_top_green,initial_red,initial_yellow,initial_green,first_usr,extracal)
    usr_msk = (core['user'] == usr)
    if core[usr_msk][0][4]=='eng':
        print('What is your initial weight (in Kg)?')
    if core[usr_msk][0][4]=='ita':
        print('Qual è il tuo peso iniziale (in Kg)?')
    if core[usr_msk][0][4]=='esp':
        print('Cual es tu peso inicial (en Kg)?')
    in_weight = input('')
    if in_weight==str(''):
        in_weight=86.0
    else:
        in_weight=float(in_weight)
    print('')
    days, weight = np.rec.array([str(usr),today], names=['user','date']), np.rec.array([str(usr),in_weight], names=['user','weight'])
    np.save('days.npy',days)
    np.save('weight.npy',weight)
    top=float(core[usr_msk][0][0])
    top_red=float(core[usr_msk][0][1])
    top_yellow=float(core[usr_msk][0][2])
    top_green=float(core[usr_msk][0][3])
    red,yellow,green=0.0,0.0,0.0
    if core[usr_msk][0][4]=='eng':
        print('Would you like to start using Dietly?')
    if core[usr_msk][0][4]=='ita':
        print('Vuoi iniziare ad usare Dietly?')
    if core[usr_msk][0][4]=='esp':
        print('Quieres empiezar a usar Dietly?')
    start = input('')
    if start==str(''):
        start='si'
    start=check(start,core[usr_msk][0][4])
    print('')
    if start == 'y' or start == 'yes' or start == 'si' or start == 's' or start == 'yep' or start == 'eja' or start == '':
        c=1
        arr = os.listdir('.')
        df = pd.DataFrame({'top': [top], 'red_left': [top_red], 'yellow_left': [top_yellow], 'green_left': [top_green], 'red': [0], 'yellow': [0], 'green': [0], 'ingredients': [str('-')], 'calories': [0], 'color': [str('-')], 'meal': [str('-')]})
        df.to_csv(usr+'_'+today+'.csv',index=False)
    if start == 'no' or start == 'n' or start == 'nop' or start == 'nope':
        c=0
        print('Salvarì!')
        print('')
else:
    weight=np.load('weight.npy',allow_pickle=True)
    days=np.load('days.npy',allow_pickle=True)
    core=np.load('core.npy',allow_pickle=True)
    
    users = core['user']
    users = np.append(users,'new')
    #to store a variable into a session_state, you first have to declare it; then you place the widget, and then you can define a variable to be equal to st.session_state.whatever_variable.
    if "usr" in st.session_state and st.session_state.usr != 'new' and  st.session_state.usr != None:
        ix=int(np.where(users == str(st.session_state.usr))[0])
    
    if "usr" not in st.session_state or st.session_state.usr == 'new' or  st.session_state.usr == None: #it's possible that, when you'll have to deal with the "if core not in arr" part, you will have to move this line and the next one up above
        st.session_state.usr = 'XXX'
        ix = None



    col1,col2 = st.columns([1,1.5])
    st.session_state.usr = col1.selectbox("",(users),index=ix, placeholder= "What is your Username?")
    usr = st.session_state.usr
    if "setup_index" not in st.session_state:
        st.session_state.setup_index = 0

    if "change_index" not in st.session_state:
        st.session_state.change_index = 0

if usr == 'new':
    
    temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user = core['top'],core['top_red'],core['top_yellow'],core['top_green'],core['lang'],core['user']
    new_user = col1.text_input('',placeholder="Insert New Username")
    if str(new_user) in temp_user:
        col1.write("The chosen Username is already being used. Please choose a different one.")
    
    if str(new_user) not in temp_user and str(new_user) != '':
        new_lan = col1.radio("What language would you like to select?",("Eng","Ita","Esp"))
        if new_lan == 'Eng':
            new_top = col1.number_input("Maximum daily calories",0,10000,1500,step = 1)
            new_perc_red = (col1.slider("Percentage of RED calories",0,100,25))
            def_yellow = min((35,100-new_perc_red))
            new_perc_yellow = (col1.slider("Percentage of YELLOW calories",0,100-new_perc_red,def_yellow))
        if new_lan == 'Ita':
            new_top = col1.number_input("Calorie massime giornaliere",0,10000,1500,step = 1)
            new_perc_red = col1.slider("Percentuale di calorie ROSSE",0,100,25)
            def_yellow = min((35,100-new_perc_red))
            new_perc_yellow = col1.slider("Percentuale di calorie GIALLE",0,100-new_perc_red,def_yellow)
        if new_lan == 'Esp':
            new_top = col1.number_input("Calorias diarias maximas",0,10000,1500,step = 1)
            new_perc_red = col1.slider("Porcentaje de calorias ROJAS",0,100,25)
            def_yellow = min((35,100-new_perc_red))
            new_perc_yellow = col1.slider("Porcentaje de calorias AMARILLAS",0,100-new_perc_red,def_yellow)

        new_top_red, new_top_yellow, new_top_green = 0.0,0.0,0.0
        new_perc_green = 100.0-new_perc_red-new_perc_yellow
        new_top_red, new_top_yellow, new_top_green = int(new_top*new_perc_red/100), int(new_top*new_perc_yellow/100), int(new_top*new_perc_green/100)
        red,yellow,green=0.0,0.0,0.0
        if new_lan == 'Eng':
            add_user = st.button("Add New User")
        if new_lan == 'Ita':
            add_user = st.button("Aggiungi Nuovo Utente")
        if new_lan == 'Esp':
            add_user = st.button("Agrega Nuevo Usuario")
            
        if add_user:
            temp_top, temp_topred, temp_topyellow, temp_topgreen, temp_lan, temp_user = np.append(temp_top,new_top), np.append(temp_topred,new_top_red), np.append(temp_topyellow,new_top_yellow), np.append(temp_topgreen,new_top_green), np.append(temp_lan,new_lan), np.append(temp_user,str(new_user))
            ix = np.argsort(temp_user)
            temp_top, temp_topred, temp_topyellow, temp_topgreen, temp_lan, temp_user = temp_top[ix], temp_topred[ix], temp_topyellow[ix], temp_topgreen[ix], temp_lan[ix], temp_user[ix]
            core = np.rec.array([temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user], names=['top','top_red','top_yellow','top_green','lang','user'])
            usr = str(new_user)
            np.save("core.npy",core)
            
    
usr_msk = (core['user'] == usr)
usr_days_msk = (days['user'] == usr)
usr_weight_msk = (weight['user'] == usr)

if usr != 'new' and usr != None and usr != str(new_user):
    
    if core[usr_msk]['lang'] == 'Eng' or core[usr_msk]['lang'] == 'eng':
        setup = col1.button('Setup')
    if core[usr_msk]['lang'] == 'Ita' or core[usr_msk]['lang'] == 'ita':
        setup = col1.button('Impostazioni')
    if core[usr_msk]['lang'] == 'Esp' or core[usr_msk]['lang'] == 'esp':
        setup = col1.button('Configuración')
    
    #if setup: #CREDO CHE CI SIANO DEI PROBLEMI CON I PULSANTI ED I "NESTED IF": INFATTI, SE IO CLICCO IL PULSANTE SETUP, QUESTO SARA' TRUE. MA QUANDO POI CREO LA FORM E CI ENTRO, IL PULSANTE SETUP DIVENTA OFF, IL CHE' INFICIA TUTTO CIO' CHE FACCIO DOPO. GUARDA DI NUOVO IL VIDEO SUI SESSION STATES.  UPDATE: WITH THE IMPLEMENTATION OF SESSIONS, IT WORKS
    if setup:
        st.session_state.setup_index = 1
    if st.session_state.setup_index == 1:
        with col1.form(key='SETUP'):
            if core[usr_msk]['lang'] == 'Eng' or core[usr_msk]['lang'] == 'eng':
                temp_lan = st.radio("Which language would you like to switch to?",("Eng","Ita","Esp"), index=0)
                temp_top = st.number_input("Maximum daily calories",0.0,10000.0,float(core[usr_msk]['top']),step = 1.0)
                temp_perc_red = st.slider("Percentage of RED calories",0,100,int(core[usr_msk]['top_red']*100/core[usr_msk]['top']))
                temp_perc_yellow = st.slider("Percentage of YELLOW calories",0,100,int(core[usr_msk]['top_yellow']*100/core[usr_msk]['top']))
            
            if core[usr_msk]['lang'] == 'Ita' or core[usr_msk]['lang'] == 'ita':
                temp_lan = st.radio("Che lingua vorresti scegliere?",("Eng","Ita","Esp"), index=1)
                temp_top = st.number_input("Calorie massime giornaliere",0.0,10000.0,float(core[usr_msk]['top'][0]),step = 1.0)
                temp_perc_red = st.slider("Percentuale di calorie ROSSE",0,100,int(core[usr_msk]['top_red'][0]*100/core[usr_msk]['top'][0]))
                temp_perc_yellow = st.slider("Percentuale di calorie GIALLE",0,100,int(core[usr_msk]['top_yellow']*100/core[usr_msk]['top']))
            
            if core[usr_msk]['lang'] == 'Esp' or core[usr_msk]['lang'] == 'esp':
                temp_lan = st.radio("Que idioma querias elegir?",("Eng","Ita","Esp"), index=2)
                temp_top = st.number_input("Calorias diarias maximas",0.0,10000.0,float(core[usr_msk]['top'][0]),step = 1.0)
                temp_perc_red = st.slider("Porcentaje de calorias ROJAS",0,100,int(core[usr_msk]['top_red'][0]*100/core[usr_msk]['top'][0]))
                temp_perc_yellow = st.slider("Porcentaje de calorias AMARILLAS",0,100,int(core[usr_msk]['top_yellow']*100/core[usr_msk]['top']))
        
            temp_top_red, temp_top_yellow, temp_top_green = 0.0,0.0,0.0
            temp_perc_green = 100.0-temp_perc_red-temp_perc_yellow
            temp_top_red, temp_top_yellow, temp_top_green = int(temp_top*temp_perc_red/100), int(temp_top*temp_perc_yellow/100), int(temp_top*temp_perc_green/100)
            
            
            if core[usr_msk]['lang'] == 'Eng' or core[usr_msk]['lang'] == 'eng':
                app = st.form_submit_button('Apply Changes')
            if core[usr_msk]['lang'] == 'Ita' or core[usr_msk]['lang'] == 'ita':
                app = st.form_submit_button('Aggiorna')
            if core[usr_msk]['lang'] == 'Esp' or core[usr_msk]['lang'] == 'esp':
                app = st.form_submit_button('Actualizar')
            
            #aggiornamento del core E SALVATAGGIO:        
            if app:
                core_top, core_topred, core_topyellow, core_topgreen, core_lan, core_user = core['top'], core['top_red'], core['top_yellow'], core['top_green'], core['lang'], core['user']
                temp_usr_msk = (core_user == str(usr))
                core_top[temp_usr_msk], core_topred[temp_usr_msk], core_topyellow[temp_usr_msk], core_topgreen[temp_usr_msk], core_lan[temp_usr_msk] = temp_top, temp_top_red, temp_top_yellow, temp_top_green, temp_lan
                core = np.rec.array([core_top,core_topred,core_topyellow,core_topgreen,core_lan,core_user],names=['top','top_red','top_yellow','top_green','lang','user'])
                np.save("core.npy",core)       
                
                #aggiornamento del file .csv E SALVATAGGIO:
                if usr+'_'+today+'.csv' in arr and usr != 'new' and usr != None:
                    df = pd.read_csv(str(usr)+'_'+str(today)+'.csv',sep=",", header=None)
                    full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(df[0][1:]).astype(float), np.array(df[1][1:]).astype(float), np.array(df[2][1:]).astype(float), np.array(df[3][1:]).astype(float), np.array(df[4][1:]).astype(float), np.array(df[5][1:]).astype(float), np.array(df[6][1:]).astype(float), np.array(df[7][1:]), np.array(df[8][1:]).astype(float), np.array(df[9][1:]), np.array(df[10][1:])
                    
                    red, yellow, green = full_red[-1], full_yellow[-1], full_green[-1]
                    top, top_red, top_yellow, top_green = (temp_top - red - yellow - green), (temp_top_red - red), (temp_top_yellow - yellow), (temp_top_green - green)
                    full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal = np.append(full_top,top), np.append(full_top_red,top_red), np.append(full_top_yellow,top_yellow), np.append(full_top_green,top_green), np.append(full_red,red), np.append(full_yellow,yellow), np.append(full_green,green), np.append(full_ingr,str('-')), np.append(full_cal,0), np.append(full_color,str('-')),np.append(full_meal,str('-'))
                    dfw = pd.DataFrame({'top': full_top, 'red_left': full_top_red, 'yellow_left': full_top_yellow, 'green_left': full_top_green, 'red': full_red, 'yellow': full_yellow, 'green': full_green, 'ingredients': full_ingr, 'calories': full_cal, 'color': full_color, 'meal': full_meal})
                    dfw.to_csv(str(usr)+'_'+str(today)+'.csv',index=False)
                
                st.session_state.setup_index = 0


if str(usr)+'.jpg' not in pic_arr and usr != None and usr != '':
    if usr == 'new' or core[usr_msk]['lang'] == 'Eng' or core[usr_msk]['lang'] == 'eng':
        pic = col2.file_uploader("Upload a photo")
        #pic = col2.camera_input("")
    if core[usr_msk]['lang'] == 'Ita' or core[usr_msk]['lang'] == 'ita':
        pic = col2.file_uploader("Carica una foto")
    if core[usr_msk]['lang'] == 'Esp' or core[usr_msk]['lang'] == 'esp':
        pic = col2.file_uploader("Cargar una foto")
    if pic != None:
        if usr == 'new' and new_user != None and new_user != '' and new_user not in temp_user:
            pic.name = str(new_user)+'.jpg'
            file_details = {"FileName":pic.name,"FileType":pic.type}
            col2.write(pic.name)
            img = load_image(pic)
            col2.image(img)
            with open(os.path.join(f"foto",pic.name),"wb") as f:
                f.write(pic.getbuffer())
            col2.success("Photo succesfully uploaded and saved!")
        if usr != 'new':
            pic.name = str(usr)+'.jpg'
            file_details = {"FileName":pic.name,"FileType":pic.type}
            col2.write(pic.name)
            img = load_image(pic)
            col2.image(img, width = 350)
            with open(os.path.join(f"foto",pic.name),"wb") as f:
                f.write(pic.getbuffer())
            if core[usr_msk]['lang'] == 'Eng' or core[usr_msk]['lang'] == 'eng':
                col2.success("Photo succesfully uploaded and saved!")
            if core[usr_msk]['lang'] == 'Ita' or core[usr_msk]['lang'] == 'ita':
                col2.success("Foto caricata e salvata con successo!")
            if core[usr_msk]['lang'] == 'Esp' or core[usr_msk]['lang'] == 'esp':
                col2.success("Foto cargada y guardada correctamente!")


if str(usr)+'.jpg' in pic_arr:
    #f = open('./foto/'+str(usr)+'.jpg','wb')
    pic = Image.open(f'./foto/{usr}.jpg')
    #img = load_image(pic)
    col2.image(pic, width = 350)
    if core[usr_msk]['lang'] == 'Eng' or core[usr_msk]['lang'] == 'eng':
        change_pic = col2.button("Change User Picture")
    if core[usr_msk]['lang'] == 'Ita' or core[usr_msk]['lang'] == 'ita':
        change_pic = col2.button("Cambia Immagine Utente")
    if core[usr_msk]['lang'] == 'Esp' or core[usr_msk]['lang'] == 'esp':
        change_pic = col2.button("Cambiar Imagen Usuario")
    if change_pic: st.session_state.change_index = 1
    if st.session_state.change_index == 1:
        if core[usr_msk]['lang'] == 'Eng' or core[usr_msk]['lang'] == 'eng':
            pic = col2.file_uploader("Upload a photo")
        if core[usr_msk]['lang'] == 'Ita' or core[usr_msk]['lang'] == 'ita':
            pic = col2.file_uploader("Carica una foto")
        if core[usr_msk]['lang'] == 'Esp' or core[usr_msk]['lang'] == 'esp':
            pic = col2.file_uploader("Cargar una foto")
        if pic != None:
            pic.name = str(usr)+'.jpg'
            file_details = {"FileName":pic.name,"FileType":pic.type}
            col2.write(pic.name)
            img = load_image(pic)
            col2.image(img, width = 350)
            os.remove(f"./foto/{pic.name}")
            with open(os.path.join(f"foto",pic.name),"wb") as f:
                f.write(pic.getbuffer())
            if core[usr_msk]['lang'] == 'Eng' or core[usr_msk]['lang'] == 'eng':
                col2.success("Photo succesfully uploaded and saved!")
            if core[usr_msk]['lang'] == 'Ita' or core[usr_msk]['lang'] == 'ita':
                col2.success("Foto caricata e salvata con successo!")
            if core[usr_msk]['lang'] == 'Esp' or core[usr_msk]['lang'] == 'esp':
                col2.success("Foto cargada y guardada correctamente!")
            st.session_state.change_index = 0

if str(usr)+'_'+today+'.csv' not in arr and usr != 'new' and usr != None:
    top=float(core[usr_msk][0][0])
    top_red=float(core[usr_msk][0][1])
    top_yellow=float(core[usr_msk][0][2])
    top_green=float(core[usr_msk][0][3])
    red,yellow,green=0.0,0.0,0.0
    df = pd.DataFrame({'top': [top], 'red_left': [top_red], 'yellow_left': [top_yellow], 'green_left': [top_green], 'red': [red], 'yellow': [yellow], 'green': [green], 'ingredients': ['-'], 'calories': [0], 'color':['-'], 'meal': ['-']})
    df.to_csv(str(usr)+'_'+str(today)+'.csv',index=False)

if str(usr)+'_'+today+'.csv' in arr and usr != 'new' and usr != None:
    df = pd.read_csv(str(usr)+'_'+str(today)+'.csv',sep=",", header=None)
    full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(df[0][1:]).astype(float), np.array(df[1][1:]).astype(float), np.array(df[2][1:]).astype(float), np.array(df[3][1:]).astype(float), np.array(df[4][1:]).astype(float), np.array(df[5][1:]).astype(float), np.array(df[6][1:]).astype(float), np.array(df[7][1:]), np.array(df[8][1:]).astype(float), np.array(df[9][1:]), np.array(df[10][1:])
    top, top_red, top_yellow, top_green, red, yellow, green=full_top[-1], full_top_red[-1], full_top_yellow[-1], full_top_green[-1], full_red[-1], full_yellow[-1], full_green[-1]










