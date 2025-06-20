import streamlit as st
import pickle
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
import tensorflow as tf
import pandas as pd
import numpy as np
import pickle


with open('label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)

with open('one_hot_encoder.pkl', 'rb') as file:
    one_hot_encoder = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

model = tf.keras.models.load_model('model.h5')

## Title
st.title('Customer Churn Prediction')


## User Input
geography = st.selectbox('Geography', one_hot_encoder.categories_[0])
gender = st.selectbox('Gender', label_encoder.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has credit card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

input_data = {
    'CreditScore': credit_score,
    'Gender': label_encoder.transform([gender])[0],
    'Age': age,
    'Tenure': tenure,
    'Balance': balance,
    'NumOfProducts': num_of_products,
    'HasCrCard': has_cr_card,
    'IsActiveMember': is_active_member,
    'EstimatedSalary': estimated_salary
}



geo_encoded = one_hot_encoder.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=one_hot_encoder.get_feature_names_out(['Geography']))

input_data_df = pd.DataFrame([input_data])


input_data_df = pd.concat([input_data_df.reset_index(drop=True), geo_encoded_df], axis=1)
print(input_data_df)

scaled_df = scaler.transform(input_data_df)

result = model.predict(scaled_df)

predicton_prob = result[0][0]

st.write(f'Prediction Probability : {predicton_prob : .2f}')

if predicton_prob < 0.5:
    st.write('Customer will not leave the bank')
else:
    st.write('Customer will leave the bank')
