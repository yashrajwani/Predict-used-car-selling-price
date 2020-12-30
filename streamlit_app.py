import streamlit as st

st.title("Predict Selling Price for Used Cars")
txt = st.text("Loading Model...")

from tensorflow import keras
import numpy as np
from sklearn.preprocessing import MinMaxScaler
model = keras.models.load_model('MLP_v1')

def one_hot(encoding_scheme, item):
    assert item in encoding_scheme
    res = [0]*len(encoding_scheme)
    res[encoding_scheme.index(item)] = 1
    return res

def inv_transform(y_pred):
    """
    Inverse transform MinMax Scaling to get meaningful output
    Parameters from .ipynb

    """
    data_min = 3e4
    data_max = 1e7
    return y_pred*(data_max-data_min)+data_min

def transform(x):
    data_min, data_max = (np.array([1.994e+03, 1.000e+00, 0.000e+00, 6.240e+02, 3.280e+01, 2.000e+00,
                                    0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,
                                    0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,
                                    0.000e+00, 0.000e+00]),
                          np.array([2.020000e+03, 2.360457e+06, 4.200000e+01, 3.604000e+03,
                                    4.000000e+02, 1.400000e+01, 1.000000e+00, 1.000000e+00,
                                    1.000000e+00, 1.000000e+00, 1.000000e+00, 1.000000e+00,
                                    1.000000e+00, 1.000000e+00, 1.000000e+00, 1.000000e+00,
                                    1.000000e+00, 1.000000e+00, 1.000000e+00, 1.000000e+00]))
    return (x-data_min)/(data_max-data_min)

txt.text("")

fuel_scheme = ["CNG", "Diesel", "LPG", "Petrol"]
seller_scheme = ["Dealer", "Individual", "Trustmark Dealer"]
transmission_scheme = ["Auto", "Manual"]
ownership_scheme = ['First owner', 'Fourth and above owner', 'Second owner' , 'Test Drive car','Third owner']


year = st.number_input('Year Bought:', value=2010) 
km_driven = st.number_input('Km Driven:', value=10000) 
mileage = st.number_input('Mileage (in kmpl):', value=20) 
engine = st.number_input('Engine capacity (in CC):', value=900) 
max_power = st.number_input('Max Power (in bhp):', value=90) 
seats = st.number_input('Number of Seats:', value=5) 

fuel = st.radio('Fuel Type:', fuel_scheme)
seller_type = st.radio('Seller Type:', seller_scheme)
transmission = st.radio('Transmission Type:', transmission_scheme)
ownership = st.radio('Ownership Type:', ['First owner', 'Second owner', 'Third owner', 'Fourth and above owner', 'Test Drive car'])

button = st.button("Predict")
if button:
    data_row = [year, km_driven, mileage, engine, max_power, seats]+ \
                one_hot(fuel_scheme, fuel)+\
                one_hot(seller_scheme, seller_type)+\
                one_hot(transmission_scheme, transmission)+\
                one_hot(ownership_scheme, ownership)


    x = np.array(data_row).reshape(1,-1)
    x = transform(x)
    st.text(f"Predicted Selling Price is Rs {inv_transform(model.predict(x))[0][0]:.0f}.")
