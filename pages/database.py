import streamlit as st
import glob #THIS IS TO IMPORT DIFFERENT FILES INTO THE MEMORY (IN THE CASE OF LESSON 8, IMAGES)
#LEZIONE 7: MULTI-PAGE APP.
#THE TWO "IMPORT" THAT FOLLOW ARE FOR THE LAST LESSON:
import pandas as pd
import streamlit_pandas as sp # IT HELPS TO QUERY A DATABASE.
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import os
import csv
from scipy.interpolate import UnivariateSpline
#from matteo3 import setup, left, plot, nw, wo, meals, check, check_setup, check_language, database_update, database_search, add_user_name, select_first_user, select_user,past_meals,simulation



st.header("Food Database")

st.write("This page will contain the ingredients' database, the possibility to add a new ingredient, and to simulate (SIM) a receipe.")

"""
- This page will contain the DTB and SIM functions. This involves a showing the database, the use of STREAMLIT-PANDAS to decide what to show (only red/yellow/green calories and so on).
- To add new ingredients to the database, you'll need some NUMERICAL AND CHARACTER INPUT, and some SELECT to decide the units, the color of the calories and stuff like this.
- Try to avoid the fact that you have to press every submit_button several times.
- Try to refresh the default values in the widgets inside the form, after pressing the submit button.
- STREAMLIT HAS BIG PROBLEMS WITH THE "ENTER" BUTTON. SE NON PREMI ENTER DOPO AVER INSERITO UN INPUT DI TESTO, NON SEMPRE CAPISCE. CERCA DI CAPIRE COME EVITARLO.

- For the SIM part, you'll think about it. You'll need either a CHARACTER INPUT, or something to combine it with other buttons and stuff like that.
"""


arr = os.listdir('.')

today = date.today()
today=today.strftime("%d_%m_%Y")
core=np.load('core.npy',allow_pickle=True)

@st.cache_data()
def load_data(i): #this is to load the data once and for all
    df = pd.read_csv("Database.csv")
    return(df)
if "i" not in st.session_state:
    st.session_state.i=0
    
df = load_data(st.session_state.i)
create_data = {
                "food": "text",
                "color": "multiselect",
                "units": "multiselect"
                }
all_widgets = sp.create_widgets(df, create_data, ignore_columns=["every"])
res = sp.filter_df(df, all_widgets)

st.write(res)



#def dtb_update(df,fd_dtb,ingr,colr,calr,ever,un,lan,form_dtb):
#    if colr == "Rosse" or colr == "Rojas": colr = 'red'
#    if colr == "Gialle" or colr == "Amarillas": colr = 'yellow'
#    if colr == "Verdi" or colr == "Verdes": colr = 'green'
#    if un == "fetta" or colr == "rebanada": colr = 'slice'
#    if un == "cucc" or colr == "cuch": colr = 'tbsp'
#    if un == "cucc.no" or colr == "cuch.ita": colr = 'tsp'
#    if un == "unità" or colr == "unidad": colr = 'unit'
#    color_dtb, cal_dtb, density_dtb, units_dtb = np.array(df['color']), #np.array(df['calories']), np.array(df['every']), np.array(df['units'])
#    if ingr == "" or colr == "" or calr == "" or ever == "" or un == "": return()
#    
#    if ingr not in fd_dtb:
#        fd_dtb, color_dtb, cal_dtb, density_dtb, units_dtb = np.append(fd_dtb,ingr), #np.append(color_dtb,colr), np.append(cal_dtb,calr), np.append(density_dtb,ever), #np.append(units_dtb,un)
#        ix= np.argsort(fd_dtb)
#        #fd_dtb,color_dtb,cal_dtb,density_dtb,units_dtb=fd_dtb[ix],color_dtb[ix],cal_dtb[ix],density_dtb[ix],units_dtb[ix]
#        dfw_dtb = pd.DataFrame({'food': fd_dtb, 'color': color_dtb, 'calories': cal_dtb, #'every': density_dtb, 'units': units_dtb})
#        dfw_dtb.to_csv('Database.csv',index=False)
#        if lan=='eng' or lan=='Eng' or "usr" not in st.session_state or st.session_state.usr == #'new' or  st.session_state.usr == None:
#            form_dtb.write("Done!")
#        if lan=='ita' or lan=='Ita':
#            form_dtb.write("Fatto!")
#        if lan=='esp' or lan=='Esp':
#            form_dtb.write("Hecho!")
#        return()
#    
#    if ingr in fd_dtb:
#        #PROVA A VEDERE SE PUOI CREARE UN'ALTRA FORM (NON NESTED)
#        fd_msk = (fd_dtb == ingr)
#        fd_msk2 = (df['food'] == ingr)
#        if lan=='eng' or lan=='Eng' or "usr" not in st.session_state or st.session_state.usr == #'new' or  st.session_state.usr == None:
#            form_dtb.write("The specified ingredient is already included in the Database:")
#            form_dtb.write(df[fd_msk2])
#            form_dtb.write("Would you like to update it?")
#        if lan=='ita' or lan=='Ita':
#            form_dtb.write("L'ingrediente selezionato è già presente nel Database:")
#            form_dtb.write(df[fd_msk2])
#            form_dtb.write("Lo vorresti aggiornare?")
#        if lan=='esp' or lan=='Esp':
#            form_dtb.write("El ingrediente seleccionado ya està presente en el Database:")
#            form_dtb.write(df[fd_msk2])
#            form_dtb.write("Querias actualizarlo?")
#        col = form_dtb.columns(2)
#        if lan=='eng' or lan=='Eng' or "usr" not in st.session_state or st.session_state.usr == #'new' or  st.session_state.usr == None:
#            conf = col[0].button("Yes")
#            den = col[1].button("No")
#        if lan=='ita' or lan=='Ita' or lan=='esp' or lan=='Esp':
#            conf = col[0].button("Yes")
#            den = col[1].button("No")
#        if den: return()
#        if conf:
#            fd_dtb, color_dtb, cal_dtb, density_dtb, units_dtb = fd_dtb[~fd_msk], #color_dtb[~fd_msk], cal_dtb[~fd_msk], density_dtb[~fd_msk], units_dtb[~fd_msk]
#            fd_dtb, color_dtb, cal_dtb, density_dtb, units_dtb = np.append(fd_dtb,ingr), #np.append(color_dtb,colr), np.append(cal_dtb,calr), np.append(density_dtb,ever), #np.append(units_dtb,un)
#            ix= np.argsort(fd_dtb)
#            #fd_dtb,color_dtb,cal_dtb,density_dtb,units_dtb=fd_dtb[ix],color_dtb[ix],cal_dtb[ix],density_dtb[ix],units_dtb[ix]
#            dfw_dtb = pd.DataFrame({'food': fd_dtb, 'color': color_dtb, 'calories': cal_dtb, #'every': density_dtb, 'units': units_dtb})
#            dfw_dtb.to_csv('Database.csv',index=False)
#            if lan=='eng' or lan=='Eng' or "usr" not in st.session_state or st.session_state.usr #== 'new' or  st.session_state.usr == None:
#                form_dtb.write("Done!")
#            if lan=='ita' or lan=='Ita':
#                form_dtb.write("Fatto!")
#            if lan=='esp' or lan=='Esp':
#                form_dtb.write("Hecho!")
#            return()


def add_to_dtb(df,fd_dtb,ingr,colr,calr,ever,un,lan,form_dtb):
    if colr == "Rosse" or colr == "Rojas": colr = 'red'
    if colr == "Gialle" or colr == "Amarillas": colr = 'yellow'
    if colr == "Verdi" or colr == "Verdes": colr = 'green'
    if un == "fetta" or colr == "rebanada": colr = 'slice'
    if un == "cucc" or colr == "cuch": colr = 'tbsp'
    if un == "cucc.no" or colr == "cuch.ita": colr = 'tsp'
    if un == "unità" or colr == "unidad": colr = 'unit'
    color_dtb, cal_dtb, density_dtb, units_dtb = np.array(df['color']), np.array(df['calories']), np.array(df['every']), np.array(df['units'])
    if ingr in fd_dtb or ingr == "" or colr == "" or calr == "" or ever == "" or un == "": return()
    #if ingr not in fd_dtb:
    fd_dtb, color_dtb, cal_dtb, density_dtb, units_dtb = np.append(fd_dtb,ingr), np.append(color_dtb,colr), np.append(cal_dtb,float(calr)), np.append(density_dtb,float(ever)), np.append(units_dtb,un)
    ix= np.argsort(fd_dtb)
    fd_dtb,color_dtb,cal_dtb,density_dtb,units_dtb=fd_dtb[ix],color_dtb[ix],cal_dtb[ix],density_dtb[ix],units_dtb[ix]
    dfw_dtb = pd.DataFrame({'food': fd_dtb, 'color': color_dtb, 'calories': cal_dtb, 'every': density_dtb, 'units': units_dtb})
    dfw_dtb.to_csv('Database.csv',index=False)
    if lan=='eng' or lan=='Eng':
        form_dtb.write("Done!")
    if lan=='ita' or lan=='Ita':
        form_dtb.write("Fatto!")
    if lan=='esp' or lan=='Esp':
        form_dtb.write("Hecho!")
    return()


def update_dtb(df,fd_dtb,ingr,colr,calr,ever,un,lan,form_dtb):
    if colr == "Rosse" or colr == "Rojas": colr = 'red'
    if colr == "Gialle" or colr == "Amarillas": colr = 'yellow'
    if colr == "Verdi" or colr == "Verdes": colr = 'green'
    if un == "fetta" or colr == "rebanada": colr = 'slice'
    if un == "cucc" or colr == "cuch": colr = 'tbsp'
    if un == "cucc.no" or colr == "cuch.ita": colr = 'tsp'
    if un == "unità" or colr == "unidad": colr = 'unit'
    color_dtb, cal_dtb, density_dtb, units_dtb = np.array(df['color']), np.array(df['calories']), np.array(df['every']), np.array(df['units'])
    if ingr == "" or colr == "" or calr == "" or ever == "" or un == "": return()
    
    fd_msk = (fd_dtb == ingr)
    
    fd_msk2 = (df['food'] == ingr)
    if lan=='eng' or lan=='Eng':
        st.write("The specified ingredient is already included in the Database:")
        st.write(df[fd_msk2])
        st.write("Would you like to update it?")
    if lan=='ita' or lan=='Ita':
        st.write("L'ingrediente selezionato è già presente nel Database:")
        st.write(df[fd_msk2])
        st.write("Lo vorresti aggiornare?")
    if lan=='esp' or lan=='Esp':
        st.write("El ingrediente seleccionado ya està presente en el Database:")
        st.write(df[fd_msk2])
        st.write("Querias actualizarlo?")
    col = st.columns(2)
    if lan == 'eng' or lan == 'Eng':
        conf = col[0].button("Yes")
        den = col[1].button("No")
    if lan=='ita' or lan=='Ita' or lan=='esp' or lan=='Esp':
        conf = col[0].button("Sì")
        den = col[1].button("No")
    if den: return()
    if conf:
        fd_dtb, color_dtb, cal_dtb, density_dtb, units_dtb = fd_dtb[~fd_msk], color_dtb[~fd_msk], cal_dtb[~fd_msk], density_dtb[~fd_msk], units_dtb[~fd_msk]
        fd_dtb, color_dtb, cal_dtb, density_dtb, units_dtb = np.append(fd_dtb,ingr), np.append(color_dtb,colr), np.append(cal_dtb,float(calr)), np.append(density_dtb,float(ever)), np.append(units_dtb,un)
        ix= np.argsort(fd_dtb)
        fd_dtb,color_dtb,cal_dtb,density_dtb,units_dtb=fd_dtb[ix],color_dtb[ix],cal_dtb[ix],density_dtb[ix],units_dtb[ix]
        dfw_dtb = pd.DataFrame({'food': fd_dtb, 'color': color_dtb, 'calories': cal_dtb, 'every': density_dtb, 'units': units_dtb})
        dfw_dtb.to_csv('Database.csv',index=False)
        if lan=='eng' or lan=='Eng':
            st.write("Done!")
        if lan=='ita' or lan=='Ita':
            st.write("Fatto!")
        if lan=='esp' or lan=='Esp':
            st.write("Hecho!")
        return()

def dtb(df,lan,i):
    fd_dtb = np.array(df['food'])

    form_dtb =  st.form(key='add_to_dtb')
    cols = form_dtb.columns(5)
    if lan=='eng' or lan=='Eng':
        ingr = cols[0].text_input("",placeholder="New Ingredient")
        colr = cols[1].selectbox("",("Red","Yellow","Green"), index = None, placeholder = "Color")
        calr = cols[2].text_input("",placeholder="Calories")
        ever = cols[3].selectbox("",("1","100"), index = None, placeholder = "Every")
        un = cols[4].selectbox("",("g","slice","tbsp","tsp","unit"), index = None, placeholder = "Units")
        #save_fd = form_dtb.form_submit_button("Add to Database", on_click = add_to_dtb, args = (df,fd_dtb,ingr,colr,calr,ever,un,core[usr_msk]['lang'][0],form_dtb))
        save_fd = form_dtb.form_submit_button("Add to Database")
    if lan=='ita' or lan=='Ita':
        ingr = cols[0].text_input("",placeholder="Nuovo Ingrediente")
        colr = cols[1].selectbox("",("Rosse","Gialle","Verdi"), index = None, placeholder = 'Colore')
        calr = cols[2].text_input("",placeholder="Calorie")
        ever = cols[3].selectbox("",("1","100"), index = None, placeholder = "Ogni")
        un = cols[4].selectbox("",("g","fetta","cucc","cucc.no","unità"), index = None, placeholder = "Unità")            
        #save_fd = form_dtb.form_submit_button("Aggiungi al Database", on_click = add_to_dtb, args = (df,fd_dtb,ingr,colr,calr,ever,un,core[usr_msk]['lang'][0],form_dtb))
        save_fd = form_dtb.form_submit_button("Aggiungi al Database")
    if lan=='esp' or lan=='Esp':
        ingr = cols[0].text_input("",placeholder="Nuevo Ingrediente")
        colr = cols[1].selectbox("",("Rojas","Amarillas","Verdes"), index = None, placeholder = "Colòr")
        calr = cols[2].text_input("",placeholder="Calorias")
        ever = cols[3].selectbox("",("1","100"), index = None, placeholder = "Cada")
        un = cols[4].selectbox("",("g","rebanada","cuch","cuch.ita","unidad"), index = None, placeholder = "Unidad")
        #save_fd = form_dtb.form_submit_button("Agregar al Database", on_click = add_to_dtb, args = (df,fd_dtb,ingr,colr,calr,ever,un,core[usr_msk]['lang'][0],form_dtb))
        save_fd = form_dtb.form_submit_button("Agregar al Database")

    if ingr in fd_dtb:
        i += 1
        update_dtb(df,fd_dtb,ingr,colr,calr,ever,un,lan,form_dtb)
        df = load_data(i)

    if ingr not in fd_dtb:
        i += 1
        add_to_dtb(df,fd_dtb,ingr,colr,calr,ever,un,lan,form_dtb)
        df = load_data(i)
        fd_dtb = np.append(fd_dtb,ingr)

    return(df,fd_dtb,i)



if "usr" in st.session_state and st.session_state.usr != 'new' and  st.session_state.usr != None:
    usr = st.session_state.usr
    usr_msk = (core['user'] == usr)
    df,fd_dtb,st.session_state.i = dtb(df,core[usr_msk]['lang'][0],st.session_state.i)
else:
    df,fd_dtb,st.session_state.i = dtb(df,"Eng",st.session_state.i)

 






