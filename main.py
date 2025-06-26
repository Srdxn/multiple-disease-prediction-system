import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pickle
import time
import os

st.set_page_config(page_title="Multiple Disease Prediction", layout="wide", initial_sidebar_state="expanded")

# Hide Streamlit's default menu and footer using CSS
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container {padding-top: 0rem;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

def disease_prediction():
    #Loading the models
    diabetes_model = pickle.load(open('./Models/diabetes.sav', 'rb'))
    heart_disease_model = pickle.load(open('./Models/heart_disease_model.sav', 'rb'))
    parkinsons_model = pickle.load(open('./Models/parkinsons.sav', 'rb'))

    #sidebar for navigation
    st.markdown("""
    <style>
    @media only screen and (max-width: 768px) {
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        [data-testid="stSidebar"] > div:first-child {
            box-shadow: none;
        }
    }
    </style>
""", unsafe_allow_html=True)


    with st.sidebar:
        selected = option_menu('Diagnostic Menu', ['About the System',
                                             'Diabetes Detection',
                                            'Heart Disease Detection',
                                            'Parkinsons Detection',
                                            ],
                               icons=['person-lines-fill', 'droplet','heart','person'],
                               default_index=0,
                               styles={
                                   "nav-link-selected": {"color": "black"}
                               })
        st.markdown('<hr>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2: 
            if st.button("Doctor Directory"):
                st.session_state.page = "doctor_directory"
                st.session_state['Diabetesdiagnosis'] = None
                st.rerun()

    if selected == "About the System":
        st.markdown("<h1 style='text-align: center;'>Welcome to the Multiple Disease Prediction System</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.write("""
            Welcome to the **Multiple Disease Prediction System** — a smart and interactive platform designed to assist users in the early detection of critical health conditions. This system leverages machine learning models to provide instant, data-driven predictions for **Diabetes**, **Heart Disease**, and **Parkinson’s Disease** based on user-submitted medical information.

            Our goal is to make preliminary health assessments more accessible, especially for individuals who may not have immediate access to healthcare facilities. Users can simply input specific medical parameters into our easy-to-use interface, and the system provides a prediction result in real-time. Each prediction module is built using disease-specific models to ensure accuracy, relevance, and reliability.

            But we go beyond just predictions.

            The platform also features a built-in Doctor Directory, allowing users to instantly connect with the right medical specialists. Based on the disease selected, users can view curated lists of:

            • 🫀 **Cardiologists** for heart-related concerns

            • 🧠 **Neurologists** for neurological conditions like Parkinson’s

            • 🍬 **Diabetologists** for metabolic disorders such as diabetes

            This feature ensures that users not only gain awareness of potential risks but are also guided toward taking the next step in seeking proper medical care.

            Whether you're conducting a quick health check or exploring the potential of AI in healthcare, our platform offers a seamless and informative experience. It's ideal for general users, students, researchers, and health-tech enthusiasts alike.

            We are continuously working to improve and expand the system, with future plans including the addition of more diseases, support for multiple languages, and deeper integration with real-world healthcare services..""")
        
    
    
    elif selected == "Diabetes Detection":

        st.markdown("<h1 style='text-align: center;'>Diabetes Detection</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            Pregnancies = st.text_input("Number of Pregnancies", placeholder="0 - 15")
            st.markdown("<br>", unsafe_allow_html=True)
        with col2:
            Glucose = st.text_input("Glucose Level (Fasting)", placeholder="40 - 600 mg/dL")
            st.markdown("<br>", unsafe_allow_html=True)
        with col3:
            BloodPressure = st.text_input("Blood Pressure value (Diastolic)", placeholder="60 - 120+ mmHg")
            st.markdown("<br>", unsafe_allow_html=True)
        with col1:
            SkinThickness = st.text_input("Skin Thickness value", placeholder="5 - 99 mm")
            st.markdown("<br>", unsafe_allow_html=True)
        with col2:
            Insulin = st.text_input("Insulin Level", placeholder="0 - 276 µIU/mL")
            st.markdown("<br>", unsafe_allow_html=True)
        with col3:
            BMI = st.text_input("BMI value", placeholder="10 - 60+")
            st.markdown("<br>", unsafe_allow_html=True)
        with col1:
            DiabetesPedigreeFunction = st.text_input("Diabetes Pedigree Function value", placeholder="0.01 - 2.5+")
            st.markdown("<br>", unsafe_allow_html=True)
        with col2:
            Age = st.text_input("Age of the Person", placeholder="1 - 120 years")
            st.markdown("<br>", unsafe_allow_html=True)


        # creating a button for Prediction
        if st.button('Diabetes Test Result'):
            if Pregnancies == '' or Glucose == '' or BloodPressure == '' or SkinThickness == '' or Insulin == '' or BMI == '' or DiabetesPedigreeFunction == '' or Age == '':
                st.info("ⓘ   Please enter all the fields")
                time.sleep(1.5)
                st.rerun()
                
            diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
            if (diab_prediction[0] == 1):
                st.session_state["Diabetesdiagnosis"] = "positive"
            else:
                st.session_state["Diabetesdiagnosis"] = "negative"

        # st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.get("Diabetesdiagnosis") == "positive":
            st.error('⚠︎   The person is probably diabetic. Please consult a diabetologist.')
        elif st.session_state.get("Diabetesdiagnosis") == "negative":
            st.success('The person is not diabetic')
        
        parameter_info = {
        "Pregnancies": {"value": Pregnancies, "normal": (0, 5), "risk": (6, 8), "unit": ""},
        "Glucose": {"value": Glucose, "normal": (40, 99), "risk": (100, 125), "unit": "mg/dL"},
        "Blood Pressure": {"value": BloodPressure, "normal": (60, 80), "risk": (81, 89), "unit": "mmHg"},
        "Skin Thickness": {"value": SkinThickness, "normal": (5, 25), "risk": (26, 34), "unit": "mm"},
        "Insulin": {"value": Insulin, "normal": (0, 100), "risk": (101, 165), "unit": "µIU/mL"},
        "BMI": {"value": BMI, "normal": (10, 24.9), "risk": (25, 29.9), "unit": ""},
        "Diabetes Pedigree Function": {"value": DiabetesPedigreeFunction, "normal": (0.01, 0.5), "risk": (0.51, 0.6), "unit": ""},
        }
        
        if st.session_state.get("Diabetesdiagnosis") in ["positive", "negative"]:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("View Report"):

                for param, info in parameter_info.items():
                    try:
                        val = float(info["value"])
                        normal_low, normal_high = info["normal"]
                        risk_low, risk_high = info["risk"]

                        if risk_high < val:
                            st.error(f"⚠︎    {param}: {val} {info['unit']} — High risk")
                        elif normal_low <= val <= normal_high:
                            st.success(f" {param}: {val} {info['unit']} — Normal")
                        elif risk_low <= val <= risk_high:
                            st.warning(f"ⓘ   {param}: {val} {info['unit']} — Early warning for diabetes risk")
                    except:
                        st.warning(f"⚠︎ {param}: Invalid or missing input")
            
                st.session_state["Diabetesdiagnosis"] = None

    
    
    
    
    
    
    elif selected == "Heart Disease Detection":
        st.markdown("<h1 style='text-align: center;'>Heart Disease Detection</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            age = st.text_input("Age", placeholder="1 - 120 years")
            st.markdown("<br>", unsafe_allow_html=True)
        with col2:
            sex = st.text_input("Sex (0 = Female, 1 = Male)", placeholder="0 or 1")
            st.markdown("<br>", unsafe_allow_html=True)
        with col3:
            cp = st.text_input("Chest Pain Type (0-3)", placeholder="0 - 3")
            st.markdown("<br>", unsafe_allow_html=True)
        with col1:
            trestbps = st.text_input("Resting Blood Pressure", placeholder="80 - 200 mmHg")
            st.markdown("<br>", unsafe_allow_html=True)
        with col2:
            chol = st.text_input("Serum Cholestoral", placeholder="60 - 600 mg/dL")
            st.markdown("<br>", unsafe_allow_html=True)
        with col3:
            fbs = st.text_input("Fasting Blood Sugar > 120 mg/dL (1 = true, 0 = false)", placeholder="0 or 1")
            st.markdown("<br>", unsafe_allow_html=True)
        with col1:
            restecg = st.text_input("Resting ECG Results (0-2)", placeholder="0 - 2")
            st.markdown("<br>", unsafe_allow_html=True)
        with col2:
            thalach = st.text_input("Max Heart Rate Achieved", placeholder="60 - 210 bpm")
            st.markdown("<br>", unsafe_allow_html=True)
        with col3:
            exang = st.text_input("Exercise Induced Angina (1 = yes; 0 = no)", placeholder="0 or 1")
            st.markdown("<br>", unsafe_allow_html=True)
        with col1:
            oldpeak = st.text_input("ST depression induced by exercise", placeholder="0.0 - 6.0")
            st.markdown("<br>", unsafe_allow_html=True)
        with col2:
            slope = st.text_input("Slope of the peak exercise ST segment (0-2)", placeholder="0 - 2")
            st.markdown("<br>", unsafe_allow_html=True)
        with col3:
            ca = st.text_input("Number of major vessels colored by fluoroscopy (0-4)", placeholder="0 - 4")
            st.markdown("<br>", unsafe_allow_html=True)
        with col2:
            thal = st.text_input("Thalassemia (1 = normal; 2 = fixed defect; 3 = reversible defect)", placeholder="1 - 3")
            st.markdown("<br>", unsafe_allow_html=True)

        # creating a button for Prediction
        if st.button('Heart Disease Test Result'):
            if age == '' or sex == '' or cp == '' or trestbps == '' or chol == '' or fbs == '' or restecg == '' or thalach == '' or exang == '' or oldpeak == '' or slope == '' or ca == '' or thal == '':
                st.info("ⓘ   Please enter all the fields")
                time.sleep(1.5)
                st.rerun()

            heart_prediction = heart_disease_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
            if heart_prediction[0] == 1:
                st.session_state["HeartDiagnosis"] = "positive"
            else:
                st.session_state["HeartDiagnosis"] = "negative"

        if st.session_state.get("HeartDiagnosis") == "positive":
            st.error('⚠︎   The person is likely to have heart disease. Please consult a cardiologist.')
        elif st.session_state.get("HeartDiagnosis") == "negative":
            st.success('The person does not show signs of heart disease.')

        parameter_info = {
        "Chest Pain Type": {"value": cp, "normal": (0, 1), "risk": (2, 3), "unit": ""},  # 0-typical angina to 3-asymptomatic
        "Resting Blood Pressure": {"value": trestbps, "normal": (80, 120), "risk": (121, 139), "unit": "mmHg"},
        "Serum Cholestoral": {"value": chol, "normal": (0, 200), "risk": (201, 240), "unit": "mg/dL"},
        "Fasting Blood Sugar": {"value": fbs, "normal": (0, 0), "risk": (1, 1), "unit": ""},  # >120 mg/dL is risky
        "Resting ECG": {"value": restecg, "normal": (0, 1), "risk": (2, 2), "unit": ""},
        "Max Heart Rate Achieved": {"value": thalach, "normal": (60, 160), "risk": (161, 185), "unit": "bpm"},
        "Exercise Induced Angina": {"value": exang, "normal": (0, 0), "risk": (1, 1), "unit": ""},
        "ST depression induced by exercise": {"value": oldpeak, "normal": (0.0, 1.0), "risk": (1.1, 2.0), "unit": ""},
        "Slope of the peak exercise ST segment": {"value": slope, "normal": (0, 1), "risk": (1, 2), "unit": ""},  # 0 = downsloping
        "Number of major vessels colored by fluoroscopy": {"value": ca, "normal": (0, 0), "risk": (1, 2), "unit": ""},
        "Thalassemia": {"value": thal, "normal": (1, 2), "risk": (3, 3), "unit": ""},  # 3 = reversible defect
        }

        if st.session_state.get("HeartDiagnosis") in ["positive", "negative"]:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("View Report"):
                for param, info in parameter_info.items():
                    try:
                        val = float(info["value"])
                        normal_low, normal_high = info["normal"]
                        risk_low, risk_high = info["risk"]

                        if risk_high < val:
                            st.error(f"⚠︎    {param}: {val} {info['unit']} — High risk")
                        elif normal_low <= val <= normal_high:
                            st.success(f" {param}: {val} {info['unit']} — Normal")
                        elif risk_low <= val <= risk_high:
                            st.warning(f"ⓘ   {param}: {val} {info['unit']} — Early warning for heart disease risk")
                    except:
                        st.warning(f"⚠︎ {param}: Invalid or missing input")

                st.session_state["HeartDiagnosis"] = None
        






    elif selected == "Parkinsons Detection":
        st.markdown("<h1 style='text-align: center;'>Parkinsons Detection</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Input fields
        fields = [
            "Fo(Hz)", "Fhi(Hz)", "Flo(Hz)", "Jitter(%)", "Jitter(Abs)", "RAP",
            "PPQ", "DDP", "Shimmer", "Shimmer(dB)", "APQ3", "APQ5",
            "APQ", "DDA", "NHR", "HNR", "RPDE", "DFA", "spread1", "spread2", "D2", "PPE"
        ]

        values = {}
        col_count = 5
        cols = st.columns(col_count)
        
        for idx, field in enumerate(fields):
            with cols[idx % col_count]:
                values[field] = st.text_input(field, placeholder="Enter value")
                st.markdown("<br>", unsafe_allow_html=True)

        if st.button('Parkinson Test Result'):
            if any(val.strip() == '' for val in values.values()):
                st.info("ⓘ   Please enter all the fields")
                time.sleep(1.5)
                st.rerun()
                

            input_data = [float(values[field]) for field in fields]
            parkinsons_prediction = parkinsons_model.predict([input_data])

            if parkinsons_prediction[0] == 1:
                st.session_state["ParkinsonDiagnosis"] = "positive"
            else:
                st.session_state["ParkinsonDiagnosis"] = "negative"

        if st.session_state.get("ParkinsonDiagnosis") == "positive":
            st.error('⚠︎   The person is likely to have Parkinson’s disease. Please consult a neurologist.')
        elif st.session_state.get("ParkinsonDiagnosis") == "negative":
            st.success('The person is not likely to have Parkinson’s disease.')

        # Report logic
        parameter_info = {
            "Fo(Hz)": {"value": values["Fo(Hz)"], "normal": (120, 160), "warning": (100, 119), "risk": (0, 99), "unit": "Hz"},
            "Fhi(Hz)": {"value": values["Fhi(Hz)"], "normal": (180, 250), "warning": (251, 300), "risk": (301, 600), "unit": "Hz"},
            "Flo(Hz)": {"value": values["Flo(Hz)"], "normal": (80, 110), "warning": (111, 130), "risk": (131, 300), "unit": "Hz"},
            "Jitter(%)": {"value": values["Jitter(%)"], "normal": (0.0, 0.01), "warning": (0.011, 0.02), "risk": (0.021, 0.1), "unit": "%"},
            "Jitter(Abs)": {"value": values["Jitter(Abs)"], "normal": (0.0, 0.00007), "warning": (0.000071, 0.0001), "risk": (0.00011, 0.001), "unit": ""},
            "RAP": {"value": values["RAP"], "normal": (0.0, 0.005), "warning": (0.0051, 0.01), "risk": (0.011, 0.05), "unit": ""},
            "PPQ": {"value": values["PPQ"], "normal": (0.0, 0.005), "warning": (0.0051, 0.01), "risk": (0.011, 0.05), "unit": ""},
            "Jitter:DDP": {"value": values["DDP"], "normal": (0.0, 0.015), "warning": (0.016, 0.03), "risk": (0.031, 0.1), "unit": ""},
            "Shimmer": {"value": values["Shimmer"], "normal": (0.0, 0.02), "warning": (0.021, 0.04), "risk": (0.041, 0.1), "unit": ""},
            "Shimmer(dB)": {"value": values["Shimmer(dB)"], "normal": (0.0, 0.2), "warning": (0.21, 0.3), "risk": (0.31, 1.0), "unit": "dB"},
            "APQ3": {"value": values["APQ3"], "normal": (0.0, 0.02), "warning": (0.021, 0.04), "risk": (0.041, 0.2), "unit": ""},
            "APQ5": {"value": values["APQ5"], "normal": (0.0, 0.03), "warning": (0.031, 0.06), "risk": (0.061, 0.2), "unit": ""},
            "APQ": {"value": values["APQ"], "normal": (0.0, 0.03), "warning": (0.031, 0.06), "risk": (0.061, 0.3), "unit": ""},
            "DDA": {"value": values["DDA"], "normal": (0.0, 0.06), "warning": (0.061, 0.09), "risk": (0.091, 0.3), "unit": ""},
            "NHR": {"value": values["NHR"], "normal": (0.0, 0.02), "warning": (0.021, 0.05), "risk": (0.051, 0.3), "unit": ""},
            "HNR": {"value": values["HNR"], "normal": (20, 30), "warning": (15, 19), "risk": (0, 14), "unit": "dB"},
            "RPDE": {"value": values["RPDE"], "normal": (0.2, 0.4), "warning": (0.41, 0.5), "risk": (0.51, 1.0), "unit": ""},
            "DFA": {"value": values["DFA"], "normal": (0.5, 0.65), "warning": (0.66, 0.75), "risk": (0.76, 1.0), "unit": ""},
            "spread1": {"value": values["spread1"], "normal": (-7, -4), "warning": (-10, -7.1), "risk": (-20, -10.1), "unit": ""},
            "spread2": {"value": values["spread2"], "normal": (0.0, 0.2), "warning": (0.21, 0.3), "risk": (0.31, 1.0), "unit": ""},
            "D2": {"value": values["D2"], "normal": (2.0, 2.5), "warning": (2.51, 3.0), "risk": (3.01, 5.0), "unit": ""},
            "PPE": {"value": values["PPE"], "normal": (0.0, 0.2), "warning": (0.21, 0.3), "risk": (0.31, 1.0), "unit": ""}
        }

        if st.session_state.get("ParkinsonDiagnosis") in ["positive", "negative"]:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("View Report"):
                for param, info in parameter_info.items():
                    try:
                        val = float(info["value"])
                        normal_low, normal_high = info["normal"]
                        warning_low, warning_high = info["warning"]
                        risk_low, risk_high = info["risk"]

                        if risk_low <= val <= risk_high:
                            st.error(f"⚠︎    {param}: {val} {info['unit']} — High risk")
                        elif warning_low <= val <= warning_high:
                            st.warning(f"ⓘ   {param}: {val} {info['unit']} — Early warning for Parkinson's disease risk")
                        elif normal_low <= val <= normal_high:
                            st.success(f"{param}: {val} {info['unit']} — Normal")
                        else:
                            st.warning(f"⚠︎ {param}: {val} {info['unit']} — Out of known range")
                    except:
                        st.warning(f"⚠︎ {param}: Invalid or missing input")

                st.session_state["ParkinsonDiagnosis"] = None
    

def doctor_directory():
    # Load the data
    @st.cache_data
    def load_data():
        return pd.read_csv("./Models/Doctor Dataset.csv")

    df = load_data()

    if st.button("Go to Home"):    
        st.session_state.page = "home"
        st.session_state['Diabetesdiagnosis'] = None
        st.rerun()

    # Centered title using markdown
    st.markdown("<h1 style='text-align: center;'>Doctor Directory</h1>", unsafe_allow_html=True)

    # Centered subheading/text
    st.markdown("<p style='text-align: center;'>Click the following buttons to see doctors by their specialization:</p>", unsafe_allow_html=True)


    df["Contact"] = pd.to_numeric(df["Contact"], errors="coerce")
    df["Contact"] = df["Contact"].fillna(0).astype("int64").astype("str")

    # Optional: Replace '0' with 'Unknown'
    df["Contact"] = df["Contact"].replace("0", "Unknown")

    # --- SESSION STATE INITIALIZATION ---
    if "specialty" not in st.session_state:
        st.session_state.specialty = None
    if "start_idx" not in st.session_state:
        st.session_state.start_idx = 0

    # --- BUTTON HANDLERS TO SET SPECIALTY ---
    col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 3, 1])
    with col1:
        if st.button("Cardiologist"):
            st.session_state.specialty = "Cardiologist"
            st.session_state.start_idx = 0
    with col3:
        if st.button("Neurologist"):
            st.session_state.specialty = "Neurologist"
            st.session_state.start_idx = 0
    with col5:
        if st.button("Diabetologist"):
            st.session_state.specialty = "Diabetologist"
            st.session_state.start_idx = 0

    # --- DISPLAY LOGIC ---
    def display_paginated_table(filtered, title):
        st.subheader(title)
        table = filtered[["Doctor", "Clinic", "Contact"]].reset_index(drop=True)
        table.index += 1

        step = 8
        start = st.session_state.start_idx
        end = start + step
        st.table(table[start:end])

        info_message = ""

    # Layout: 3 columns to center buttons
        col1, col2, col3 = st.columns([2, 1, 2])

        with col2:
            # Sub-columns for side-by-side buttons
            btn_col1, btn_col2 = st.columns(2)

            with btn_col1:
                if st.button("Previous"):
                    if start > 0:
                        st.session_state.start_idx = max(start - step, 0)
                        st.rerun()
                    else:
                        info_message = " This is the first page."

            with btn_col2:
                if st.button("Show more"):
                    if end < len(table):
                        st.session_state.start_idx = start + step
                        st.rerun()
                    else:
                        info_message = " No more doctors to show."
        if info_message:
            st.info("ⓘ  " + info_message)
            time.sleep(1.5)
            info_message = ""
            st.rerun()


    # --- FILTER & DISPLAY ---
    if st.session_state.specialty:
        filtered = df[df["Specialization"] == st.session_state.specialty]
        emoji_map = {
            "Cardiologist": "❤️ Cardiologists",
            "Neurologist": "⚕️ Neurologists",
            "Diabetologist": "🩸  Diabetologists"
        }
        display_paginated_table(filtered, emoji_map[st.session_state.specialty])

    else:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("<p style='text-align: center; color: red;'>Please select a specialization</p>", unsafe_allow_html=True)


if st.session_state.page == "home":
    disease_prediction()
elif st.session_state.page == "doctor_directory":
    doctor_directory()
