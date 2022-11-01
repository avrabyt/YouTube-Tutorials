import numpy as np
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
import os, random

st.set_page_config(layout="wide")

if 'random_file' not in st.session_state:
    st.session_state.random_file = "cat1.jpg"

st.title("Singular Value Decomposition of an Image")
uploaded_file = st.sidebar.file_uploader("", type=['jpg','png','jpeg','tiff','bmp'])

if uploaded_file is not None:
    st.sidebar.info("File uploaded : " + uploaded_file.name)
    image = Image.open(uploaded_file)

else:
    # This button doesnot exist when file upload exists
    # Try new examples from Image directory 
    # Updates session state variable random file 
    if st.sidebar.button("Try New Example Image!"):
        random_file = random.choice(os.listdir("Image"))
        st.session_state.random_file = random_file
    
    # Opens file from the session state variable
    st.sidebar.info("Example file : " + st.session_state.random_file)
    image = Image.open("Image/{}".format(st.session_state.random_file))
    
imggray = image.convert('LA')
# Convert into numpy matrix
img_mat = np.array(list(imggray.getdata(band=0)), float)
img_mat.shape = (imggray.size[1], imggray.size[0])
img_mat = np.matrix(img_mat)
st.sidebar.write(img_mat.shape) 
# Compute SVD
U, S, V = np.linalg.svd(img_mat)

# Draw a slider
n_dim = st.slider("SVD rank(n)",0, int(S.shape[0]/5),5)
re_img = np.matrix(U[:, :n_dim]) * np.diag(S[:n_dim]) * np.matrix(V[:n_dim, :])  
p = (n_dim * re_img.shape[0] + n_dim+ n_dim * re_img.shape[1])/(re_img.shape[0]*re_img.shape[1])
st.info("Compare to original image : " +str(round(p*100,2)) + "% (approx) as much as space used. ")

# Dump the figure
fig, ax = plt.subplots(1,2, figsize = (10,10))
plt.subplot(1,2,1)
title = "Original-GrayScaled"
plt.imshow(imggray)
plt.title(title)
plt.subplot(1,2,2)
title = "Rank = %s" % n_dim
plt.imshow(re_img, cmap="gray")
plt.title(title)
st.pyplot(fig)

    
# Resources 
# https://www.frankcleary.com/svdimage/

