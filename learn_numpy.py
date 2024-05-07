import streamlit as st
import numpy as np 

def learn_numpy():
    value = 1 + 2
    st.write(value)
    
    ### Numpy arrays
    my_list = [1, 2, 3]
    arr = np.array(my_list)
    st.write(arr)
    my_matrix = [[1,2,3], [4,5,6], [7,8,9]]
    st.write(my_matrix)
    st.write(np.array(my_matrix))
    values = np.arange(0,10)
    st.write(values)