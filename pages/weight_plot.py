import streamlit as st
import glob #THIS IS TO IMPORT DIFFERENT FILES INTO THE MEMORY (IN THE CASE OF LESSON 8, IMAGES)
import pandas as pd
import streamlit_pandas as sp # IT HELPS TO QUERY A DATABASE.
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import os
import csv
from scipy.interpolate import UnivariateSpline
#from matteo3 import setup, left, plot, nw, wo, meals, check, check_setup, check_language, database_update, database_search, add_user_name, select_first_user, select_user,past_meals,simulation



st.header("Weight plot")

#st.write("This page will contain the plot of the weights, and the possibility to add a new weight.")
"""
- Aggiusta la larghezza/altezza del plot.
"""
arr = os.listdir('.')

today = date.today()
today=today.strftime("%d_%m_%Y")

if "usr" in st.session_state and st.session_state.usr != 'new' and  st.session_state.usr != None:
    usr = st.session_state.usr
    weight=np.load('weight.npy',allow_pickle=True)
    days=np.load('days.npy',allow_pickle=True)
    core=np.load('core.npy',allow_pickle=True)
    users = core['user']
    users = np.append(users,'new')
    usr_msk = (core['user'] == usr)
    usr_days_msk = (days['user'] == usr)
    usr_weight_msk = (weight['user'] == usr)


#plotting function
def plot(core,days,weight,user):
    if len(days)<1:
        if core['lang'][0]=='eng' or core['lang'][0]=='Eng':
            print('No weights to show, yet')
        if core['lang'][0]=='ita' or core['lang'][0]=='Ita':
            print('Non ci sono ancora pesate da mostrare')
        if core['lang'][0]=='esp' or core['lang'][0]=='Esp':
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
    
    if core['lang'][0]=='eng' or core['lang'][0]=='Eng':
        width = st.sidebar.slider("Plot width", 1, 25, 15)
        height = st.sidebar.slider("Plot height", 1, 25, 5)
    if core['lang'][0]=='ita' or core['lang'][0]=='Ita':
        width = st.sidebar.slider("Larghezza", 1, 25, 15)
        height = st.sidebar.slider("Altezza", 1, 25, 5)
    if core['lang'][0]=='esp' or core['lang'][0]=='Esp':
        width = st.sidebar.slider("Anchura", 1, 25, 15)
        height = st.sidebar.slider("Altura", 1, 25, 5)
    fig1 = plt.figure(figsize=(width,height))
    gs = fig1.add_gridspec(1,1)
    ax1= fig1.add_subplot(gs[0,0])
    spl_date = np.arange(len(days))
    spl = UnivariateSpline(spl_date, weight)
    spl.set_smoothing_factor(len(days)//7)
    if core['lang'][0]=='eng' or core['lang'][0]=='Eng':
        ax1.set_ylabel(r"$Weight\,(kg)$", fontsize=18)
        ax1.set_xlabel(r"$Day$", fontsize=18)
    if core['lang'][0]=='ita' or core['lang'][0]=='Ita':
        ax1.set_ylabel(r"$Peso\,(kg)$", fontsize=18)
        ax1.set_xlabel(r"$Data$", fontsize=18)
    if core['lang'][0]=='esp' or core['lang'][0]=='Esp':
        ax1.set_ylabel(r"$Peso\,(kg)$", fontsize=18)
        ax1.set_xlabel(r"$Fecha$", fontsize=18)
    ax1.set_ylim(ymin=min(weight-0.2),ymax=max(weight+0.2))
    ax1.plot(days,weight,linewidth=1,color='k')
    ax1.plot(spl_date,spl(spl_date),linewidth=1,color='r')
    ax1.scatter(days,weight,s=(60-len(days)//3),color='r')
    sup = (max(weight+0.2)-min(weight-0.2))/40
    for h in range(len(days)):
        plt.text(days[h],weight[h],str(weight[h]),fontsize=(18-len(days)//6),position=(days[h],weight[h]+sup))
    if core['lang'][0]=='eng' or core['lang'][0]=='Eng':
        fig1.suptitle(r"Average dayly loss: "+str(avg_loss)+r"$\,$Kg",fontsize=16)
    if core['lang'][0]=='ita' or core['lang'][0]=='Ita':
        fig1.suptitle(r"Perdita di peso media giornaliera: "+str(avg_loss)+r"$\,$Kg",fontsize=16)
    if core['lang'][0]=='esp' or core['lang'][0]=='Esp':
        fig1.suptitle(r"Perdida de peso media diaria: "+str(avg_loss)+r"$\,$Kg",fontsize=16)
    ax1.set_xticks(ticks=days)
    newdays = np.copy(days)
    for i in range(len(newdays)):
        newdays[i] = newdays[i][:-5]
    ax1.set_xticklabels(labels=newdays,fontsize=(14-len(days)//5))
    ax1.tick_params('y',labelsize=(14-len(days)//5))
    st.pyplot(fig1)
    return()


#function to add the new daily weight
def nw(weight,days,core,today,user):
    usr_msk = (core['user'] == user)
    usr_days_msk = (days['user'] == user)
    usr_weight_msk = (weight['user'] == user)
    if today in days[usr_days_msk]['date']:
        change_msk= (days['user']==user) & (days['date']==today)
        st.write(weight[change_msk]['weight'])
        if core[usr_msk][0][4]=='eng' or core[usr_msk][0][4]=='Eng':
            neweight = st.number_input("Daily weight",value=weight[change_msk]['weight'][0])
            info = st.button("Update")
        if core[usr_msk][0][4]=='ita' or core[usr_msk][0][4]=='Ita':
            neweight = st.number_input("Pesata giornaliera",value=weight[change_msk]['weight'][0])
            info = st.button("Aggiorna")
        if core[usr_msk][0][4]=='esp' or core[usr_msk][0][4]=='Esp':
            neweight = st.number_input("Pesada diaria",value=weight[change_msk]['weight'][0])
            info = st.button("Actualiza")
        
        if info:
            neweight=float(neweight)
            change_msk= (days['user']==user) & (days['date']==today)
            weight = weight[~change_msk]
            temp_weight_user, temp_weight_weight = weight['user'], weight['weight']
            temp_weight_user, temp_weight_weight = np.append(temp_weight_user,str(user)), np.append(temp_weight_weight,neweight)
            weight = np.rec.array([temp_weight_user,temp_weight_weight], names=['user','weight'])
            print('')
        
    
    if today not in days[usr_days_msk]['date']:
        if core[usr_msk][0][4]=='eng' or core[usr_msk][0][4]=='Eng':
            neweight = st.number_input("Upload daily weight (in kg)")
            info = st.button("Upload")
        if core[usr_msk][0][4]=='ita' or core[usr_msk][0][4]=='Ita':
            neweight = st.number_input("Caricare la pesata giornaliera (in kg)")
            info = st.button("Carica")
        if core[usr_msk][0][4]=='esp' or core[usr_msk][0][4]=='Esp':
            neweight = st.number_input("Cargar la pesada diaria (en kg)")
            info = st.button("Carga")
        
        
        if info:
            neweight=float(neweight)
            temp_days_user, temp_days_date = days['user'], days['date']
            temp_weight_user, temp_weight_weight = weight['user'], weight['weight']
            temp_days_user, temp_days_date = np.append(temp_days_user,str(user)), np.append(temp_days_date,today)
            temp_weight_user, temp_weight_weight = np.append(temp_weight_user,str(user)), np.append(temp_weight_weight,neweight)
            days, weight = np.rec.array([temp_days_user,temp_days_date], names=['user','date']), np.rec.array([temp_weight_user,temp_weight_weight], names=['user','weight'])
            np.save('days.npy',days)
    np.save('weight.npy',weight)

    return(weight,days)
    








if "usr" in st.session_state and st.session_state.usr != 'new' and  st.session_state.usr != None:
    weight,days=nw(weight,days,core,today,usr)
    usr_msk = (core['user'] == usr)
    usr_days_msk = (days['user'] == usr)
    usr_weight_msk = (weight['user'] == usr)
    plot(core[usr_msk],days[usr_days_msk]['date'],weight[usr_weight_msk]['weight'],usr)
else:
    st.write("Please, select a User from the main page.")
    st.write("Per favore, selezionare un Utente dalla pagina principale.")
    st.write("Por favor, elegir un Usuario de la pagina principal.")



    




