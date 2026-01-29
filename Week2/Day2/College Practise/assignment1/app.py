import streamlit as st
import db 

database = db.database()
database.connectDb()

st.title("Register")

with st.form("register" , clear_on_submit=True):
    name = st.text_input("Enter your Name")
    password = st.text_input("Enter your Password")
    submitReg = st.form_submit_button("submit")
    
if submitReg:
    data = [name, password]
    database.register(data=data)
    st.success("Registered the user")
    st.balloons()
elif name == "" or password == "":
    st.warning("Name or password can't be empty ")
else:
    st.error("Somthing went wrong")

st.title("Login")

with st.form("login" , clear_on_submit=True):
    id = st.number_input("Enter your Id")
    password = st.text_input("Enter your Password")
    submitLog = st.form_submit_button("submit")
    
if submitLog:
    data = [id , password]
    user = database.login(data=data)
    if user:
        st.success("Logged In")
        st.balloons()
    else:
        st.error("Try again")

