import streamlit as st
import pandas as pd

# Header 

st.header("Student Records")

# Title

st.title("Students DB")

# SubHeader : This acts like a sub-heading

st.subheader("This is a Sub header")

# Text : This is to show a simple text in the ui

st.text("This is a simple text")

# Hr : This is a horizontal line

st.markdown("---")

# Write : This acts like text but allows python var to write code style to ui 


st.write([1,2,3,4,5])

# Write vs text

b = [6,7,8,9]
st.text(b)

# Display formats for Markdown : ### , ** ** , * * , - 

st.markdown("### Heading")
st.markdown("- List1 \n - List2")

st.markdown("<h1 stlye='color:red'> This is using HTML </h1>" , unsafe_allow_html=True)

# Code : It helps in showing the code in the ui 

st.code("""
        def add(a,b):
            return a + b
    """ , language="python")

# latex : This is used for displaying the mathmatical equations

st.latex(r"""
        a^2 + b^2 + 2ab = (a + b) ^ 2      
    """)

# divider : It is used to divide two sections in the ui

st.divider()

# Button : its a button 


if st.button("show"): 
    st.write("Here!")
    st.balloons()
else: 
    st.write("There!")

# Text input : This is to take input from the user

# num = st.number_input("Enter your num between 1 : " , placeholder=0)

# if num > 10 and num < 0:
#     st.error("Input Invalid")
# else :
#     st.success(f"Your number: {num}")

# Checkbox : its a checkbox

if st.checkbox("agree to my conditions !"):
    st.write("GOOD")

# Radio : only one option can be selected at a time 

option = st.radio("select the status: " , ("TO DO" , "In Progress ", "Completed"))
st.write(option)

# Slider 

st.slider("select your age " , 0,10)

# Select : its like a drop down list and it also have a multiselect variation 

country = st.selectbox("Select your country : ", ("India" , "Japan"))
st.write(country)

skills = st.multiselect(
    "Select your skills ", ("Python" , "CPP" , "Svelte" , "FireBase")
)

st.write(skills)

# upload_file 

uploadFile = st.file_uploader("Chooes file")
if uploadFile is not None :
    st.success("File uploaded")


st.divider()

# Form's in Streamlit

idx = 10
with st.form("myForm"):
    name = st.text_input("Enter your Name")
    age = st.number_input("Enter your name")
    submit = st.form_submit_button("Submit")

if submit: 
    st.write(name , age)    

st.subheader("Loging")

st.divider()

with st.form("login"):
    name = st.text_input("Enter your Name")
    password = st.text_input("Enter your Password")
    submit = st.form_submit_button("Submit")

if submit:
    st.success("login success")
    
# Columns

col1 , col2 , col3 = st.columns(3)

with col1: 
    st.header("This is col1")
with col2: 
    st.header("This is col2")
with col3: 
    st.header("This is col3")

st.divider()

# Container 
cont = st.container()
cont.write("This is a container")
cont.button("cont")

st.divider()

# Table

data = pd.DataFrame({
    "col1":[1,2,3],
    "col2":[4,5,6],
    "col3":[8,9,0]
})
st.table(data=data)

st.divider()

# Side Bar

st.sidebar.title("This is a Side bar ")
option = st.sidebar.selectbox("select page" , ["page1" , "page2" , "page3"])
st.write(f"current page {option}")

# @st.cache_data
# class load_data:
#     def userData(self):
#         return "User"
    
    
# data = load_data()
# st.write(data)
