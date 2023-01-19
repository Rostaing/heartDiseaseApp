import streamlit as st
from st_aggrid import AgGrid
import plotly.express as px
import pickle
import  pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
# from pivottablejs import pivot_ui
from scipy import stats
import datetime
import time
from streamlit_disqus import st_disqus
# import neattext.functions as nfx

st.set_page_config(page_title="heart disease - app", page_icon="📍") # , layout="wide"

# st.snow()
# st.markdown(
#     """
#     <style>
#     .small-font {
#         font-size:12px;
#         font-style: italic;
#         color: #b1a7a6;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


with st.sidebar:
    
    selected = option_menu(
        "MENU",
        ["HOME", "DATASET", "EDA", "VISUALIZATION", "PREDICTION"],
        icons=["house", "graph-up-arrow", "book", "bar-chart-line", "calendar2-check"],
        menu_icon = "cast",
        default_index=0
    )

html_temp = """
    <div style="background-color:tomato;padding:15px;text-align:center;">
    <h2 style="color:white;">Heart Disease App</h2>
    </div>
"""

st.markdown(html_temp, unsafe_allow_html=True)
        
hide_menu = """
    <style>
        #MainMenu{
            visibility: hidden;
        }
        
        
        footer{
            visibility: hidden;
         }
         
         header{
             visibility: visible;
         }
        
        {
            display:block;
            position:relative;
            color:tomato;
            padding:5px;
            top:3px;
            background-color:tomato;
            text-align:center;
            content:'Copyright @ 2022: Davila Rostaing';
        } 
    </style>
"""

# password_guess = st.text_input('What is the Password?') 

# if password_guess != 'streamlit_is_great': 
#   st.stop()

    
model = pickle.load(open('C:/Users/Rostaing/Desktop/Data Science/DataScienceProjects/head_disease.sav', 'rb'))



@st.cache
def load_data():
    df = pd.read_csv("heart_Disease.csv")
    df["sex"].replace( [0, 1], ["Male", "Female"], inplace=True)
    return df

df = load_data()

def eda():
    
    st.write("***Exploratory Data Analysis (EDA)***")
    sb = st.selectbox("", ["shape", "types", "dimension", "size", "significant_correlation", "describe", "null values", "Hypothesis"])
    
    if sb == "shape":
        st.write(f"{sb}:", df.shape)
        
    elif sb == "types":
        st.write(df.dtypes)
        
    elif sb == "dimension":
        st.write(f"{sb}:", df.ndim)
        
    elif sb == "size":
        st.write(f"{sb}:", df.size)
        
    elif sb == "significant_correlation":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        var_y = st.selectbox("Y axis", numeric_cols)
        pearson_coef, p_value = stats.pearsonr(df[var_x], df[var_y])
        st.write(f"The Pearson Correlation Coefficient is {pearson_coef}, with P-value = {p_value}")
        if p_value < 0.001:
            st.success("There is strong evidence that the correlation is significant.")
            st.balloons()
        elif p_value < 0.05:
            st.info("There is moderate evidence that the correlation is significant.")
        elif p_value < 0.1:
            st.warning("There is weak evidence that the correlation is significant.")
        elif p_value >  0.1:
            st.error("There is no evidence that the correlation is significant.")
        
    elif sb == "describe":
        st.write(df.describe())
        
    elif sb == "null values":
        st.write(df.isnull().sum())
        
    elif sb == "Hypothesis":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        var_y = st.selectbox("Y axis", numeric_cols)
        tset, p_value = stats.pearsonr(df[var_x], df[var_y])
        st.write(f"Statistique = {tset} P-value = {p_value}")
        if p_value < 0.05:
            st.warning("We are rejecting null hypothesis.")
        else:
            st.success("We are accepting null hypothesis.")
        
def visual():
    
    v = st.selectbox("Chart Type", ("Bar", "Correlation", "Line", "Histogram", "Violin", "Density", "Heatmaps", "Scatter", "Area", "Funnel", "Pie", "Box", "Ecdf"))
    
    if v == "Bar":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        var_y = st.selectbox("Y axis", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.bar(df, x=var_x, y=var_y, color=var_color)
        st.plotly_chart(fig)
        
    elif v == "Correlation":
        fig = plt.figure(figsize=(22, 9))
        sns.heatmap(df.corr(), annot=True) 
        st.pyplot(fig)
        
    elif v == "Line":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.line(df, x=var_x, color=var_color)
        st.plotly_chart(fig)
        
    elif v == "Histogram":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X variable", numeric_cols)
        var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.histogram(df, x=var_x, y=var_y, color=var_color, marginal="rug", hover_data=df.columns)
        plt.xlabel(var_x)
        plt.ylabel(var_y)
        st.plotly_chart(fig)
        
    elif v == "Violin":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        var_y = st.selectbox("Y axis", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.violin(df, x=var_x, y=var_y, color=var_color, box=True, points="all", hover_data=df.columns)
        plt.xlabel(var_x)
        plt.ylabel(var_y)
        st.plotly_chart(fig)
    
    elif v == "Density":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        var_y = st.selectbox("Y axis", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.density_contour(df, x=var_x, y=var_y)
        plt.xlabel(var_x)
        plt.ylabel(var_y)
        st.plotly_chart(fig)
        
    elif v == "Heatmaps":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        var_y = st.selectbox("Y axis", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.density_heatmap(df, x=var_x, y=var_y, marginal_x="rug", marginal_y="histogram")
        plt.xlabel(var_x)
        plt.ylabel(var_y)
        st.plotly_chart(fig)
        
                
    elif v == "Scatter":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        var_y = st.selectbox("Y axis", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.scatter(data_frame=df, x=var_x, y=var_y, color=var_color, size_max=60) # size=df.size, animation_frame=df.size,
        st.plotly_chart(fig)
        
    elif v == "Area":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        var_y = st.selectbox("Y axis", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.area(df, x=var_x, y=var_y, color=var_color, line_group=var_color)
        st.plotly_chart(fig)
        
    elif v == "Funnel":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        var_y = st.selectbox("Y axis", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.funnel(df, x=var_x, y=var_y, color=var_color)
        st.plotly_chart(fig)
        
    elif v == "Pie":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X axis", numeric_cols)
        # var_y = st.selectbox("Y axis", numeric_cols)
        # var_color = st.selectbox("Marker", categories)
        fig = px.pie(values=df[var_x].value_counts(), names=df[var_x].value_counts().index)
        st.plotly_chart(fig)
        
    elif v == "Box":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X variable", numeric_cols)
        # var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.box(df, x=var_x, color=var_color, notched=True)
        st.plotly_chart(fig)
    
    elif v == "Ecdf":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X variable", numeric_cols)
        # var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.ecdf(df, x=var_x, color=var_color)
        st.plotly_chart(fig)
        
def pred():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = int(st.number_input('Age', min_value=0, max_value=100)) # ,step=1, format="%i"
        
    with col2:
        sex = int(st.number_input('Sex (0=male, 1=female)', min_value=0, max_value=1))
        
    with col3:
        cp = int(st.number_input('Chest Pain types', min_value=0, max_value=3))
        
    with col1:
        trestbps = int(st.number_input('Resting Blood Pressure > 120 mg/dl', min_value=120))
        
    with col2:
        chol = int(st.number_input('Serum Cholestoral in mg/dl', min_value=0))
        
    with col3:
        fbs = int(st.number_input('Fasting Blood Sugar', min_value=0, max_value=1))
        
    with col1:
        restecg = int(st.number_input('Resting Electrocardiographic results', min_value=0, max_value=1))
        
    with col2:
        thalach = int(st.number_input('Maximum Heart Rate achieved', min_value=0))
        
    with col3:
        exang = int(st.number_input('Exercise Induced Angina', min_value=0, max_value=1))
        
    with col1:
        oldpeak = float(st.number_input('ST depression induced by exercise', min_value=0.0, max_value=3.))
        
    with col2:
        slope = int(st.number_input('Slope of the peak exercise ST segment', min_value=0, max_value=2))
        
    with col3:
        ca = int(st.number_input('Major vessels colored by flourosopy', min_value=0, max_value=4))
        
    with col1:
        thal = int(st.number_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect', min_value=0, max_value=2))
    
    if st.button('Heart Disease Test Result'):
        heart_prediction = model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])                          
        
        if (heart_prediction[0] == 1):
            with st.spinner("In progress..."):
                time.sleep(5)
                heart_diagnosis = 'The person is having heart disease'
                st.warning(heart_diagnosis)
        else:
             with st.spinner("In progress..."):
                time.sleep(5)
                heart_diagnosis = 'The person does not have any heart disease'
                st.success(heart_diagnosis)
                st.balloons()
        
        

def main():
    # st.camera_input("Take a picture")
    st.markdown(hide_menu, unsafe_allow_html=True)
    if selected == "MENU":
        st_disqus("steamlit-disqus-demo")
    elif selected == "DATASET":
        st.write("***Dataset***")
       # AgGrid(df)
        # pivot_ui(df)
        st.dataframe(data=df)
        # result = nfx.clean_text()
        
        tr = df.to_csv(index=False).encode('utf-8')
        st.download_button(label='Download data', data=tr, mime='text/csv', file_name='heaart_disease.csv')
        # st.mitosheet.sheet(df, analysis_to_replay="id-qiflyttyzf")
    elif selected == "EDA":
        eda()
    elif selected == "VISUALIZATION":
        st.write("***Visualization***")
        visual()
    elif selected == "PREDICTION":
        st.write("***Prediction system***")
        pred()
        
        
if __name__ == "__main__":
    main()

ligne = """
    <div>
        <hr>
    </div>
"""
st.markdown(ligne, unsafe_allow_html = True)
st.markdown(
            """
            <p style="color:#fff;">This Data Science App was coded by Davila Rostaing, Data Scientist.<p/>
            """
            , unsafe_allow_html = True)