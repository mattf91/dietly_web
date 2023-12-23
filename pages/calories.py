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



st.header("Calories, calories calories!!")

st.write("This page will show the remaining calories, you will have the possibility to log the workout session, it will show you the ingredients that you ate in any day, and you'll be able to modify them.")

"""
- This page will contain the LEFT, WO, MEAL and PAST functions.
- The LEFT part only consists in showing some data; for the WO part, I'll insert a NUMERIC INPUT.

- For the MEAL and PAST parts, you'll have a SELECT button to choose the date that you want to inspect (the default date will be "today"). You'll see what you ate that day, and you'll be able to modify it on the fly, with buttons.

- You'll have a CHARACTER INPUT to insert the new ingredients that you ate (that will appear immediately in the list of stuff that you ate that day), together with a series of conversion buttons for the units and stuff, and a NUMERIC INPUT for the ammount of ingredient that you ate.
- There will be a display connected to the database, that by default will show nothing. But if you don't remember the exact name of an ingredient, you can query it in the database. If that specific ingredient is not in the database yet, you can upload it, and you'll see the database updated on the fly.
"""


today = date.today()
today=today.strftime("%d_%m_%Y")

if "usr" in st.session_state and st.session_state.usr != 'new' and  st.session_state.usr != None:
    usr = st.session_state.usr
    
    core=np.load('core.npy',allow_pickle=True)
    users = core['user']
    users = np.append(users,'new')
    usr_msk = (core['user'] == usr)
    usr_days_msk = (days['user'] == usr)
    usr_weight_msk = (weight['user'] == usr)














    




