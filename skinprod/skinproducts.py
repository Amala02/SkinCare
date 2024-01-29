import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
data_skin_orig=pd.read_csv('skinprod\\ingreds.csv')
data_skin=pd.read_csv('skinprod\\cosmetics_clean.csv')
Names=[]
Labels=[]
for index,row in data_skin.iterrows():
  Names.append(index)
  if(row['Label']=='Moisturizer'):
    Labels.append(0)
  if(row['Label']=='Cleanser'):
    Labels.append(1)
  if(row['Label']=='Treatment'):
    Labels.append(2)
  if(row['Label']=='Face Mask'):
    Labels.append(3)
  if(row['Label']=='Eye cream'):
    Labels.append(4)
  if(row['Label']=='Sun protect'):
    Labels.append(5)
Names_orig=data_skin['Name']
data_skin['Label']=Labels
data_skin['Name']=Names
model = DecisionTreeClassifier()
model.fit(data_skin.drop('Name', axis=1), data_skin['Name'])

st.title("Skincare Questionnaire")

st.header("1. Select your most apt skin type:")
skintype=st.radio("", ['Oily', 'Combination', 'Dry', 'Normal'])

st.header("2. Is your skin sensitive?")
Sensitivity = st.checkbox("Yes", key="sens")

st.header("3.Do you struggle frequently with dark circles? If yes, stretch the skin under your eyes and observe")
darkcircle=st.radio("Does it:", ["Darkness move on stretching?",  "Not move at all?", "No dark circles"])

st.header("4.Do you have wrinkles or wrinkly skin?")
wrinkles=st.checkbox("Yes", key="wrinkle")

st.header("5.How often do you get acne or pimples at a time?")
acne=st.radio("",['frequently', 'very rarely'])


st.header("6.Select Skincare Product Type(s):")
Moisturizer = st.checkbox("Moisturizer", key="mois")
Cleanser= st.checkbox("Cleanser", key="clean")
Treatment= st.checkbox("Treatment", key="treat")
Mask=st.checkbox("Face mask", key="mask")
Sun=st.checkbox("Sunscreen", key="sun")
Eye=st.checkbox("Eye cream", key="eye")

if st.button("Submit"):
    if(skintype=='Oily'):
        Combination=0
        Dry=0
        Normal=0
        Oily=1
    if(skintype=='Normal'):
        Combination=0
        Dry=0
        Normal=1
        Oily=0
    if(skintype=='Dry'):
        Combination=0
        Dry=1
        Normal=0
        Oily=0
    if(skintype=='Combination'):
        Combination=1
        Dry=0
        Normal=0
        Oily=0

    if(Sensitivity):
        Sensitivty=1
    else:
        Sensitivity=0

    products=['Moisturizer', 'Cleanser', 'Treatment', 'Mask', 'Eyecream', 'Sunscreen']
    selected_products=[]
    if Moisturizer:
        selected_products.append(0)
    if Cleanser:
        selected_products.append(1)
    if Treatment:
        selected_products.append(2)
    if Mask:
        selected_products.append(3)
    if Eye:
        selected_products.append(4)
    if Sun:
        selected_products.append(5)
  

    Suggestions=[]
    if(darkcircle=="Darkness move on stretching?"):
      for index,row in data_skin_orig.iterrows():
        if(row['Label']==4)and('Hyaluronic' in row['Ingredients'])and('Retinol' in row['Ingredients'])and(row['Name']!='#NAME?'):
          st.write("You may have vascular dark circles, try:", row['Name'])
    if(darkcircle=="Not move at all?"):
      for index,row in data_skin_orig.iterrows():
        if(row['Label']==4)and('vitamin c' in row['Ingredients'].lower())and(row['Name']!='#NAME?'):
          st.write("You may have pigmented dark circles, try:", row['Name'])

    
    if wrinkles:
      st.write("For treating wrinkles, you might want to try:")
    for index,row in data_skin_orig.iterrows():
      
      if(Combination==1):
        if wrinkles:
          if('wrinkle' in row['Name'])and (row['Combination']==1):
            st.write(row['Name'])
      if(Normal==1):
        if wrinkles:
          if('wrinkle' in row['Name'])and (row['Normal']==1):
            st.write(row['Name'])
      if(Dry==1):
        if wrinkles:
          if('wrinkle' in row['Name'])and (row['Dry']==1):
            st.write(row['Name'])
      if(Oily==1):
        if wrinkles:
          if('wrinkle' in row['Name'])and (row['Oily']==1):
            st.write(row['Name'])

      
    for i in range(len(selected_products)):
        user_input = pd.DataFrame({
        'Label': [selected_products[i]],
        'Combination': [Combination],
        'Dry': [Dry],
        'Normal': [Normal],
        'Oily': [Oily],
        'Sensitive': [Sensitivity] })
        predicted_product = model.predict(user_input)
        Suggestions.append(products[selected_products[i]]+":"+Names_orig[predicted_product[0]])
    #Suggestions=set(Suggestions)
    #Suggestions=list(Suggestions)
    for i in Suggestions:
      st.write(i)
