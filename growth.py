import os
import streamlit as st

st.set_page_config(page_title="SweepMaster", layout="wide")

st.write("Installing dependencies... Please wait ⏳")
os.system("pip install --upgrade pip")  # ✅ Upgrade pip to avoid issues
os.system("pip install openpyxl")  # ✅ Force install openpyxl before execution

import pandas as pd
from io import BytesIO

if importlib.util.find_spec("openpyxl") is not None:
    st.success("✅ openpyxl is installed!")
else:
    st.error("❌ openpyxl is NOT installed! 🚨")
    
# ✅ Install dependencies before running the app
st.write("Installing dependencies... Please wait ⏳")
os.system("pip install openpyxl")

#custom css
st.markdown(
    """
      <style>
        .stApp{
            background-color: #ffffff;
            color: black;
        }   
      </style>
    """,
    unsafe_allow_html=True   
)
#title and description
st.title("SweepMaster: Level Up Your Insights!")
st.write("Transform your file between CSV and Excel formats with built-in data cleaning and visualization")

#files upload
uploaded_files=st.file_uploader("Upload your files (accepts CSV or Excel format):",type=["csv", "xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext=os.path.splitext(file.name)[-1].lower()  #file extension  or full file nname ko display kareiga in lower case

        if file_ext==".csv":
            df=pd.read_csv(file)   #agr file extension csv hogi tou yeh csv me format me uploaded file ko read kareiga 
        elif file_ext==".xlsx":
            df=pd.read_excel(file, engine="openpyxl")    
        else:
            st.error(f"unspported file type: {file_ext}") 
            continue 
        
         #file_details
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())

        #dat cleaning option
        st.subheader("Data Cleaning Option")
        if st.checkbox(f"clean data for {file.name}"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from the file: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicate Removed!")

            with col2:
                if st.button(f"Fill missing values for: {file.name}"):      
                    numeric_cols =df.select_dtypes(include=['number']).columns
                    df[numeric_cols]= df[numeric_cols].fillna(df[numeric_cols].mean())   #fillna method non availiable data ko stor krta hai 
                    st.write("Missing values have been filled")

        st.subheader("Select Columns To Keep")
        columns=st.multiselect(f"Choose Columns for {file.name}",df.columns, default=df.columns)
        df=df[columns]


        #data visualisation
        st.subheader("Data Visualisation")
        if st.checkbox(f"Show Data Visualisation for file{file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])
        
        #conversion option
        st.subheader("Conversion Options")
        conversion_type=st.radio (f"Convert {file.name} to:", ["CSV", "EXCEL"], key=file.name )
        if st.button(f"Convert {file.name}"):
            buffer=BytesIO()
            if conversion_type=="CSV":
                df.to_csv(buffer,index=False)
                file.name=file.name.replace(file_ext,".csv")
                mime_type="text/csv"

            elif conversion_type=="EXCEL":
                df.to_excel(buffer,index=False)
                file_name=file.name.replace(file_ext,".xlsx")
                mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)    
            
            st.download_button(
                label=(f"Download {file.name} as {conversion_type}"),
                data=buffer,
                file_name= file_name,
                mime=mime_type
            )
st.success("All Files Processed Successfully")

 
