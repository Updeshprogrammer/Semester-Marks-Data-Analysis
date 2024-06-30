import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Custom CSS for background images
st.markdown("""
<style>
    body {
        background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
        background-size: cover;
    }
    [data-testid=stSidebar] {
        background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
        background-size: cover;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    st.header("Menu")
    option = st.selectbox("Choose a student", ("Updesh Kushwaha", "Shubham Kumawat", "Narendra Singh","Urvashi_Bhardwaj","Adit_Yadav"))

# Title
st.title(option)
st.header('Semester Marks Data Analysis')

# Load the data
file_path = f'{option.replace(" ", "_")}_Semester_Marks.xlsx'

# Check if the file exists
if not os.path.exists(file_path):
    st.error(f"File not found: {file_path}. Please check the file path.")
    st.stop()

try:
    df = pd.read_excel(file_path)
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# Ensure the 'Grade' columns are strings if they exist
for semester in ["1st_Sem", "2nd_Sem", "3rd_Sem"]:
    grade_column = f'Grade_{semester}'
    if grade_column in df.columns:
        df[grade_column] = df[grade_column].astype(str)

# Semester selection
semester = st.sidebar.selectbox("Select Semester", ["First Semester", "Second Semester", "Third Semester"])
subject_filter = st.sidebar.text_input("Filter subjects")

# Tabs for different visualizations
tabs = st.tabs(["Data", "Average Marks", "Grade Distribution", "Percentage Semester wise"])

with tabs[0]:
    st.subheader(f"{semester} Data")

    if semester == "First Semester":
        sem_data = df[
            ['Subject', 'Marks1_1st_Sem', 'Marks2_1st_Sem', 'Grade_1st_Sem', 'Credit_1st_Sem', 'Roll_number']].dropna()
    elif semester == "Second Semester":
        sem_data = df[
            ['Subject', 'Marks1_2nd_Sem', 'Marks2_2nd_Sem', 'Grade_2nd_Sem', 'Credit_2nd_Sem', 'Roll_number']].dropna()
    elif semester == "Third Semester":
        sem_data = df[
            ['Subject', 'Marks1_3rd_Sem', 'Marks2_3rd_Sem', 'Grade_3rd_Sem', 'Credit_3rd_Sem', 'Roll_number']].dropna()

    sem_data.columns = ['Subject', 'Marks1', 'Marks2', 'Grade', 'Credit', 'RollNumber']

    if subject_filter:
        sem_data = sem_data[sem_data['Subject'].str.contains(subject_filter, case=False, na=False)]

    st.write(sem_data)

    st.download_button(label="Download Data as CSV", data=sem_data.to_csv(index=False),
                       file_name=f"{option}_{semester}_Data.csv")

with tabs[1]:
    st.subheader("Average Marks")

    sem_data['Average Marks'] = (sem_data['Marks1'] + sem_data['Marks2']) / 2
    st.bar_chart(sem_data.set_index('Subject')['Average Marks'])

with tabs[2]:
    st.subheader("Grade Distribution")

    grade_counts = sem_data['Grade'].value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Count']
    fig = px.pie(grade_counts, values='Count', names='Grade', title=f'Grade Distribution {semester}')
    st.plotly_chart(fig)

with tabs[3]:
    # st.subheader("Percentage Semester wise")
    # Percentage
    a = sem_data['Marks1'].sum()
    b = sem_data['Marks2'].sum()
    total = a + b
    st.write(f"### Percentage:{total / 900 * 100}%")

    # Convert Grade to numeric for GPA calculation
    # sem_data['Grade'] = pd.to_numeric(sem_data['Grade'], errors='coerce')

    # if sem_data['Grade'].isnull().any():
    #     st.error("Grade column contains non-numeric values that could not be converted.")
    # else:
    #     total_credits = sem_data['Credit'].sum()
    #     weighted_grades = (sem_data['Credit'] * sem_data['Grade']).sum()
    #     cumulative_gpa = weighted_grades / total_credits
    #     st.write(f"### Cumulative GPA: {cumulative_gpa:.2f}")

        # Percentage calculation
        # total_marks = sem_data['Marks1'].sum() + sem_data['Marks2'].sum()
        # # st.write(f"### Percentage: {total_marks / (2 * total_credits * 100) * 100:.2f}%")
        # st.write(f"### Percentage: {total_marks / (900*100)}%")

