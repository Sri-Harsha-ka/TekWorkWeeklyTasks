import streamlit as st 
from db import database
import pandas as pd

st.markdown("---")
st.title("-------------TODO App-------------")
task = st.text_input("Enter Task")
status = st.radio("Select Status : " , ["ToDo", "In Progress" , "Completed"])

data = [task , status]

db = database()
db.connectDb()

if st.button("submit"):
    db.createRows(data=data)
    st.success("Added the Task")

st.subheader("-------------Tasks-------------")
records = db.readRows()

# df = pd.DataFrame(records, columns=["Id", "Task", "Status"])
# st.dataframe(df)

idx1 = 1
idx2 = -1
for r in records:
    c1,c2,c3 = st.columns(3)
    
    c1.write(r)
    if c2.button("delete" , key=idx1):
        db.deleteRows(r[0])
    
    if f"show_{idx1}" not in st.session_state:
        st.session_state[f"show_{idx1}"] = False

    if c3.button("update", key=idx2):
        st.session_state[f"show_{idx1}"] = True

    if st.session_state[f"show_{idx1}"]:
        task = st.text_input("Enter Task", key=idx1*100)
        status = st.radio(
            "Select Status",
            ["ToDo", "In Progress", "Completed"],
            key=idx2*100
        )

        if st.button("confirm update", key=idx1*1000):
            data = [r[0], task, status]
            db.updateRows(data=data)
            st.session_state[f"show_{idx1}"] = False

    idx1 += 1
    idx2 -= 1