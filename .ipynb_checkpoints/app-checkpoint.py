import streamlit as st
from st_aggrid import AgGrid
import plotly.express as px
import pickle
import  pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from pivottablejs import pivot_ui
from scipy import stats


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
<h2 style="color:white;">Data Science App</h2>
</div>
"""
   # footer{
   #          visibility: hidden;
   #      }
        
hide_menu = """
    <style>
        #MainMenu{
            visibility: hidden;
        } 
    </style>
"""

my_footer = """
    <style>
        content:'Copyright @ 2022: Davila Rostaing';
        display:block;
        position:relative;
        color:tomato;
        padding:5px;
        top:3px;
      
    </style>
"""
st.markdown(html_temp, unsafe_allow_html=True)
    
model = pickle.load(open('C:/Users/Rostaing/Desktop/Data Science/DataScienceProjects/head_disease.sav', 'rb'))



@st.cache
def load_data():
    df = pd.read_csv("heart_Disease.csv")
    df["sex"].replace( [0, 1], ["Male", "Female"], inplace=True)
    return df

df = load_data()

def eda():
    
    st.write("***Exploratory Data Analysis (EDA)***")
    sb = st.selectbox("", ["shape", "types", "dimension", "size", "count", "describe", "null values", "Statistique inférentielle"])
    
    if sb == "shape":
        st.write(f"{sb}:", df.shape)
        
    elif sb == "types":
        st.write(df.dtypes)
        
    elif sb == "dimension":
        st.write(f"{sb}:", df.ndim)
        
    elif sb == "size":
        st.write(f"{sb}:", df.size)
        
    elif sb == "count":
        st.write(df.count())
        
    elif sb == "describe":
        st.write(df.describe())
        
    elif sb == "null values":
        st.write(df.isnull().sum())
        
    # elif sb == "pearson test":
    #     statistics, p_value = stats.pearsonr(df["age"], df["target"])
    #     st.write("Test (age vs target)")
    #     st.success(f"statistics = {statistics} and p-value = {p_value}")
        
    # elif sb == "Statistique inférentielle":
    #     numeric_cols = df.select_dtypes(exclude=['object'])
    #     var_x = st.selectbox("X variable", numeric_cols)
    #     var_y = st.selectbox("Y variable", numeric_cols)
    #     tset, p_value = stats.pearsonr(var_x, var_y)
    #     # st.write("Statistique =""{tset} P-value = {p_value}")
    #     if p_value < 0.05:
    #         st.warning("We are rejecting null hypothesis.")
    #     else:
    #         st.success("We are accepting null hypothesis.")
        


def visual():
    
    v = st.selectbox("Chooce your plot", ("Bar", "Correlation", "Histogram", "Violin", "Density", "Heatmaps", "Scatter", "Area", "Funnel", "Pie", "Box", "Ecdf"))
    
    if v == "Bar":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X variable", numeric_cols)
        var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.bar(df, x=var_x, y=var_y, color=var_color)
        st.plotly_chart(fig)
        
    elif v == "Correlation":
        fig = plt.figure(figsize=(22, 9))
        sns.heatmap(df.corr(), annot=True) 
        st.pyplot(fig)
        
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
        var_x = st.selectbox("X variable", numeric_cols)
        var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.violin(df, x=var_x, y=var_y, color=var_color, box=True, points="all", hover_data=df.columns)
        plt.xlabel(var_x)
        plt.ylabel(var_y)
        st.plotly_chart(fig)
    
    elif v == "Density":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X variable", numeric_cols)
        var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.density_contour(df, x=var_x, y=var_y)
        plt.xlabel(var_x)
        plt.ylabel(var_y)
        st.plotly_chart(fig)
        
    elif v == "Heatmaps":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X variable", numeric_cols)
        var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.density_heatmap(df, x=var_x, y=var_y, marginal_x="rug", marginal_y="histogram")
        plt.xlabel(var_x)
        plt.ylabel(var_y)
        st.plotly_chart(fig)
        
#     elif v == "3D":
#         numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
#         categories = df.select_dtypes(include=['object']).columns.to_list()
#         var_x = st.selectbox("X variable", numeric_cols)
#         var_y = st.selectbox("Y variable", numeric_cols)
#         var_color = st.selectbox("Marker", categories)
#         fig = px.scatter_3d(df, x=var_x, y=var_y, z=var_y, color=var_color, size=df, hover_name=var_color,
#                   symbol="result", color_discrete_map = {"Joly": "blue", "Bergeron": "green", "Coderre":"red"})
#         plt.xlabel(var_x)
#         plt.ylabel(var_y)
#         st.plotly_chart(fig)
        
        

        
    elif v == "Scatter":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X variable", numeric_cols)
        var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.scatter(data_frame=df, x=var_x, y=var_y, color=var_color, size_max=60,         hover_name=var_color)
        st.plotly_chart(fig)
        
    elif v == "Area":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X variable", numeric_cols)
        var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.area(df, x=var_x, y=var_y, color=var_color, line_group=var_color)
        st.plotly_chart(fig)
        
    elif v == "Funnel":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X variable", numeric_cols)
        var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.funnel(df, x=var_x, y=var_y, color=var_color)
        st.plotly_chart(fig)
        
    elif v == "Pie":
        numeric_cols = df.select_dtypes(exclude=['object']).columns.to_list()
        categories = df.select_dtypes(include=['object']).columns.to_list()
        var_x = st.selectbox("X variable", numeric_cols)
        var_y = st.selectbox("Y variable", numeric_cols)
        var_color = st.selectbox("Marker", categories)
        fig = px.pie(df, values=var_x, names=var_color, color=var_color)
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
        age = int(st.number_input('Age'))
        
    with col2:
        sex = int(st.number_input('Sex'))
        
    with col3:
        cp = int(st.number_input('Chest Pain types'))
        
    with col1:
        trestbps = int(st.number_input('Resting Blood Pressure'))
        
    with col2:
        chol = int(st.number_input('Serum Cholestoral in mg/dl'))
        
    with col3:
        fbs = int(st.number_input('Fasting Blood Sugar > 120 mg/dl'))
        
    with col1:
        restecg = int(st.number_input('Resting Electrocardiographic results'))
        
    with col2:
        thalach = int(st.number_input('Maximum Heart Rate achieved'))
        
    with col3:
        exang = int(st.number_input('Exercise Induced Angina'))
        
    with col1:
        oldpeak = float(st.number_input('ST depression induced by exercise'))
        
    with col2:
        slope = int(st.number_input('Slope of the peak exercise ST segment'))
        
    with col3:
        ca = int(st.number_input('Major vessels colored by flourosopy'))
        
    with col1:
        thal = int(st.number_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect'))
    
    if st.button('Heart Disease Test Result'):
        heart_prediction = model.predict([[age, sex, cp, trestbps, chol, fbs,      restecg,thalach,exang,oldpeak,slope,ca,thal]])                          
        
        if (heart_prediction[0] == 1):
            heart_diagnosis = 'The person is having heart disease'
            st.warning(heart_diagnosis)
        else:
            heart_diagnosis = 'The person does not have any heart disease'
            st.success(heart_diagnosis)
        
        

def main():
    st.markdown(hide_menu, unsafe_allow_html=True)
    if selected == "DATASET":
        st.write("***Dataset***")
        # AgGrid(df)
        # pivot_ui(df)
        st.dataframe(data=df)
    elif selected == "EDA":
        eda()
    elif selected == "VISUALIZATION":
        st.write("***Visualization***")
        visual()
    elif selected == "PREDICTION":
        st.write("***Prediction system***")
        pred()
    st.markdown(my_footer, unsafe_allow_html=True)
if __name__ == "__main__":
    main()