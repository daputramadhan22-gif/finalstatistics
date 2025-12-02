import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
from collections import Counter

st.title("🧮 Descriptive Statistics Analysis")

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data preview:", df.head())
    
    col = st.selectbox("Select column for analysis:", df.columns)
    
    if pd.api.types.is_numeric_dtype(df[col]):
        data = df[col].dropna()
        st.header("📊 Numeric Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mean", f"{data.mean():.2f}")
        col2.metric("Median", f"{data.median():.2f}")
        col3.metric("Std Dev", f"{data.std():.2f}")
        col4.metric("Mode", f"{stats.mode(data, keepdims=True)[0][0]:.2f}")
        
        col5, col6 = st.columns(2)
        col5.metric("Minimum", f"{data.min():.2f}")
        col6.metric("Maximum", f"{data.max():.2f}")
        
        stats_df = pd.DataFrame({
            'Statistic': ['Mean', 'Median', 'Mode', 'Min', 'Max', 'Std'],
            'Value': [data.mean(), data.median(), stats.mode(data, keepdims=True)[0][0],
                     data.min(), data.max(), data.std()]
        })
        st.table(stats_df)
        
        viz = st.selectbox("Choose visualization:", ["Histogram", "Boxplot", "Both"])
        if viz in ["Histogram", "Both"]:
            fig_hist = px.histogram(data, x=col, nbins=20, title=f"Histogram of {col}")
            st.plotly_chart(fig_hist)
        if viz in ["Boxplot", "Both"]:
            fig_box = px.box(data, y=col, title=f"Boxplot of {col}")
            st.plotly_chart(fig_box)
    else:
        data = df[col].dropna()
        st.header("📈 Categorical Statistics")
        
        freq = Counter(data)
        freq_df = pd.DataFrame.from_dict(freq, orient='index', columns=['Frequency']).sort_values('Frequency', ascending=False)
        freq_df['Percentage'] = (freq_df['Frequency'] / len(data) * 100).round(2)
        st.table(freq_df)
        
        fig_pie = px.pie(values=freq.values(), names=freq.keys(), title=f"Distribution of {col}")
        st.plotly_chart(fig_pie)
