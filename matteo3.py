import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import os
import csv
from astropy.io import fits
import pandas as pd
from scipy.interpolate import UnivariateSpline


#allows you to add the first user
def add_user_name(core):
    cc=1
    while cc==1:
        print("New User's name: ")
        print("Nuovo nome Utente: ")
        print("Nuevo nombre Usuario: ")
        print("")
        gg=0
        while gg==0:
            name = str(input(''))
            print('')
            if str(name) in core['user']:
                print('The chosen Username is already being used. Please, choose another one.')
                print('Il nome utente è già in uso. Indicarne un altro.')
                print('El nombre del usuario elegido ya existe. Por favor, eligen otro nombre.')
                print('')
                gg=0
            else: gg=1
        print('')
        print("The user's name is "+name+", correct?")
        print("Il nome utente è "+name+", corretto?")
        print("El nombre del usuario es "+name+", correcto?")
        print('')
        confirm_name = input('')
        xx=1
        while xx==1:
            if confirm_name != 'y' and confirm_name != 'yes' and confirm_name != 'si' and confirm_name != 's' and confirm_name != 'yep' and confirm_name != 'eja' and confirm_name != 'no' and confirm_name != 'n' and confirm_name != 'nop' and confirm_name != 'nope':
                print('Sorry, could you repeat?')
                print('Non ho capito, puoi ripetere?')
                print('Lo siento, puedes repetir?')
                confirm_name = input('')
                xx=1
            else: xx=0
        if confirm_name == 'y' or confirm_name == 'yes' or confirm_name == 'si' or confirm_name == 's' or confirm_name == 'yep' or confirm_name == 'eja' or confirm_name == '':
            print('')
            cc=0
        if confirm_name == 'no' or confirm_name == 'n' or confirm_name == 'nop' or confirm_name == 'nope':
            cc=1
    return(name)



#select the first user, at the opening of dietly
def select_first_user(core,arr,today,days,weight,extracal):
    print('Users list:')
    print('Lista Utenti:')
    print('Lista Usuarios:')
    print('')
    print(core['user'])
    print('')
    print("If you are among them, type your User name; otherwise type 'add'.")
    print("Se sei uno di questi Utenti, scrivi il tuo nome Utente; altrimenti, scrivi 'agg'.")
    print("Si uno de estos Usuarios, escribe tu Usuario; de lo contrario, escribe 'agr'.")
    print('')
    temp_usr = str(input(''))
    print('')
    bb = 0
    while bb == 0:
        if temp_usr in core['user']:
            usr = temp_usr
            usr_msk=(core['user']==usr)
            if core[usr_msk][0][4] == 'eng':
                print('Welcome back, '+usr)
                print('')
            if core[usr_msk][0][4] == 'ita':
                print('Bentornato/a, '+usr)
                print('')
            if core[usr_msk][0][4] == 'esp':
                print('Bienvenido/a de vuelta, '+usr)
                print('')
            if str(usr)+'_'+str(today)+'.csv' not in arr:
                top=float(core[usr_msk][0][0])
                top_red=float(core[usr_msk][0][1])
                top_yellow=float(core[usr_msk][0][2])
                top_green=float(core[usr_msk][0][3])
                red,yellow,green=0.0,0.0,0.0
                df = pd.DataFrame({'top': [top], 'red_left': [top_red], 'yellow_left': [top_yellow], 'green_left': [top_green], 'red': [red], 'yellow': [yellow], 'green': [green], 'ingredients': ['-'], 'calories': [0], 'color':['-'], 'meal': ['-']})
                df.to_csv(str(usr)+'_'+str(today)+'.csv',index=False)
            bb=1
        if temp_usr == 'add' or temp_usr == 'agg' or temp_usr == 'agr':
            core,top,top_red,top_yellow,top_green,usr = setup(arr,core,today,1400.0,350.0,490.0,560.0,0.0,0.0,0.0,temp_usr,extracal)
            usr_msk=(core['user']==usr)
            if core[usr_msk][0][4]=='eng':
                print('What is your initial weight (in Kg)?')
            if core[usr_msk][0][4]=='ita':
                print('Qual è il tuo peso iniziale (in Kg)?')
            if core[usr_msk][0][4]=='esp':
                print('Cual es tu peso inicial (en Kg)?')
            cc=0
            while cc==0:
                in_weight = input('')
                try:
                    in_weight=float(in_weight)
                except:
                    if core[usr_msk][0][4] == 'eng':
                        print('Sorry, could you repeat?')
                    if core[usr_msk][0][4] == 'ita':
                        print('Non ho capito, puoi ripetere?')
                    if core[usr_msk][0][4] == 'esp':
                        print('Lo siento, puedes repetir?')
                    cc=0
                else:
                    in_weight=float(in_weight)
                    cc=1
                
            temp_days_user, temp_days_date = days['user'], days['date']
            temp_weight_user, temp_weight_weight = weight['user'], weight['weight']
            temp_days_user, temp_days_date = np.append(temp_days_user,str(usr)), np.append(temp_days_date,today)
            temp_weight_user, temp_weight_weight = np.append(temp_weight_user,str(usr)), np.append(temp_weight_weight,float(in_weight))
            days, weight = np.rec.array([temp_days_user,temp_days_date], names=['user','date']), np.rec.array([temp_weight_user,temp_weight_weight], names=['user','weight'])
            np.save('days.npy',days)
            np.save('weight.npy',weight)
            df = pd.DataFrame({'top': [top], 'red_left': [top_red], 'yellow_left': [top_yellow], 'green_left': [top_green], 'red': [0], 'yellow': [0], 'green': [0], 'ingredients': ['-'], 'calories': [0], 'color':['-'], 'meal': ['-']})
            df.to_csv(str(usr)+'_'+str(today)+'.csv',index=False)
            print('')
            bb=1
        if temp_usr not in core['user'] and (temp_usr != 'add' and temp_usr != 'agg' and temp_usr != 'agr'):
            print('Sorry, could you repeat?')
            print('Non ho capito, puoi ripetere?')
            print('Lo siento, puedes repetir?')
            print('')
            temp_usr = str(input(''))
    return(usr,core,days,weight)


#change, add or delete a user
def select_user(core,arr,today,days,weight,user,extracal):
    usr_msk=(core['user']==user)
    if core[usr_msk][0][4] == 'eng':
        print('Users list:')
    if core[usr_msk][0][4] == 'ita':
        print('Lista Utenti:')
    if core[usr_msk][0][4] == 'esp':
        print('Lista Usuarios:')
    print('')
    print(core['user'])
    print('')
    if core[usr_msk][0][4] == 'eng':
        print("If you are among them, type your User name; otherwise type 'add' to add a new User, or 'del' to delete one.")
    if core[usr_msk][0][4] == 'ita':
        print("Se sei uno di questi Utenti, scrivi il tuo nome Utente; altrimenti, scrivi 'agg' per aggiungere un nuovo Utente, o 'canc' per cancellarne uno.")
    if core[usr_msk][0][4] == 'esp':
        print("Si uno de estos Usuarios, escribe tu nombre; de lo contrario, escribe 'agr' para agregar un nuevo Usuario, o 'canc' para eliminar uno de esos.")
    print('')
    temp_usr = str(input(''))
    print('')
    bb = 0
    while bb == 0:
        if temp_usr in core['user']:
            usr = temp_usr
            usr_msk=(core['user']==usr)
            if core[usr_msk][0][4] == 'eng':
                print('Welcome back, '+usr)
            if core[usr_msk][0][4] == 'ita':
                print('Bentornato/a, '+usr)
            if core[usr_msk][0][4] == 'esp':
                print('Bienvenido/a de vuelta, '+usr)
            print('')
            if str(usr)+'_'+str(today)+'.csv' not in arr:
                top=float(core[usr_msk][0][0])
                top_red=float(core[usr_msk][0][1])
                top_yellow=float(core[usr_msk][0][2])
                top_green=float(core[usr_msk][0][3])
                red,yellow,green=0.0,0.0,0.0
                df = pd.DataFrame({'top': [top], 'red_left': [top_red], 'yellow_left': [top_yellow], 'green_left': [top_green], 'red': [red], 'yellow': [yellow], 'green': [green], 'ingredients': ['-'], 'calories': [0], 'color':['-'], 'meal': ['-']})
                df.to_csv(str(usr)+'_'+str(today)+'.csv',index=False)
            bb=1
        if temp_usr == 'del' or temp_usr == 'canc':
            usr_msk=(core['user']==str(user))
            if core[usr_msk][0][4] == 'eng':
                print("Which User would you like to delete? (Press 'Enter' to move on).")
            if core[usr_msk][0][4] == 'ita':
                print("Quale Utente vorresti eliminare? (Premere 'Enter' per andare avanti).")
            if core[usr_msk][0][4] == 'esp':
                print("Que Usuario quieres eliminar? (Pulse 'Enter' para salir).")
            rr=0
            while rr==0:
                user_del=input('')
                print('')
                if user_del == str(''):
                    rr=1
                if str(user_del) not in core['user'] and str(user_del) != str(''):
                    if core[usr_msk][0][4] == 'eng':
                        print("The chosen User is not in the list. Please, specify another User")
                    if core[usr_msk][0][4] == 'ita':
                        print("L'Utente selezionato non è nella lista. Per favore, indicare un altro Utente")
                    if core[usr_msk][0][4] == 'esp':
                        print('El Usuario elegido no està en la lista. Por favor, elegir otro Usuario.')
                    print('')
                    rr=0
                if str(user_del) in core['user']:
                    if core[usr_msk][0][4] == 'eng':
                        print("Would you like to delete "+str(user_del)+" from the list of Users?")
                    if core[usr_msk][0][4] == 'ita':
                        print("Vorresti eliminare "+str(user_del)+" dalla lista degli Utenti?")
                    if core[usr_msk][0][4] == 'esp':
                        print("Querias eliminar "+str(user_del)+" de la lista de los Usuarios?")
                    conf=input('')
                    print('')
                    conf=check(conf,core[usr_msk][0][4])
                    if conf == 'y' or conf == 'yes' or conf == 'si' or conf == 's' or conf == 'yep' or conf == 'eja' or conf == '':
                        usr_delete_msk=(core['user']==user_del)
                        usr_delete_days_msk = (days['user'] == user_del)
                        usr_delete_weight_msk = (weight['user'] == user_del)
                        core, weight, days = core[~usr_delete_msk],weight[~usr_delete_weight_msk],days[~usr_delete_days_msk]
                        np.save('days.npy',days)
                        np.save('weight.npy',weight)
                        np.save('core.npy',core)
                        rr=1
                    if conf == 'no' or conf == 'n' or conf == 'nop' or conf == 'nope':
                        if core[usr_msk][0][4] == 'eng':
                            print("Please, specify another User (press 'Enter' to move on).")
                        if core[usr_msk][0][4] == 'ita':
                            print("Per favore, selezionare un altro Utente (Premere 'Enter' per andare avanti).")
                        if core[usr_msk][0][4] == 'esp':
                            print("Por favor, elegir otro Usuario (Pulse 'Enter' para salir).")
                        rr=0
                        print('')
            bb=1
            return(user,core,days,weight)

        
        if temp_usr == 'add' or temp_usr == 'agg' or temp_usr == 'agr':
            core,top,top_red,top_yellow,top_green,usr = setup(arr,core,today,1400.0,350.0,490.0,560.0,0.0,0.0,0.0,temp_usr,extracal)
            usr_msk=(core['user']==usr)
            if core[usr_msk][0][4]=='eng':
                print('What is your initial weight (in Kg)?')
            if core[usr_msk][0][4]=='ita':
                print('Qual è il tuo peso iniziale (in Kg)?')
            if core[usr_msk][0][4]=='esp':
                print('Cual es tu peso inicial (en Kg)?')
            cc=0
            while cc==0:
                in_weight = input('')
                if str(in_weight).isdigit() == True:
                    cc=1
                else:
                    cc=0
                    if core[usr_msk][0][4]=='eng':
                        print('Could you repeat, please?')
                    if core[usr_msk][0][4]=='ita':
                        print('Potresti ripetere, per favore?')
                    if core[usr_msk][0][4]=='esp':
                        print('Puedes repetir, por favor?')

            temp_days_user, temp_days_date = days['user'], days['date']
            temp_weight_user, temp_weight_weight = weight['user'], weight['weight']
            temp_days_user, temp_days_date = np.append(temp_days_user,str(usr)), np.append(temp_days_date,today)
            temp_weight_user, temp_weight_weight = np.append(temp_weight_user,str(usr)), np.append(temp_weight_weight,float(in_weight))
            days, weight = np.rec.array([temp_days_user,temp_days_date], names=['user','date']), np.rec.array([temp_weight_user,temp_weight_weight], names=['user','weight'])
            np.save('days.npy',days)
            np.save('weight.npy',weight)
            df = pd.DataFrame({'top': [top], 'red_left': [top_red], 'yellow_left': [top_yellow], 'green_left': [top_green], 'red': [0], 'yellow': [0], 'green': [0], 'ingredients': ['-'], 'calories': [0], 'color':['-'], 'meal': ['-']})
            df.to_csv(str(usr)+'_'+str(today)+'.csv',index=False)
            print('')
            bb=1
        if temp_usr not in core['user'] and (temp_usr != 'add' and temp_usr != 'agg' and temp_usr != 'agr' and temp_usr != 'del' and temp_usr != 'canc'):
            print('Sorry, could you repeat?')
            print('Non ho capito, puoi ripetere?')
            print('Lo siento, puedes repetir?')
            print('')
            temp_usr = str(input(''))
    return(usr,core,days,weight)
    

#spelling check 'yes'
def check(key,lang):
    x=1
    while x==1:
        if key != 'y' and key != 'yes' and key != 'si' and key != 's' and key != 'yep' and key != 'eja' and key != 'no' and key != 'n' and key != 'nop' and key != 'nope':
            if lang == 'eng':
                print('Sorry, could you repeat?')
            if lang == 'ita':
                print('Non ho capito, puoi ripetere?')
            if lang == 'esp':
                print('Lo siento, puedes repetir?')
            key = input('')
            print('')
            x=1
        else: x=0

    return(str(key))


#spelling check 'setup'
def check_setup(key,lang):
    x=1
    while x==1:
        if key != 'lan' and key != 'par':
            if lang == 'eng':
                print('Sorry, could you repeat?')
            if lang == 'ita':
                print('Non ho capito, puoi ripetere?')
            if lang == 'esp':
                print('Lo siento, puedes repetir?')
            key = input('')
            x=1
        else: x=0

    return(str(key))



#spelling check 'lang'
def check_language(key,lang):
    x=1
    while x==1:
        if key != 'eng' and key != 'ita' and key != 'esp':
            if lang == 'eng':
                print('Sorry, could you repeat?')
            if lang == 'ita':
                print('Non ho capito, puoi ripetere?')
            if lang == 'esp':
                print('Lo siento, puedes repetir?')
            key = input('')
            x=1
        else: x=0

    return(str(key))




#per le impostazioni
def setup(arr,core,today,top,top_red,top_yellow,top_green,red,yellow,green,user,extracal):
    if 'core.npy' in arr and user != 'add' and user != 'agg' and user != 'agr':
        usr_msk = (core['user'] == str(user))
        z=1
        while z==1:
            if core[usr_msk][0][4]=='eng':
                print('Would you like to change the language (type: "lan") or the parameters of the diet (type: "par")?')
            if core[usr_msk][0][4]=='ita':
                print('Vuoi cambiare la lingua (digita: "lan") o i parametri della dieta (digita: "par")?')
            if core[usr_msk][0][4]=='esp':
                print('Quieres cambiar el idioma (digita: "lan") o los parametros de la dieta (digita: "par")?')
            print('')
            choice = input('')
            print('')
            choice = check_setup(choice,core[usr_msk][0][4])
            if choice == 'par':
                if core[usr_msk][0][4]=='eng':
                    print('You currently have the following setup:')
                    print(str(core[usr_msk][0][0])+' total calories per day')
                    print(str(float(core[usr_msk][0][1])*100/float(core[usr_msk][0][0]))+'% of red calories')
                    print(str(float(core[usr_msk][0][2])*100/float(core[usr_msk][0][0]))+'% of yellow calories')
                    print(str(float(core[usr_msk][0][3])*100/float(core[usr_msk][0][0]))+'% of green calories')
                    print('')
                    print('Would you like to change it?')
                if core[usr_msk][0][4]=='ita':
                    print('Al momento hai le seguenti impostazioni:')
                    print(str(core[usr_msk][0][0])+' calorie giornaliere totali')
                    print(str(float(core[usr_msk][0][1])*100/float(core[usr_msk][0][0]))+'% di calorie rosse')
                    print(str(float(core[usr_msk][0][2])*100/float(core[usr_msk][0][0]))+'% di calorie gialle')
                    print(str(float(core[usr_msk][0][3])*100/float(core[usr_msk][0][0]))+'% di calorie verdi')
                    print('')
                    print('Vuoi cambiarle?')
                if core[usr_msk][0][4]=='esp':
                    print('Ahora tienes esta configuracion:')
                    print(str(core[usr_msk][0][0])+' calorias totales cada dia')
                    print(str(float(core[usr_msk][0][1])*100/float(core[usr_msk][0][0]))+'% de calorias rojas')
                    print(str(float(core[usr_msk][0][2])*100/float(core[usr_msk][0][0]))+'% de calorias amarillas')
                    print(str(float(core[usr_msk][0][3])*100/float(core[usr_msk][0][0]))+'% de calorias verdes')
                    print('')
                    print('Quieres cambiarlas?')
                change=input('')
                change=check(change,core[usr_msk][0][4])
                print('')
                if change == 'no' or change == 'n' or change == 'nop' or change == 'nope':
                    if core[usr_msk][0][4]=='eng':
                        print('Would you like to change anything else?')
                    if core[usr_msk][0][4]=='ita':
                        print('Vuoi cambiare altro?')
                    if core[usr_msk][0][4]=='esp':
                        print('Quieres cambiar algo màs?')
                    el= input('')
                    el=check(el,core[usr_msk][0][4])
                    print('')
                    if el == 'y' or el == 'yes' or el == 'si' or el == 's' or el == 'yep' or el == 'eja' or el == '':
                        z=1
                    if el == 'no' or el == 'n' or el == 'nop' or el == 'nope':
                        z=0
                        return(core,top,top_red,top_yellow,top_green,str(user))
                if change == 'y' or change == 'yes' or change == 'si' or change == 's' or change == 'yep' or change == 'eja':
                    if core[usr_msk][0][4]=='eng':
                        print('What is the chosen daily calories intake (in Kcal)?')
                    if core[usr_msk][0][4]=='ita':
                        print('Qual è il tuo fabbisogno calorico giornaliero (in Kcal)?')
                    if core[usr_msk][0][4]=='esp':
                        print('Cuantas calorias necesitas cada dia (in Kcal)?')
                    new_core_top=float(input(''))
                    print('')
                    if core[usr_msk][0][4]=='eng':
                        print('What is the percentage of red calories?')
                    if core[usr_msk][0][4]=='ita':
                        print('Qual è la percentuale di calorie rosse?')
                    if core[usr_msk][0][4]=='esp':
                        print('Cual es la percentual de calorias rojas?')
                    new_perc_red=float(input(''))
                    print('')
                    if core[usr_msk][0][4]=='eng':
                        print('What is the percentage of yellow calories?')
                    if core[usr_msk][0][4]=='ita':
                        print('Qual è la percentuale di calorie gialle?')
                    if core[usr_msk][0][4]=='esp':
                        print('Cual es la percentual de calorias amarillas?')
                    new_perc_yellow=float(input(''))
                    print('')
                    new_top_core_red = float(int(new_core_top*new_perc_red/100))
                    new_top_core_yellow = float(int(new_core_top*new_perc_yellow/100))
                    new_top_core_green= new_core_top-new_top_core_yellow-new_top_core_red
                    """
                    new_top=float(top)+new_core_top-float(core[usr_msk][0][0])
                    new_top_red=float(int(float(top_red)+(new_core_top-float(core[usr_msk][0][0]))*new_perc_red/100))
                    new_top_red=new_top_red+int(extracal*(float(new_perc_red)/100))
                    new_top_yellow=float(int(float(top_yellow)+(new_core_top-float(core[usr_msk][0][0]))*new_perc_yellow/100))
                    new_top_yellow=new_top_yellow+int(extracal*(float(new_perc_yellow)/100))
                    new_top_green=new_top-new_top_red-new_top_yellow
                    new_top_green=new_top_green+int(extracal*(float((100.0-new_perc_red-new_perc_yellow))/100))
                    new_top=new_top_red+new_top_yellow+new_top_green
                    """
                    new_top=new_core_top-red-yellow-green+extracal
                    new_top_red=new_top_core_red-red+int(extracal*(float(new_perc_red)/100))
                    new_top_yellow=new_top_core_yellow-yellow+int(extracal*(float(new_perc_yellow)/100))
                    new_top_green=new_top_core_green-green+int(extracal*(float((100.0-new_perc_red-new_perc_yellow))/100))
                    temp_core=core[~usr_msk]
                    temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user=temp_core['top'],temp_core['top_red'],temp_core['top_yellow'],temp_core['top_green'],temp_core['lang'],temp_core['user']
                    temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user=np.append(temp_top,new_core_top),np.append(temp_topred,new_top_core_red),np.append(temp_topyellow,new_top_core_yellow),np.append(temp_topgreen,new_top_core_green),np.append(temp_lan,core[usr_msk][0][4]),np.append(temp_user,str(user))
                    core= np.rec.array([temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user],names=['top','top_red','top_yellow','top_green','lang','user'])
                    usr_msk = (core['user'] == str(user))
                    if core[usr_msk][0][4]=='eng':
                        print('This is your new setup:')
                        print(str(core[usr_msk][0][0])+' total calories per day')
                        print(str(core[usr_msk][0][1])+' red calories')
                        print(str(core[usr_msk][0][2])+' yellow calories')
                        print(str(core[usr_msk][0][3])+' green calories')
                    if core[usr_msk][0][4]=='ita':
                        print('Queste sono le nuove impostazioni:')
                        print(str(core[usr_msk][0][0])+' calorie giornaliere totali')
                        print(str(core[usr_msk][0][1])+' calorie rosse')
                        print(str(core[usr_msk][0][2])+' calorie gialle')
                        print(str(core[usr_msk][0][3])+' calorie verdi')
                    if core[usr_msk][0][4]=='esp':
                        print('Esta es la nueva configuracion:')
                        print(str(core[usr_msk][0][0])+' calorias totales cada dia')
                        print(str(core[usr_msk][0][1])+' calorias rojas')
                        print(str(core[usr_msk][0][2])+' calorias amarillas')
                        print(str(core[usr_msk][0][3])+' calorias verdes')
                    print('')
                    np.save('core.npy',core)
                    
                    if core[usr_msk][0][4]=='eng':
                        print('Would you like to change anything else?')
                    if core[usr_msk][0][4]=='ita':
                        print('Vuoi cambiare altro?')
                    if core[usr_msk][0][4]=='esp':
                        print('Quieres cambiar algo màs?')
                    el= input('')
                    el=check(el,core[usr_msk][0][4])
                    print('')
                    if el == 'y' or el == 'yes' or el == 'si' or el == 's' or el == 'yep' or el == 'eja' or el == '':
                        z=1
                    if el == 'no' or el == 'n' or el == 'nop' or el == 'nope':
                        z=0
                        df = pd.read_csv(str(user)+'_'+str(today)+'.csv',sep=",", header=None)
                        full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(df[0][1:]).astype(float), np.array(df[1][1:]).astype(float), np.array(df[2][1:]).astype(float), np.array(df[3][1:]).astype(float), np.array(df[4][1:]).astype(float), np.array(df[5][1:]).astype(float), np.array(df[6][1:]).astype(float), np.array(df[7][1:]), np.array(df[8][1:]).astype(float), np.array(df[9][1:]), np.array(df[10][1:])
                        full_top[-1], full_top_red[-1], full_top_yellow[-1], full_top_green[-1]=new_top,(new_top_red),new_top_yellow,new_top_green
                        dw = pd.DataFrame({'top': full_top, 'red_left': full_top_red, 'yellow_left': full_top_yellow, 'green_left': full_top_green, 'red': full_red, 'yellow': full_yellow, 'green': full_green, 'ingredients': full_ingr, 'calories': full_cal, 'color': full_color, 'meal': full_meal})
                        dw.to_csv(str(user)+'_'+str(today)+'.csv',index=False)
                        return(core,new_top,new_top_red,new_top_yellow,new_top_green,str(user))
                    
            if choice == 'lan':
                if core[usr_msk][0][4]=='eng':
                    print('To which language would you like to switch? "eng" for English, "ita" for Italian, or "esp" for Espanol')
                    print('')
                    lan = input('')
                    print('')
                    lan = check_language(lan,core[usr_msk][0][4])
                    print('')
                    print('Would you like to switch to '+str(lan)+'?')
                if core[usr_msk][0][4]=='ita':
                    print('A che linguaggio vuoi passare? "eng" per inglese, "ita" per italiano, o "esp" per spagnolo')
                    print('')
                    lan = input('')
                    print('')
                    lan = check_language(lan,core[usr_msk][0][4])
                    print('')
                    print('Vuoi passare a '+str(lan)+'?')
                if core[usr_msk][0][4]=='esp':
                    print('A que idioma quieres cambiar? "eng" per ingles, "ita" para italiano, o "esp" para espanol')
                    print('')
                    lan = input('')
                    print('')
                    lan = check_language(lan,core[usr_msk][0][4])
                    print('')
                    print('Quieres cambiar a '+str(lan)+'?')
                
                conf=input('')
                conf=check(conf,core[usr_msk][0][4])
                print('')
                if conf == 'y' or conf == 'yes' or conf == 'si' or conf == 's' or conf == 'yep' or conf == 'eja' or conf == '':
                    temp_core=core[~usr_msk]
                    temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user=temp_core['top'],temp_core['top_red'],temp_core['top_yellow'],temp_core['top_green'],temp_core['lang'],temp_core['user']
                    temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user=np.append(temp_top,core[usr_msk][0][0]),np.append(temp_topred,core[usr_msk][0][1]),np.append(temp_topyellow,core[usr_msk][0][2]),np.append(temp_topgreen,core[usr_msk][0][3]),np.append(temp_lan,str(lan)),np.append(temp_user,str(user))
                    core= np.rec.array([temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user],names=['top','top_red','top_yellow','top_green','lang','user'])
                    usr_msk = (core['user'] == str(user))
                    np.save('core.npy',core)
                if core[usr_msk][0][4]=='eng':
                    print('Would you like to change anything else?')
                if core[usr_msk][0][4]=='ita':
                    print('Vuoi cambiare altro?')
                if core[usr_msk][0][4]=='esp':
                    print('Quieres cambiar algo màs?')
                el= input('')
                el=check(el,core[usr_msk][0][4])
                print('')
                if el == 'y' or el == 'yes' or el == 'si' or el == 's' or el == 'yep' or el == 'eja' or el == '':
                    z=1
                if el == 'no' or el == 'n' or el == 'nop' or el == 'nope':
                    z=0
                    return(core,top,top_red,top_yellow,top_green,str(user))
    if 'core.npy' not in arr:
        print('Which language would you prefer? "eng" for English, "ita" for Italian, or "esp" for Espanol')
        print('(You can change it later on by calling the "setup" function)')
        print('')
        print('Quale lingua preferisci? "eng" per inglese, "ita" per italiano, o "esp" per spagnolo')
        print('(La puoi cambiare in qualsiasi momento chiamando la funzione "setup")')
        print('')
        print('Cual idioma prefieres? "eng" para ingles, "ita" para italiano, o "esp" para espanol')
        print('(Lo puedes cambiar en cualquier momento llamando la funciòn "setup")')
        print('')
        lan = input('')
        print('')
        vv=0
        if lan != 'eng' and lan != 'ita' and lan != 'esp':
            while vv == 0:
                print('Sorry, could you repeat?')
                print('')
                print('Non ho capito, puoi ripetere?')
                print('')
                print('Lo siento, puedes repetir?')
                print('')
                lan = input('')
                print('')
                if lan != 'eng' and lan != 'ita' and lan != 'esp':
                    vv=0
                else:
                    vv=1
            
        if lan=='eng':
            print('What is the chosen daily calories intake?')
            top=input('')
            if top==str(''):
                top=1400.0
            else:
                top=float(top)
            print('')
            print('What is the percentage of red calories?')
            perc_red=input('')
            if perc_red==str(''):
                perc_red=25.0
            else:
                perc_red=float(perc_red)
            print('')
            print('What is the percentage of yellow calories?')
            perc_yellow=input('')
            if perc_yellow==str(''):
                perc_yellow=35.0
            else:
                perc_yellow=float(perc_yellow)
            print('')
        if lan=='ita':
            print('Qual è il tuo fabbisogno calorico giornaliero (in Kcal)?')
            top=input('')
            if top==str(''):
                top=1400.0
            else:
                top=float(top)
            print('')
            print('Qual è la percentuale di calorie rosse?')
            perc_red=input('')
            if perc_red==str(''):
                perc_red=25.0
            else:
                perc_red=float(perc_red)
            print('')
            print('Qual è la percentuale di calorie gialle?')
            perc_yellow=input('')
            if perc_yellow==str(''):
                perc_yellow=35.0
            else:
                perc_yellow=float(perc_yellow)
            print('')
        if lan=='esp':
            print('Cuantas calorias necesitas cada dia (in Kcal)?')
            top=input('')
            if top==str(''):
                top=1400.0
            else:
                top=float(top)
            print('')
            print('Cual es la percentual de calorias rojas?')
            perc_red=input('')
            print('')
            if perc_red==str(''):
                perc_red=25.0
            else:
                perc_red=float(perc_red)
            print('Cual es la percentual de calorias amarillas?')
            perc_yellow=input('')
            print('')
            if perc_yellow==str(''):
                perc_yellow=35.0
            else:
                perc_yellow=float(perc_yellow)
            print('')
        
        top_red = top*perc_red/100
        top_yellow = top*perc_yellow/100
        top_green= top-top_yellow-top_red
        core= np.rec.array([top,top_red,top_yellow,top_green,str(lan),str(user)],names=['top','top_red','top_yellow','top_green','lang','user'])
        usr_msk = (core['user'] == user)
        if core[usr_msk][0][4]=='eng':
            print('This is your new setup:')
            print(str(core[usr_msk][0][0])+' total calories per day')
            print(str(core[usr_msk][0][1])+' red calories')
            print(str(core[usr_msk][0][2])+' yellow calories')
            print(str(core[usr_msk][0][3])+' green calories')
        if core[usr_msk][0][4]=='ita':
            print('Queste sono le nuove impostazioni:')
            print(str(core[usr_msk][0][0])+' calorie giornaliere totali')
            print(str(core[usr_msk][0][1])+' calorie rosse')
            print(str(core[usr_msk][0][2])+' calorie gialle')
            print(str(core[usr_msk][0][3])+' calorie verdi')
        if core[usr_msk][0][4]=='esp':
            print('Esta es la nueva configuracion:')
            print(str(core[usr_msk][0][0])+' calorias totales cada dia')
            print(str(core[usr_msk][0][1])+' calorias rojas')
            print(str(core[usr_msk][0][2])+' calorias amarillas')
            print(str(core[usr_msk][0][3])+' calorias verdes')
        print('')
        np.save('core.npy',core)
        
        if str(user)+'_'+str(today)+'.csv' in arr:
            dfr = pd.read_csv(str(user)+'_'+str(today)+'.csv',sep=",", header=None)
            full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(dfr[0][1:]).astype(float), np.array(dfr[1][1:]).astype(float), np.array(dfr[2][1:]).astype(float), np.array(dfr[3][1:]).astype(float), np.array(dfr[4][1:]).astype(float), np.array(dfr[5][1:]).astype(float), np.array(dfr[6][1:]).astype(float), np.array(dfr[7][1:]), np.array(dfr[8][1:]).astype(float), np.array(dfr[9][1:]), np.array(dfr[10][1:])
            top, top_red, top_yellow, top_green, red, yellow, green=full_top[-1], full_top_red[-1], full_top_yellow[-1], full_top_green[-1], full_red[-1], full_yellow[-1], full_green[-1]
            full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal=np.append(full_top,(core[usr_msk][0][0]-red-yellow-green)), np.append(full_top_red,(core[usr_msk][0][1]-red)), np.append(full_top_yellow,(core[usr_msk][0][2]-yellow)), np.append(full_top_green,(core[usr_msk][0][3]-green)), np.append(full_red,red), np.append(full_yellow,yellow), np.append(full_green,green), np.append(full_ingr,'-'), np.append(full_cal,0), np.append(full_color,'-'),np.append(full_meal,'-')
            
            dfw = pd.DataFrame({'top': full_top, 'red_left': full_top_red, 'yellow_left': full_top_yellow, 'green_left': full_top_green, 'red': full_red, 'yellow': full_yellow, 'green': full_green, 'ingredients': full_ingr, 'calories': full_cal, 'color': full_color, 'meal': full_meal})
            dfw.to_csv(str(user)+'_'+str(today)+'.csv',index=False)
        if str(user)+'_'+str(today)+'.csv' not in arr:
            dfw = pd.DataFrame({'top': [core[usr_msk][0][0]], 'red_left': [core[usr_msk][0][1]], 'yellow_left': [core[usr_msk][0][2]], 'green_left': [core[usr_msk][0][3]], 'red': [0], 'yellow': [0], 'green': [0], 'ingredients':['-'], 'calories':[0], 'color':['-'], 'meal':['-']})
        dfw.to_csv(str(user)+'_'+str(today)+'.csv',index=False)
        return(core,top,top_red,top_yellow,top_green,str(user))
    
    if 'core.npy' in arr and (user == 'add' or user == 'agg' or user == 'agr'):
        usr = add_user_name(core)
        usr = str(usr)
        print('Welcome to Dietly, '+usr+'! Benvenuto/a su Dietly, '+usr+'! Bienvenido/a en Dietly, '+usr+'!')
        print('')
        print('Which language would you prefer? "eng" for English, "ita" for Italian, or "esp" for Espanol')
        print('(You can change it later on by calling the "setup" function)')
        print('')
        print('Quale lingua preferisci? "eng" per inglese, "ita" per italiano, o "esp" per spagnolo')
        print('(La puoi cambiare in qualsiasi momento chiamando la funzione "setup")')
        print('')
        print('Cual idioma prefieres? "eng" para ingles, "ita" para italiano, o "esp" para espanol')
        print('(Lo puedes cambiar en cualquier momento llamando la funciòn "setup")')
        print('')
        lan = input('')
        print('')
        vv=0
        if lan != 'eng' and lan != 'ita' and lan != 'esp':
            while vv == 0:
                print('Sorry, could you repeat?')
                print('')
                print('Non ho capito, puoi ripetere?')
                print('')
                print('Lo siento, puedes repetir?')
                print('')
                lan = input('')
                if lan != 'eng' and lan != 'ita' and lan != 'esp':
                    vv=0
                else:
                    vv=1
            
        print('')
        if lan=='eng':
            print('What is the chosen daily calories intake?')
            top=input('')
            if top==str(''):
                top=1400.0
            else:
                top=float(top)
            print('')
            print('What is the percentage of red calories?')
            perc_red=input('')
            if perc_red==str(''):
                perc_red=25.0
            else:
                perc_red=float(perc_red)
            print('')
            print('What is the percentage of yellow calories?')
            perc_yellow=input('')
            if perc_yellow==str(''):
                perc_yellow=35.0
            else:
                perc_yellow=float(perc_yellow)
            print('')
        if lan=='ita':
            print('Qual è il tuo fabbisogno calorico giornaliero (in Kcal)?')
            top=input('')
            if top==str(''):
                top=1400.0
            else:
                top=float(top)
            print('')
            print('Qual è la percentuale di calorie rosse?')
            perc_red=input('')
            if perc_red==str(''):
                perc_red=25.0
            else:
                perc_red=float(perc_red)
            print('')
            print('Qual è la percentuale di calorie gialle?')
            perc_yellow=input('')
            if perc_yellow==str(''):
                perc_yellow=35.0
            else:
                perc_yellow=float(perc_yellow)
            print('')
        if lan=='esp':
            print('Cuantas calorias necesitas cada dia (in Kcal)?')
            top=input('')
            if top==str(''):
                top=1400.0
            else:
                top=float(top)
            print('')
            print('Cual es la percentual de calorias rojas?')
            perc_red=input('')
            print('')
            if perc_red==str(''):
                perc_red=25.0
            else:
                perc_red=float(perc_red)
            print('Cual es la percentual de calorias amarillas?')
            perc_yellow=input('')
            print('')
            if perc_yellow==str(''):
                perc_yellow=35.0
            else:
                perc_yellow=float(perc_yellow)
            print('')
        
        top_red = top*perc_red/100
        top_yellow = top*perc_yellow/100
        top_green= top-top_yellow-top_red
        temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user=core['top'],core['top_red'],core['top_yellow'],core['top_green'],core['lang'],core['user']
        temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user=np.append(temp_top,top),np.append(temp_topred,top_red),np.append(temp_topyellow,top_yellow),np.append(temp_topgreen,top_green),np.append(temp_lan,str(lan)),np.append(temp_user,str(usr))
        core= np.rec.array([temp_top,temp_topred,temp_topyellow,temp_topgreen,temp_lan,temp_user],names=['top','top_red','top_yellow','top_green','lang','user'])
        usr_msk = (core['user'] == usr)
        if core[usr_msk][0][4]=='eng':
            print('This is your new setup:')
            print(str(core[usr_msk][0][0])+' total calories per day')
            print(str(core[usr_msk][0][1])+' red calories')
            print(str(core[usr_msk][0][2])+' yellow calories')
            print(str(core[usr_msk][0][3])+' green calories')
        if core[usr_msk][0][4]=='ita':
            print('Queste sono le nuove impostazioni:')
            print(str(core[usr_msk][0][0])+' calorie giornaliere totali')
            print(str(core[usr_msk][0][1])+' calorie rosse')
            print(str(core[usr_msk][0][2])+' calorie gialle')
            print(str(core[usr_msk][0][3])+' calorie verdi')
        if core[usr_msk][0][4]=='esp':
            print('Esta es la nueva configuracion:')
            print(str(core[usr_msk][0][0])+' calorias totales cada dia')
            print(str(core[usr_msk][0][1])+' calorias rojas')
            print(str(core[usr_msk][0][2])+' calorias amarillas')
            print(str(core[usr_msk][0][3])+' calorias verdes')
        print('')
        np.save('core.npy',core)
        
        if str(usr)+'_'+str(today)+'.csv' in arr:
            dfr = pd.read_csv(str(usr)+'_'+str(today)+'.csv',sep=",", header=None)
            full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(dfr[0][1:]).astype(float), np.array(dfr[1][1:]).astype(float), np.array(dfr[2][1:]).astype(float), np.array(dfr[3][1:]).astype(float), np.array(dfr[4][1:]).astype(float), np.array(dfr[5][1:]).astype(float), np.array(dfr[6][1:]).astype(float), np.array(dfr[7][1:]), np.array(dfr[8][1:]).astype(float), np.array(dfr[9][1:]), np.array(dfr[10][1:])
            top, top_red, top_yellow, top_green, red, yellow, green=full_top[-1], full_top_red[-1], full_top_yellow[-1], full_top_green[-1], full_red[-1], full_yellow[-1], full_green[-1]
            full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal=np.append(full_top,(core[usr_msk][0][0]-red-yellow-green)), np.append(full_top_red,(core[usr_msk][0][1]-red)), np.append(full_top_yellow,(core[usr_msk][0][2]-yellow)), np.append(full_top_green,(core[usr_msk][0][3]-green)), np.append(full_red,red), np.append(full_yellow,yellow), np.append(full_green,green), np.append(full_ingr,'-'), np.append(full_cal,0), np.append(full_color,'-'),np.append(full_meal,'-')
            
            dfw = pd.DataFrame({'top': full_top, 'red_left': full_top_red, 'yellow_left': full_top_yellow, 'green_left': full_top_green, 'red': full_red, 'yellow': full_yellow, 'green': full_green, 'ingredients': full_ingr, 'calories': full_cal, 'color': full_color, 'meal': full_meal})
            dfw.to_csv(str(usr)+'_'+str(today)+'.csv',index=False)
        if str(usr)+'_'+str(today)+'.csv' not in arr:
            dfw = pd.DataFrame({'top': [core[usr_msk][0][0]], 'red_left': [core[usr_msk][0][1]], 'yellow_left': [core[usr_msk][0][2]], 'green_left': [core[usr_msk][0][3]], 'red': [0], 'yellow': [0], 'green': [0], 'ingredients':['-'], 'calories':[0], 'color':['-'], 'meal':['-']})
        dfw.to_csv(str(usr)+'_'+str(today)+'.csv',index=False)
        return(core,top,top_red,top_yellow,top_green,str(usr))




#per sapere quante calorie sono rimaste 
def left(tot_red,tot_yellow,tot_green,lan):
    if tot_red <=0: tot_red=0
    if tot_yellow <=0: tot_yellow=0
    if tot_green <=0: tot_green=0
    tot_left = tot_red + tot_yellow + tot_green
    if lan=='eng':
        print('You have '+str(tot_left)+' Kcal left today. Of which:')
        print('')
        print(str(tot_red)+' RED')
        print(str(tot_yellow)+' YELLOW')
        print(str(tot_green)+' GREEN')
    if lan=='ita':
        print('Ti rimangono '+str(tot_left)+' Kcal, oggi. Di cui:')
        print('')
        print(str(tot_red)+' ROSSE')
        print(str(tot_yellow)+' GIALLE')
        print(str(tot_green)+' VERDI')
    if lan=='esp':
        print('Te quedan '+str(tot_left)+' Kcal, hoy. De esas:')
        print('')
        print(str(tot_red)+' ROJAS')
        print(str(tot_yellow)+' AMARILLAS')
        print(str(tot_green)+' VERDES')

    print('')
    return()



#plotting function

def plot(core,days,weight,user):
    if len(days)<1:
        if core[4]=='eng':
            print('No weights to show, yet')
        if core[4]=='ita':
            print('Non ci sono ancora pesate da mostrare')
        if core[4]=='esp':
            print('Todavia no tienes pesaje para mostrar')
        next_fun=input('')
        print('')
        return()
    if len(days)>1:
        l=min(7,len(days))
        ll=-np.arange(1,l)
        loss=[]
        for i in ll:
            loss.append(float(weight[i])-float(weight[i-1]))
        avg_loss=round(-np.mean(loss),3)
    if len(days)<2:
        avg_loss=0
    
    fig1 = plt.figure(figsize=(9,8))
    gs = fig1.add_gridspec(1,1)
    ax1= fig1.add_subplot(gs[0,0])
    spl_date = np.arange(len(days))
    spl = UnivariateSpline(spl_date, weight)
    spl.set_smoothing_factor(len(days)//7)
    if core[4]=='eng':
        ax1.set_ylabel(r"$Weight\,(kg)$", fontsize=18)
        ax1.set_xlabel(r"$Day$", fontsize=18)
    if core[4]=='ita':
        ax1.set_ylabel(r"$Peso\,(kg)$", fontsize=18)
        ax1.set_xlabel(r"$Data$", fontsize=18)
    if core[4]=='esp':
        ax1.set_ylabel(r"$Peso\,(kg)$", fontsize=18)
        ax1.set_xlabel(r"$Fecha$", fontsize=18)
    ax1.set_ylim(ymin=min(weight-0.2),ymax=max(weight+0.2))
    ax1.plot(days,weight,linewidth=1,color='k')
    ax1.plot(spl_date,spl(spl_date),linewidth=1,color='r')
    ax1.scatter(days,weight,s=(60-len(days)//3),color='r')
    sup = (max(weight+0.2)-min(weight-0.2))/40
    for h in range(len(days)):
        plt.text(days[h],weight[h],str(weight[h]),fontsize=(18-len(days)//6),position=(days[h],weight[h]+sup))
    if core[4]=='eng':
        fig1.suptitle(r"Average dayly loss: "+str(avg_loss)+r"$\,$Kg",fontsize=16)
    if core[4]=='ita':
        fig1.suptitle(r"Perdita di peso media giornaliera: "+str(avg_loss)+r"$\,$Kg",fontsize=16)
    if core[4]=='esp':
        fig1.suptitle(r"Perdida de peso media diaria: "+str(avg_loss)+r"$\,$Kg",fontsize=16)
    ax1.set_xticks(ticks=days)
    newdays = np.copy(days)
    for i in range(len(newdays)):
        newdays[i] = newdays[i][:-5]
    ax1.set_xticklabels(labels=newdays,fontsize=(14-len(days)//5))
    ax1.tick_params('y',labelsize=(14-len(days)//5))
    plt.show(block=False)
    close= input('')
    plt.close('all')
    return()

def past_meals(core,user,arr):
    usr_msk=(core['user']==user)
    tt = 0
    while tt == 0: 
        cc = 0
        while cc == 0:
            if core[usr_msk][0][4]=='eng':
                print('The meals of which day would you like to update? (format: dd_mm_yyyy)')
            if core[usr_msk][0][4]=='ita':
                print('I pasti di quale giorno vorresti aggiornare? (format: dd_mm_yyyy)')
            if core[usr_msk][0][4]=='esp':
                print('Las comidas de cual dìa querias actualizar? (format: dd_mm_yyyy)')
            today2 = input('')
            print('')
            if core[usr_msk][0][4]=='eng':
                print('Would you like to update the meals of the '+str(today2)+'?')
            if core[usr_msk][0][4]=='ita':
                print('Vorresti aggiornare i pasti del '+str(today2)+'?')
            if core[usr_msk][0][4]=='esp':
                print('Querias actualizar las comidas del '+str(today2)+'?')
            conf = input('')
            print('')
            conf = check(conf,core[usr_msk][0][4])
            if conf == 'y' or conf == 'yes' or conf == 'si' or conf == 's' or conf == 'yep' or conf == 'eja':
                cc = 1
            if conf == 'no' or conf == 'n' or conf == 'nop' or conf == 'nope':
                if core[usr_msk][0][4]=='eng':
                    print('Whould you like to select another day?')
                if core[usr_msk][0][4]=='ita':
                    print('Vorresti selezionare un altro giorno?')
                if core[usr_msk][0][4]=='esp':
                    print('Querias elegir otro dia?')
                conf2 = input('')
                print('')
                conf2 = check(conf2,core[usr_msk][0][4])
                if conf2 == 'no' or conf2 == 'n' or conf2 == 'nop' or conf2 == 'nope':
                    cc = 1
                    return()
                else: cc = 0
        
        if str(user)+'_'+str(today2)+'.csv' in arr:
            df = pd.read_csv(str(user)+'_'+str(today2)+'.csv',sep=",", header=None)
            full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(df[0][1:]).astype(float), np.array(df[1][1:]).astype(float), np.array(df[2][1:]).astype(float), np.array(df[3][1:]).astype(float), np.array(df[4][1:]).astype(float), np.array(df[5][1:]).astype(float), np.array(df[6][1:]).astype(float), np.array(df[7][1:]), np.array(df[8][1:]).astype(float), np.array(df[9][1:]), np.array(df[10][1:])
            top, top_red, top_yellow, top_green, red, yellow, green=full_top[-1], full_top_red[-1], full_top_yellow[-1], full_top_green[-1], full_red[-1], full_yellow[-1], full_green[-1]
        if str(user)+'_'+str(today2)+'.csv' not in arr:
            top=float(core[usr_msk][0][0])
            top_red=float(core[usr_msk][0][1])
            top_yellow=float(core[usr_msk][0][2])
            top_green=float(core[usr_msk][0][3])
            red,yellow,green=0.0,0.0,0.0
            df = pd.DataFrame({'top': [top], 'red_left': [top_red], 'yellow_left': [top_yellow], 'green_left': [top_green], 'red': [red], 'yellow': [yellow], 'green': [green], 'ingredients': ['-'], 'calories': [0], 'color':['-'], 'meal': ['-']})
            df.to_csv(str(user)+'_'+str(today2)+'.csv',index=False)
        
        top,top_red,top_yellow,top_green,red,yellow,green = meals(top,top_red,top_yellow,top_green,red,yellow,green,core[usr_msk][0],today2,str(user))

        if core[usr_msk][0][4]=='eng':
            print('Whould you like to update the meals of another day?')
        if core[usr_msk][0][4]=='ita':
            print('Vorresti aggiornare i pasti di un altro giorno?')
        if core[usr_msk][0][4]=='esp':
            print('Querias actualizar las comidas de un otro dia?')
        conf3 = input('')
        conf3 = check(conf3,core[usr_msk][0][4])
        if conf3 == 'y' or conf3 == 'yes' or conf3 == 'si' or conf3 == 's' or conf3 == 'yep' or conf3 == 'eja':
            print('')
        if conf3 == 'no' or conf3 == 'n' or conf3 == 'nop' or conf3 == 'nope':
            tt = 1
        else: tt = 0
    return()


#logging new weight
def nw(weight,days,core,today,user):
    usr_msk = (core['user'] == user)
    usr_days_msk = (days['user'] == user)
    usr_weight_msk = (weight['user'] == user)
    if today in days[usr_days_msk]['date']:
        if core[usr_msk][0][4]=='eng':
            print('You already uploaded your weight today, do you want to modify it?')
        if core[usr_msk][0][4]=='ita':
            print('Hai già caricato il tuo peso oggi, lo vuoi modificare?')
        if core[usr_msk][0][4]=='esp':
            print('Ya cargaste tu peso hoy, quieres actualizarlo?')
        info=input('')
        info=check(info,core[usr_msk][0][4])
        print('')
        if info == 'y' or info == 'yes' or info == 'si' or info == 's' or info == 'yep' or info == 'eja':
            if core[usr_msk][0][4]=='eng':
                print('What is the new weight (in kg)?')
            if core[usr_msk][0][4]=='ita':
                print('Qual è la nuova pesata (in kg)?')
            if core[usr_msk][0][4]=='esp':
                print('Cual es el nuevo peso? (en kg)?')
            neweight=float(input(''))
            change_msk= (days['user']==user) & (days['date']==today)
            weight = weight[~change_msk]
            temp_weight_user, temp_weight_weight = weight['user'], weight['weight']
            temp_weight_user, temp_weight_weight = np.append(temp_weight_user,str(user)), np.append(temp_weight_weight,neweight)
            weight = np.rec.array([temp_weight_user,temp_weight_weight], names=['user','weight'])
            print('')
        
    
    if today not in days[usr_days_msk]['date']:
        if core[usr_msk][0][4]=='eng':
            print('Do you want to upload the new weight (in kg)?')
        if core[usr_msk][0][4]=='ita':
            print('Vuoi caricare la nuova pesata (in kg)?')
        if core[usr_msk][0][4]=='esp':
            print('Quieres cargar el nuevo peso? (en kg)')
        info=input('')
        info=check(info,core[usr_msk][0][4])
        print('')
        if info == 'y' or info == 'yes' or info == 'si' or info == 's' or info == 'yep' or info == 'eja':
            if core[usr_msk][0][4]=='eng':
                print('What is your weight (in kg) today?')
            if core[usr_msk][0][4]=='ita':
                print('Qual è il tuo peso (in kg) oggi?')
            if core[usr_msk][0][4]=='esp':
                print('Cual es tu peso (en kg) hoy?')
            neweight=float(input(''))
            temp_days_user, temp_days_date = days['user'], days['date']
            temp_weight_user, temp_weight_weight = weight['user'], weight['weight']
            temp_days_user, temp_days_date = np.append(temp_days_user,str(user)), np.append(temp_days_date,today)
            temp_weight_user, temp_weight_weight = np.append(temp_weight_user,str(user)), np.append(temp_weight_weight,neweight)
            days, weight = np.rec.array([temp_days_user,temp_days_date], names=['user','date']), np.rec.array([temp_weight_user,temp_weight_weight], names=['user','weight'])
            np.save('days.npy',days)
    np.save('weight.npy',weight)

    return(weight,days)
    


#workout part

def wo(top,top_red,top_yellow,top_green,red,yellow,green,core,today,user):
    usr_msk = (core['user'] == user)
    if core[usr_msk][0][4]=='eng':
        print('How many Kcal did you burn?')
    if core[usr_msk][0][4]=='ita':
        print('Quante Kcal hai bruciato?')
    if core[usr_msk][0][4]=='esp':
        print('Cuantas Kcal quemaste?')
    dd=0
    while dd==0:
        extracal=input('')
        try:
            extracal=float(extracal)
        except:
            if core[usr_msk][0][4] == 'eng':
                print('Sorry, could you repeat?')
            if core[usr_msk][0][4] == 'ita':
                print('Non ho capito, puoi ripetere?')
            if core[usr_msk][0][4] == 'esp':
                print('Lo siento, puedes repetir?')
            dd=0
        else:
            extracal=float(extracal)
            dd=1


    print('')
    extracal= int(extracal)/2
    if core[usr_msk][0][4]=='eng':
        print("Do you want to update today's info?")
    if core[usr_msk][0][4]=='ita':
        print('Vuoi aggiornare le informazioni di oggi?')
    if core[usr_msk][0][4]=='esp':
        print('Quieres actualizar las infociones de hoy?')
    info=input('')
    info=check(info,core[usr_msk][0][4])
    print('')
    if info == 'y' or info == 'yes' or info == 'si' or info == 's' or info == 'yep' or info == 'eja':
        top = top + extracal
        top_red = top_red+round(extracal*(core[usr_msk][0][1])/core[usr_msk][0][0])
        top_yellow = top_yellow+round(extracal*(core[usr_msk][0][2])/core[usr_msk][0][0])
        top_green = top_green+round(extracal*(core[usr_msk][0][3])/core[usr_msk][0][0])
        left(top_red,top_yellow,top_green,core[usr_msk][0][4])
        dfr = pd.read_csv(str(user)+'_'+str(today)+'.csv',sep=",", header=None)
        full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(dfr[0][1:]).astype(float), np.array(dfr[1][1:]).astype(float), np.array(dfr[2][1:]).astype(float), np.array(dfr[3][1:]).astype(float), np.array(dfr[4][1:]).astype(float), np.array(dfr[5][1:]).astype(float), np.array(dfr[6][1:]).astype(float), np.array(dfr[7][1:]), np.array(dfr[8][1:]).astype(float), np.array(dfr[9][1:]), np.array(dfr[10][1:])
        full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal=np.append(full_top,top), np.append(full_top_red,top_red), np.append(full_top_yellow,top_yellow), np.append(full_top_green,top_green), np.append(full_red,red), np.append(full_yellow,yellow), np.append(full_green,green), np.append(full_ingr,str('-')), np.append(full_cal,0), np.append(full_color,str('-')),np.append(full_meal,str('-'))
        
        dfw = pd.DataFrame({'top': full_top, 'red_left': full_top_red, 'yellow_left': full_top_yellow, 'green_left': full_top_green, 'red': full_red, 'yellow': full_yellow, 'green': full_green, 'ingredients': full_ingr, 'calories': full_cal, 'color': full_color, 'meal': full_meal})
        dfw.to_csv(str(user)+'_'+str(today)+'.csv',index=False)
    return(top,top_red,top_yellow,top_green,extracal)


#spelling check for ingredients' color
def color_check(color, lang):
    c=1
    while c==1:
        if str(color)== 'red' or str(color)== 'yellow' or str(color)== 'green' or str(color)== 'rosso' or str(color)== 'rosse' or str(color)== 'rojo' or str(color)== 'rojas' or str(color)== 'giallo' or str(color)== 'gialle' or str(color)== 'amarillo' or str(color)== 'amarillas' or str(color)== 'verde' or str(color)== 'verdi' or str(color)== 'verdes': c=0
        else:
            if lang == 'eng':
                print('Sorry, could you repeat?')
            if lang == 'ita':
                print('Non ho capito, puoi ripetere?')
            if lang == 'esp':
                print('Lo siento, puedes repetir?')
            color=input('')
            print('')
    if str(color)== 'rosso' or str(color)== 'rosse' or str(color)== 'rojo' or str(color)== 'rojas': color = 'red'
    if str(color)== 'giallo' or str(color)== 'gialle' or str(color)== 'amarillo' or str(color)== 'amarillas': color = 'yellow'
    if str(color)== 'verde' or str(color)== 'verdi' or str(color)== 'verdes': color = 'green'
    return(str(color))


#check if an entry is a digit
def is_digit_check(lang):
    bb = 1
    while bb==1:
        key=input('')
        if str(key).isdigit() == True:
            bb=0
        else:
            if lang == 'eng':
                print('Sorry, could you repeat?')
            if lang == 'ita':
                print('Non ho capito, puoi ripetere?')
            if lang == 'esp':
                print('Lo siento, puedes repetir?')
            print('')
    return(key)



#spelling check for calory units
def unit_check(unit, lang):
    c=1
    while c==1:
        if str(unit)== 'g' or str(unit)== 'unit' or str(unit)== 'tsp' or str(unit)== 'tbsp' or str(unit)== 'slice': c=0
        else:
            if lang == 'eng':
                print('Sorry, could you repeat?')
            if lang == 'ita':
                print('Non ho capito, puoi ripetere?')
            if lang == 'esp':
                print('Lo siento, puedes repetir?')
            unit=input('')
            print('')
    return(str(unit))


#spelling check for decision
def decision_check(dec, lang):
    c=1
    while c==1:
        if str(dec) == 'dtb' or str(dec)== 'ingr': c=0
        else:
            if lang == 'eng':
                print('Sorry, could you repeat?')
            if lang == 'ita':
                print('Non ho capito, puoi ripetere?')
            if lang == 'esp':
                print('Lo siento, puedes repetir?')
            dec=input('')
            print('')
    return(str(dec))


def ml_check(lang):
    bb = 1
    while bb==1:
        key=input('')
        if str(key) == 'l' or str(key) == 'p' or str(key) == 'a' or str(key) == 'b' or str(key) == 'co' or str(key) == 'de' or str(key) == 'ce' or str(key) == 'c' or str(key) == 'd' or str(key) == 's':
            bb=0
        else:
            if lang == 'eng':
                print('Sorry, could you repeat?')
            if lang == 'ita':
                print('Non ho capito, puoi ripetere?')
            if lang == 'esp':
                print('Lo siento, puedes repetir?')
            print('')
    return(key)




#per controllare/aggiornare il database degli ingredienti
def database_update(lang):
    dfr_dtb = pd.read_csv('Database.csv',sep=",", header=None)
    fd_dtb, color_dtb, cal_dtb, density_dtb, units_dtb= np.array(dfr_dtb[0][1:]).astype(str), np.array(dfr_dtb[1][1:]).astype(str), np.array(dfr_dtb[2][1:]).astype(float), np.array(dfr_dtb[3][1:]).astype(float), np.array(dfr_dtb[4][1:]).astype(str)
    if lang == 'eng':
        print("Would you like to see the full database (digit 'dtb'), or to check a single ingredient (digit 'ingr')?")
    if lang == 'ita':
        print("Vorresti vedere tutto il database (digita 'dtb'), o un singolo ingrediente (digita 'ingr')?")
    if lang == 'esp':
        print("Desea ver todo el database (escriba 'dtb'), o un solo ingrediente (escriba 'ingr')?")
    decision=input('')
    print('')
    decision=decision_check(decision, lang)
    if decision == 'dtb':
        print(dfr_dtb)
        print('')
    else:
        x=1
        while x==1:
            if lang == 'eng':
                print('Which ingredient would you like to check?')
            if lang == 'ita':
                print('Che ingrediente vorresti controllare?')
            if lang == 'esp':
                print('Cual ingrediente querias verificar?')
            fd=input('')
            fd=str(fd)
            print('')
            if fd in fd_dtb:
                fd_msk= fd_dtb==fd
                if lang == 'eng':
                    print(str(fd_dtb[fd_msk][0])+': '+str(cal_dtb[fd_msk][0])+' '+str(color_dtb[fd_msk][0])+' Kcal every '+ str(density_dtb[fd_msk][0]) +' '+ str(units_dtb[fd_msk][0]))
                    print('')
                    print('Would you like to check another ingredient?')
                if lang == 'ita':
                    print(str(fd_dtb[fd_msk][0])+': '+str(cal_dtb[fd_msk][0])+' '+str(color_dtb[fd_msk][0])+' Kcal ogni '+ str(density_dtb[fd_msk][0]) +' '+ str(units_dtb[fd_msk][0]))
                    print('')
                    print('Vorresti controllare un altro ingrediente?')
                if lang == 'esp':
                    print(str(fd_dtb[fd_msk][0])+': '+str(cal_dtb[fd_msk][0])+' '+str(color_dtb[fd_msk][0])+' Kcal cada '+ str(density_dtb[fd_msk][0]) +' '+ str(units_dtb[fd_msk][0]))
                    print('')
                    print('Querias verifcar otro ingrediente?')
                other=input('')
                other=check(other,lang)
                print('')
                if other == 'no' or other == 'n' or other == 'nop' or other == 'nope':
                    x=0
                if other == 'y' or other == 'yes' or other == 'si' or other == 's' or other == 'yep' or other == 'eja':
                    x=1
            else:
                if lang == 'eng':
                    print(fd+' is not in the database. Do you want to add it?')
                if lang == 'ita':
                    print(fd+' non è nel database. Lo vuoi aggiungere (in inglese)?')
                if lang == 'esp':
                    print(fd+' no està en el database. Quieres agregarlo (en ingles)?')
                add = input('')
                add=check(add,lang)
                print('')
                if add == 'y' or add == 'yes' or add == 'si' or add == 's' or add == 'yep' or add == 'eja':
                    zz = 1
                    while zz == 1:
                        if lang == 'eng':
                            print('What color are these calories?')
                            col=input('')
                            col = color_check(col,lang)
                            print('')
                            print('What is the calory intake...')
                            cal = is_digit_check(lang)
                            cal=float(cal)
                            print('')
                            print('...for this amount...')
                            den = is_digit_check(lang)
                            den = float(den)
                            print('')
                            print('...in these units (g for "grams", unit for "units", tsp for "teaspoons", tbsp for "tablespoons", slice for "slices")?')
                            un=input('')
                            un=unit_check(un,lang)
                        if lang == 'ita':
                            print('Di che colore sono le calorie di questo cibo?')
                            col=input('')
                            col=color_check(col,lang)
                            print('')
                            print('Qual è la quantità di calorie...')
                            cal = is_digit_check(lang)
                            cal=float(cal)
                            print('')
                            print('...per questa quantità di cibo...')
                            den = is_digit_check(lang)
                            den = float(den)
                            print('')
                            print('...in queste unità (g per "grammi", unit per "unità", tsp per "cucchiaini", tbsp per "cucchiai", slice per "fette")?')
                            un=input('')
                            un=unit_check(un,lang)
                        if lang == 'esp':
                            print('Cual es el color de las calorias de este ingrediente?')
                            col=input('')
                            col=color_check(col,lang)
                            print('')
                            print('Cual es la cuantidad de calorias...')
                            cal = is_digit_check(lang)
                            cal=float(cal)
                            print('')
                            print('...para esta cuantidad del ingrediente...')
                            den = is_digit_check(lang)
                            den = float(den)
                            print('')
                            print('...en estas unitas (g para "grammos", unit para "unidades", tsp para "cuchariditas", tbsp para "cucharas", slice para "rebanadas")?')
                            un=input('')
                            un=unit_check(un,lang)
                        print('')
                        if lang=='eng':
                            print(str(fd)+': '+str(cal)+' '+str(col)+' Kcal every '+ str(den) +' '+ str(un)+'. Is it correct?')
                        if lang=='ita':
                            print(str(fd)+': '+str(cal)+' Kcal '+str(col)+' ogni '+ str(den) +' '+ str(un)+". E' corretto?")
                        if lang=='esp':
                            print(str(fd)+': '+str(cal)+' Kcal '+str(col)+' cada '+ str(den) +' '+ str(un)+'. Es correcto?')
                        correct=input('')
                        correct=check(correct,lang)
                        print('')
                        if correct =='no' or correct == 'n' or correct == 'nop' or correct == 'nope':
                            zz = 1
                        if correct == 'y' or correct == 'yes' or correct == 'si' or correct == 's' or correct == 'yep' or correct == 'eja' or correct == '':
                            fd_dtb=np.append(fd_dtb,fd)
                            color_dtb=np.append(color_dtb,col)
                            cal_dtb=np.append(cal_dtb,cal)
                            density_dtb=np.append(density_dtb,den)
                            units_dtb=np.append(units_dtb,un)
                            ix= np.argsort(fd_dtb)
                            fd_dtb,color_dtb,cal_dtb,density_dtb,units_dtb=fd_dtb[ix],color_dtb[ix],cal_dtb[ix],density_dtb[ix],units_dtb[ix]
                            dfw_dtb = pd.DataFrame({'food': fd_dtb, 'color': color_dtb, 'calories': cal_dtb, 'every': density_dtb, 'units': units_dtb})
                            dfw_dtb.to_csv('Database.csv',index=False)
                            zz = 0
                    if lang=='eng':
                        print('Would you like to check another ingredient?')
                    if lang=='ita':
                        print('Vorresti controllare un altro ingrediente?')
                    if lang=='esp':
                        print('Quieres comprobar otro ingrediente?')
                    other=input('')
                    other=check(other,lang)
                    print('')
                    if other == 'no' or other == 'n' or other == 'nop' or other == 'nope':
                        x=0
                    if other == 'y' or other == 'yes' or other == 'si' or other == 's' or other == 'yep' or other == 'eja':
                        x=1

                if add == 'no' or add == 'n' or add == 'nop' or add == 'nope':
                    if lang=='eng':
                        print('Would you like to check another ingredient?')
                    if lang=='ita':
                        print('Vorresti controllare un altro ingrediente?')
                    if lang=='esp':
                        print('Quieres comprobar otro ingrediente?')
                    other=input('')
                    other=check(other,lang)
                    print('')
                    if other == 'no' or other == 'n' or other == 'nop' or other == 'nope':
                        x=0
                    if other == 'y' or other == 'yes' or other == 'si' or other == 's' or other == 'yep' or other == 'eja':
                        x=1
    return()
    





#per accedere/aggiornare il database da dentro "meals"

def database_search(lang,dtb):
    fd_dtb, color_dtb, cal_dtb, density_dtb, units_dtb= np.array(dtb[0][1:]).astype(str), np.array(dtb[1][1:]).astype(str), np.array(dtb[2][1:]).astype(float), np.array(dtb[3][1:]).astype(float), np.array(dtb[4][1:]).astype(str)
    if lang=='eng':
        print('Which ingredient would you like to add?')
    if lang=='ita':
        print('Che ingrediente vorresti aggiungere?')
    if lang=='esp':
        print('Cual ingrediente querias agregar?')
    fd=input('')
    fd=str(fd)
    print('')
    if fd in fd_dtb:
        fd_msk= fd_dtb==fd
        if lang=='eng':
            print(str(fd_dtb[fd_msk][0])+': '+str(cal_dtb[fd_msk][0])+' '+str(color_dtb[fd_msk][0])+' Kcal every '+ str(density_dtb[fd_msk][0]) +' '+ str(units_dtb[fd_msk][0]))
        if lang=='ita':
            print(str(fd_dtb[fd_msk][0])+': '+str(cal_dtb[fd_msk][0])+' Kcal '+str(color_dtb[fd_msk][0])+' ogni '+str(density_dtb[fd_msk][0]) +' '+ str(units_dtb[fd_msk][0]))
        if lang=='esp':
            print(str(fd_dtb[fd_msk][0])+': '+str(cal_dtb[fd_msk][0])+' Kcal '+str(color_dtb[fd_msk][0])+' cada '+ str(density_dtb[fd_msk][0]) +' '+ str(units_dtb[fd_msk][0]))
        print('')
        return(fd)
    else:
        """
        maybe add a spelling check here
        """
        zz = 1
        if lang=='eng':
            print(fd+' is not in the database. Would you like to add it?')
        if lang=='ita':
            print(fd+' non è nel database. Lo vuoi aggiungere (in inglese)?')
        if lang=='esp':
            print(fd+' no està en el database. Quieres agregarlo (en ingles)?')
        temp=input('')
        temp=check(temp,lang)
        print('')
        if temp== 'no' or temp == 'n' or temp == 'nop' or temp == 'nope':
            fd = 'empty'
            zz = 0
        
        while zz == 1:
            if lang=='eng':
                print('What color are these calories?')
                col=input('')
                print('')
                color_check(col,lang)
                if col == str(''): break
                print('What is the calory intake...')
                cal=input('')
                print('')
                print('...for this amount...')
                den=input('')
                print('')
                print('...in these units (g for "grams", unit for "units", tsp for "teaspoons", tbsp for "tablespoons", slice for "slices")?')
                un=input('')
            if lang=='ita':
                print('Di che colore sono le calorie di questo cibo?')
                col=input('')
                print('')
                color_check(col,lang)
                if col == str(''): break
                print('Qual è la quantità di calorie...')
                cal=input('')
                print('')
                print('...per questa quantità di cibo...')
                den=input('')
                print('')
                print('...in queste unità (g per "grammi", unit per "unità", tsp per "cucchiaini", tbsp per "cucchiai", slice per "fette")?')
                un=input('')
            if lang=='esp':
                print('Cual es el color de las calorias de este ingrediente?')
                col=input('')
                print('')
                color_check(col,lang)
                if col == str(''): break
                print('Cual es la cuantidad de calorias...')
                cal=input('')
                print('')
                print('...para esta cuantidad del ingrediente...')
                den=input('')
                print('')
                print('...en estas unitas (g para "grammos", unit para "unidades", tsp para "cuchariditas", tbsp para "cucharas", slice para "rebanadas")?')
                un=input('')
            print('')
            if lang=='eng':
                print(str(fd)+': '+str(cal)+' '+str(col)+' Kcal every '+ str(den) +' '+ str(un)+'. Is it correct?')
            if lang=='ita':
                print(str(fd)+': '+str(cal)+' Kcal '+str(col)+' ogni '+ str(den) +' '+ str(un)+". E' corretto?")
            if lang=='esp':
                print(str(fd)+': '+str(cal)+' Kcal '+str(col)+' cada '+ str(den) +' '+ str(un)+'. Es correcto?')
            print('')
            correct=input('')
            print('')
            correct=check(correct,lang)
            if correct =='no' or correct == 'n' or correct == 'nop' or correct == 'nope':
                if lang=='eng':
                    print("Would you like to add it with different settings?")
                if lang=='ita':
                    print("Vuoi aggiungerlo con caratteristiche differenti?")
                if lang=='esp':
                    print("Quieres agregar este ingrediente con caracteristicas diferentes?")
                ans=input('')
                ans=check(ans,lang)
                print('')
                if ans == 'y' or ans == 'yes' or ans == 'si' or ans == 's' or ans == 'yep' or ans == 'eja' or ans == '':
                    zz = 1
                if ans =='no' or ans == 'n' or ans == 'nop' or ans == 'nope':
                    fd = 'empty'
                    zz = 0
            if correct == 'y' or correct == 'yes' or correct == 'si' or correct == 's' or correct == 'yep' or correct == 'eja' or correct == '':
                fd_dtb=np.append(fd_dtb,fd)
                color_dtb=np.append(color_dtb,col)
                cal_dtb=np.append(cal_dtb,cal)
                density_dtb=np.append(density_dtb,den)
                units_dtb=np.append(units_dtb,un)
                ix= np.argsort(fd_dtb)
                fd_dtb,color_dtb,cal_dtb,density_dtb,units_dtb=fd_dtb[ix],color_dtb[ix],cal_dtb[ix],density_dtb[ix],units_dtb[ix]
                dfw_dtb = pd.DataFrame({'food': fd_dtb, 'color': color_dtb, 'calories': cal_dtb, 'every': density_dtb, 'units': units_dtb})
                dfw_dtb.to_csv('Database.csv',index=False)
                zz = 0
        return(fd)







#logging the meals
def meals(top,top_red,top_yellow,top_green,red,yellow,green,core,today,user):
    usr_msk = (core['user'] == user)
    left(top_red,top_yellow,top_green,core[usr_msk][0][4])
    dfr_dtb = pd.read_csv('Database.csv',sep=",", header=None)
    fd_dtb = np.array(dfr_dtb[0][1:]).astype(str)

    x = 1
    while x == 1:
        fd = database_search(core[usr_msk][0][4],dfr_dtb)
        if fd != 'empty':            
            dfr_dtb = pd.read_csv('Database.csv',sep=",", header=None)
            fd_dtb, color_dtb, cal_dtb, density_dtb, units_dtb= np.array(dfr_dtb[0][1:]).astype(str), np.array(dfr_dtb[1][1:]).astype(str), np.array(dfr_dtb[2][1:]).astype(float), np.array(dfr_dtb[3][1:]).astype(float), np.array(dfr_dtb[4][1:]).astype(str)

            if core[usr_msk][0][4]=='eng':
                print('How much/many of this ingredient?')
            if core[usr_msk][0][4]=='ita':
                print('Inserire la quantità')
            if core[usr_msk][0][4]=='esp':
                print('Insertar la cantidad')
            qnt = float(input(''))
            print('')


            fd_msk= fd_dtb==fd
            if color_dtb[fd_msk][0] == 'red':
                par_red_cal = round(cal_dtb[fd_msk][0]*qnt/density_dtb[fd_msk][0])
                temp_top = top-par_red_cal
                temp_red = top_red-par_red_cal
                if temp_red<= 0:
                    if top_yellow + temp_red>=0:
                        temp_yellow = top_yellow + temp_red
                        temp_green = top_green
                    else:
                        temp_green = top_green + (top_yellow + temp_red)
                        temp_yellow = top_yellow + temp_red
                else:
                    temp_yellow = top_yellow
                    temp_green = top_green

                if core[usr_msk][0][4]=='eng':
                    print(str(par_red_cal)+' '+str(color_dtb[fd_msk][0])+' Kcal')
                    print('You would still have '+str(temp_red)+' red Kcal, '+str(temp_yellow)+' yellow Kcal, and '+str(temp_green)+' green Kcal left, for a total of ', str(temp_top)+' Kcal')
                    print('')
                    print('Would you like to log this food?')
                if core[usr_msk][0][4]=='ita':
                    print(str(par_red_cal)+' Kcal rosse')
                    print('Avresti ancora '+str(temp_red)+' Kcal rosse, '+str(temp_yellow)+' Kcal gialle, e '+str(temp_green)+' Kcal verdi rimaste, per un totale di ', str(temp_top)+' Kcal')
                    print('')
                    print('Vuoi loggare questo cibo?')
                if core[usr_msk][0][4]=='esp':
                    print(str(par_red_cal)+' Kcal rojas')
                    print('Dejarian todavia '+str(temp_red)+' Kcal rojas, '+str(temp_yellow)+' Kcal amarillas, y '+str(temp_green)+' Kcal vierdes, para un total de ', str(temp_top)+' Kcal')
                    print('')
                    print('Quieres salvar este ingrediente?')


                log = input('')
                log=check(log,core[usr_msk][0][4])
                if log == 'y' or log == 'yes' or log == 'si' or log == 's' or log == 'yep' or log == 'eja':
                    print('')
                    if core[usr_msk][0][4]=='eng':
                        print("Which meal is it? ('b' for Breakfast, 'l' for Lunch, 'd' for Dinner, 's' for Snack)")
                    if core[usr_msk][0][4]=='ita':
                        print("Che pasto è? ('co' per COlazione, 'p' per Pranzo, 'ce' per CEna, 's' per Snack)")
                    if core[usr_msk][0][4]=='esp':
                        print("Que comida es? ('de' para DEsayuno, 'a' para Almuerzo, 'c' para Cena, 's' para Snack)")
                    ml = ml_check(core[usr_msk][0][4])
                    if ml== 'co' or ml== 'de': ml = 'b'
                    if ml== 'p' or ml== 'a': ml = 'l'
                    if ml== 'ce' or ml== 'c': ml = 'd'
                    print('')
                    top,top_red,top_yellow,top_green,red=temp_top,temp_red,temp_yellow,temp_green,red+par_red_cal
                    dfr = pd.read_csv(str(user)+'_'+str(today)+'.csv',sep=",", header=None)
                    full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(dfr[0][1:]).astype(float), np.array(dfr[1][1:]).astype(float), np.array(dfr[2][1:]).astype(float), np.array(dfr[3][1:]).astype(float), np.array(dfr[4][1:]).astype(float), np.array(dfr[5][1:]).astype(float), np.array(dfr[6][1:]).astype(float), np.array(dfr[7][1:]), np.array(dfr[8][1:]).astype(float), np.array(dfr[9][1:]), np.array(dfr[10][1:])
                    full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal=np.append(full_top,top), np.append(full_top_red,top_red), np.append(full_top_yellow,top_yellow), np.append(full_top_green,top_green), np.append(full_red,red), np.append(full_yellow,yellow), np.append(full_green,green), np.append(full_ingr,str(fd)), np.append(full_cal,par_red_cal), np.append(full_color,str(color_dtb[fd_msk][0])),np.append(full_meal,str(ml))
                    dfw = pd.DataFrame({'top': full_top, 'red_left': full_top_red, 'yellow_left': full_top_yellow, 'green_left': full_top_green, 'red': full_red, 'yellow': full_yellow, 'green': full_green, 'ingredients': full_ingr, 'calories': full_cal, 'color': full_color, 'meal': full_meal})
                    dfw.to_csv(str(user)+'_'+str(today)+'.csv',index=False)
                if log == 'no' or log == 'n' or log == 'nop' or log == 'nope':
                    print('')


            if color_dtb[fd_msk][0] == 'yellow':
                par_yellow_cal = round(cal_dtb[fd_msk][0]*qnt/density_dtb[fd_msk][0])
                temp_top = top-par_yellow_cal
                temp_yellow = top_yellow-par_yellow_cal
                if temp_yellow <= 0:
                    if top_red + temp_yellow>=0:
                        temp_red = top_red + temp_yellow
                        temp_green = top_green
                    else:
                        temp_green = top_green + (top_red + temp_yellow)
                        temp_red = top_red + temp_yellow
                else:
                    temp_red = top_red
                    temp_green = top_green

                if core[usr_msk][0][4]=='eng':
                    print(str(par_yellow_cal)+' '+str(color_dtb[fd_msk][0])+' Kcal')
                    print('You would still have '+str(temp_red)+' red Kcal, '+str(temp_yellow)+' yellow Kcal, and '+str(temp_green)+' green Kcal left, for a total of ', str(temp_top)+' Kcal')
                    print('')
                    print('Would you like to log this food?')
                if core[usr_msk][0][4]=='ita':
                    print(str(par_yellow_cal)+' Kcal gialle')
                    print('Avresti ancora '+str(temp_red)+' Kcal rosse, '+str(temp_yellow)+' Kcal gialle, e '+str(temp_green)+' Kcal verdi rimaste, per un totale di ', str(temp_top)+' Kcal')
                    print('')
                    print('Vuoi loggare questo cibo?')
                if core[usr_msk][0][4]=='esp':
                    print(str(par_yellow_cal)+' Kcal amarillas')
                    print('Dejarian todavia '+str(temp_red)+' Kcal rojas, '+str(temp_yellow)+' Kcal amarillas, y '+str(temp_green)+' Kcal vierdes, para un total de ', str(temp_top)+' Kcal')
                    print('')
                    print('Quieres salvar este ingrediente?')

                log = input('')
                log=check(log,core[usr_msk][0][4])
                if log == 'y' or log == 'yes' or log == 'si' or log == 's' or log == 'yep' or log == 'eja':
                    print('')
                    if core[usr_msk][0][4]=='eng':
                        print("Which meal is it? ('b' for Breakfast, 'l' for Lunch, 'd' for Dinner, 's' for Snack)")
                    if core[usr_msk][0][4]=='ita':
                        print("Che pasto è? ('co' per COlazione, 'p' per Pranzo, 'ce' per CEna, 's' per Snack)")
                    if core[usr_msk][0][4]=='esp':
                        print("Que comida es? ('de' para DEsayuno, 'a' para Almuerzo, 'c' para Cena, 's' para Snack)")
                    ml = ml_check(core[usr_msk][0][4])
                    if ml== 'co' or ml== 'de': ml = 'b'
                    if ml== 'p' or ml== 'a': ml = 'l'
                    if ml== 'ce' or ml== 'c': ml = 'd'
                    print('')
                    top,top_red,top_yellow,top_green,yellow=temp_top,temp_red,temp_yellow,temp_green,yellow+par_yellow_cal
                    dfr = pd.read_csv(str(user)+'_'+str(today)+'.csv',sep=",", header=None)
                    full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(dfr[0][1:]).astype(float), np.array(dfr[1][1:]).astype(float), np.array(dfr[2][1:]).astype(float), np.array(dfr[3][1:]).astype(float), np.array(dfr[4][1:]).astype(float), np.array(dfr[5][1:]).astype(float), np.array(dfr[6][1:]).astype(float), np.array(dfr[7][1:]), np.array(dfr[8][1:]).astype(float), np.array(dfr[9][1:]), np.array(dfr[10][1:])
                    full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal=np.append(full_top,top), np.append(full_top_red,top_red), np.append(full_top_yellow,top_yellow), np.append(full_top_green,top_green), np.append(full_red,red), np.append(full_yellow,yellow), np.append(full_green,green), np.append(full_ingr,str(fd)), np.append(full_cal,par_yellow_cal), np.append(full_color,str(color_dtb[fd_msk][0])),np.append(full_meal,str(ml))
                    dfw = pd.DataFrame({'top': full_top, 'red_left': full_top_red, 'yellow_left': full_top_yellow, 'green_left': full_top_green, 'red': full_red, 'yellow': full_yellow, 'green': full_green, 'ingredients': full_ingr, 'calories': full_cal, 'color': full_color, 'meal': full_meal})
                    dfw.to_csv(str(user)+'_'+str(today)+'.csv',index=False)
                if log == 'no' or log == 'n' or log == 'nop' or log == 'nope':
                    print('')


            if color_dtb[fd_msk] == 'green':
                par_green_cal = round(cal_dtb[fd_msk][0]*qnt/density_dtb[fd_msk][0])
                temp_top = top-par_green_cal
                temp_green = top_green-par_green_cal
                if temp_green >= 0:
                    temp_red = top_red
                    temp_yellow = top_yellow
                else:
                    if top_yellow+round(temp_green/2)>=0 and top_red+round(temp_green/2)>=0:
                        temp_red = top_red+round(temp_green/2)
                        temp_yellow = top_yellow+round(temp_green/2)
                    else:
                        if top_yellow + temp_green>=0:
                            temp_yellow = top_yellow + temp_green
                            temp_red = top_red
                        if (top_yellow + temp_green<0) and (top_red + temp_green>=0):
                            temp_yellow = top_yellow
                            temp_red = top_red + temp_green
            
                if core[usr_msk][0][4]=='eng':
                    print(str(par_green_cal)+' '+str(color_dtb[fd_msk][0])+' Kcal')
                    print('You would still have '+str(temp_red)+' red Kcal, '+str(temp_yellow)+' yellow Kcal, and '+str(temp_green)+' green Kcal left, for a total of ', str(temp_top)+' Kcal')
                    print('')
                    print('Would you like to log this food?')
                if core[usr_msk][0][4]=='ita':
                    print(str(par_green_cal)+' Kcal verdi')
                    print('Avresti ancora '+str(temp_red)+' Kcal rosse, '+str(temp_yellow)+' Kcal gialle, e '+str(temp_green)+' Kcal verdi rimaste, per un totale di ', str(temp_top)+' Kcal')
                    print('')
                    print('Vuoi loggare questo cibo?')
                if core[usr_msk][0][4]=='esp':
                    print(str(par_yellow_cal)+' Kcal vierdes')
                    print('Dejarian todavia '+str(temp_red)+' Kcal rojas, '+str(temp_yellow)+' Kcal amarillas, y '+str(temp_green)+' Kcal vierdes, para un total de ', str(temp_top)+' Kcal')
                    print('')
                    print('Quieres salvar este ingrediente?')
                log = input('')
                log=check(log,core[usr_msk][0][4])
                if log == 'y' or log == 'yes' or log == 'si' or log == 's' or log == 'yep' or log == 'eja':
                    print('')
                    if core[usr_msk][0][4]=='eng':
                        print("Which meal is it? ('b' for Breakfast, 'l' for Lunch, 'd' for Dinner, 's' for Snack)")
                    if core[usr_msk][0][4]=='ita':
                        print("Che pasto è? ('co' per COlazione, 'p' per Pranzo, 'ce' per CEna, 's' per Snack)")
                    if core[usr_msk][0][4]=='esp':
                        print("Que comida es? ('de' para DEsayuno, 'a' para Almuerzo, 'c' para Cena, 's' para Snack)")
                    ml = ml_check(core[usr_msk][0][4])
                    if ml== 'co' or ml== 'de': ml = 'b'
                    if ml== 'p' or ml== 'a': ml = 'l'
                    if ml== 'ce' or ml== 'c': ml = 'd'

                    top,top_red,top_yellow,top_green,green=temp_top,temp_red,temp_yellow,temp_green,green+par_green_cal
                    dfr = pd.read_csv(str(user)+'_'+str(today)+'.csv',sep=",", header=None)
                    full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(dfr[0][1:]).astype(float), np.array(dfr[1][1:]).astype(float), np.array(dfr[2][1:]).astype(float), np.array(dfr[3][1:]).astype(float), np.array(dfr[4][1:]).astype(float), np.array(dfr[5][1:]).astype(float), np.array(dfr[6][1:]).astype(float), np.array(dfr[7][1:]), np.array(dfr[8][1:]).astype(float), np.array(dfr[9][1:]), np.array(dfr[10][1:])
                    full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal=np.append(full_top,top), np.append(full_top_red,top_red), np.append(full_top_yellow,top_yellow), np.append(full_top_green,top_green), np.append(full_red,red), np.append(full_yellow,yellow), np.append(full_green,green), np.append(full_ingr,str(fd)), np.append(full_cal,par_green_cal), np.append(full_color,str(color_dtb[fd_msk][0])),np.append(full_meal,str(ml))
                    dfw = pd.DataFrame({'top': full_top, 'red_left': full_top_red, 'yellow_left': full_top_yellow, 'green_left': full_top_green, 'red': full_red, 'yellow': full_yellow, 'green': full_green, 'ingredients': full_ingr, 'calories': full_cal, 'color': full_color, 'meal': full_meal})
                    dfw.to_csv(str(user)+'_'+str(today)+'.csv',index=False)
                    print('')
                if log == 'no' or log == 'n' or log == 'nop' or log == 'nope':
                    print('')
        

                
        if core[usr_msk][0][4]=='eng':
            print('Would you like to log other food?')
        if core[usr_msk][0][4]=='ita':
            print('Vorresti aggiungere altro cibo?')
        if core[usr_msk][0][4]=='eng':
            print('Quieres agregar otros ingredientes?')
        other=input('')
        other=check(other,core[usr_msk][0][4])
        print('')
        if other  == 'y' or other == 'yes' or other == 'si' or other == 's' or other == 'yep' or other == 'eja':
            x=1
        if other == 'no' or other == 'n' or other == 'nop' or other == 'nope':
            x=0
    
    left(top_red,top_yellow,top_green,core[usr_msk][0][4])
    return(top,top_red,top_yellow,top_green,red,yellow,green)

"""
#QUESTO SERVIREBBE SE DECIDESSI DI AGGIUNGERE UNA FUNZIONE PER LOGGARE IL CIBO SEGNATO QUI SOTTO. ANDREBBE TUTTO AL POSTO DI 'def simulation(core):'
def simulation(today,arr,core,user):
    
    if user+'_'+today+'.csv' not in arr:
        top=float(core[usr_msk][0][0])
        top_red=float(core[usr_msk][0][1])
        top_yellow=float(core[usr_msk][0][2])
        top_green=float(core[usr_msk][0][3])
        red,yellow,green=0.0,0.0,0.0
        df = pd.DataFrame({'top': [top], 'red_left': [top_red], 'yellow_left': [top_yellow], 'green_left': [top_green], 'red': [red], 'yellow': [yellow], 'green': [green], 'ingredients': ['-'], 'calories': [0], 'color':['-'], 'meal': ['-']})
        df.to_csv(str(user)+'_'+str(today)+'.csv',index=False)
    else:
        df = pd.read_csv(str(user)+'_'+str(today)+'.csv',sep=",", header=None)
        full_top, full_top_red, full_top_yellow, full_top_green, full_red, full_yellow, full_green, full_ingr, full_cal, full_color, full_meal= np.array(df[0][1:]).astype(float), np.array(df[1][1:]).astype(float), np.array(df[2][1:]).astype(float), np.array(df[3][1:]).astype(float), np.array(df[4][1:]).astype(float), np.array(df[5][1:]).astype(float), np.array(df[6][1:]).astype(float), np.array(df[7][1:]), np.array(df[8][1:]).astype(float), np.array(df[9][1:]), np.array(df[10][1:])
        top, top_red, top_yellow, top_green, red, yellow, green=full_top[-1], full_top_red[-1], full_top_yellow[-1], full_top_green[-1], full_red[-1], full_yellow[-1], full_green[-1]
    """
def simulation(core,user):
    usr_msk=(core['user']==user)
    cc,temp_red,temp_yellow,temp_green = 1,0.0,0.0,0.0
    extra_fd,extra_qnt,extra_un = np.array([]),np.array([]),np.array([])
    while cc == 1:
        dfr_dtb = pd.read_csv('Database.csv',sep=",", header=None)
        temp_fd = database_search(core[usr_msk][0][4],dfr_dtb)
        if temp_fd != 'empty':            
            dfr_dtb = pd.read_csv('Database.csv',sep=",", header=None) #non spostarlo da qui
            fd_dtb, color_dtb, cal_dtb, density_dtb, units_dtb= np.array(dfr_dtb[0][1:]).astype(str), np.array(dfr_dtb[1][1:]).astype(str), np.array(dfr_dtb[2][1:]).astype(float), np.array(dfr_dtb[3][1:]).astype(float), np.array(dfr_dtb[4][1:]).astype(str)

            if core[usr_msk][0][4]=='eng':
                print('How much/many of this ingredient?')
            if core[usr_msk][0][4]=='ita':
                print('Inserire la quantità')
            if core[usr_msk][0][4]=='esp':
                print('Insertar la cantidad')
            qnt = float(input(''))
            print('')

            fd_msk= fd_dtb==temp_fd
            if qnt != 0 and qnt != 0.0:
                extra_fd = np.append(extra_fd,temp_fd)
                extra_qnt = np.append(extra_qnt,qnt)
                extra_un = np.append(extra_un,units_dtb[fd_msk][0])
                temp_cal=round(cal_dtb[fd_msk][0]*qnt/density_dtb[fd_msk][0])
                if color_dtb[fd_msk][0] == 'red':
                    temp_red=temp_red+temp_cal
                if color_dtb[fd_msk][0] == 'yellow':
                    temp_yellow=temp_yellow+temp_cal
                if color_dtb[fd_msk][0] == 'green':
                    temp_green=temp_green+temp_cal
            
            if core[usr_msk][0][4]=='eng':
                print('Would you like to add other food?')
            if core[usr_msk][0][4]=='ita':
                print('Vorresti aggiungere altro cibo?')
            if core[usr_msk][0][4]=='eng':
                print('Quieres agregar otros ingredientes?')
            other=input('')
            other=check(other,core[usr_msk][0][4])
            print('')
            if other  == 'y' or other == 'yes' or other == 'si' or other == 's' or other == 'yep' or other == 'eja':
                cc = 1
            if other == 'no' or other == 'n' or other == 'nop' or other == 'nope':
                cc = 0

    tot = temp_red+temp_yellow+temp_green        
    if core[usr_msk][0][4]=='eng':
        print('This meal contains:')
        for i in range(len(extra_fd)):
            print(str(extra_qnt[i])+' '+str(extra_un[i])+' of '+str(extra_fd[i]))
        print('')
        print('For a total of '+str(tot)+' Kcal. Of which:')
        print(str(temp_red)+' RED')
        print(str(temp_yellow)+' YELLOW')
        print(str(temp_green)+' GREEN')
    if core[usr_msk][0][4]=='ita':
        print('Questo pasto contiene:')
        for i in range(len(extra_fd)):
            print(str(extra_qnt[i])+' '+str(extra_un[i])+' di '+str(extra_fd[i]))
        print('')
        print('Per un totale di '+str(tot)+' Kcal. Di cui:')
        print(str(temp_red)+' ROSSE')
        print(str(temp_yellow)+' GIALLE')
        print(str(temp_green)+' VERDI')
    if core[usr_msk][0][4]=='esp':
        print('Esta comida contiene:'+str(tot)+' Kcal. De esas:')
        for i in range(len(extra_fd)):
            print(str(extra_qnt[i])+' '+str(extra_un[i])+' de '+str(extra_fd[i]))
        print('')
        print('Por un total de '+str(tot)+' Kcal. De esas:')
        print(str(temp_red)+' ROJAS')
        print(str(temp_yellow)+' AMARILLAS')
        print(str(temp_green)+' VERDES')

    return()