import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pickle
import time
import os

st.set_page_config(page_title="Multiple Disease Prediction", layout="wide")

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

# st.markdown("""
#         <style>
#          /* Hover: border and text cyan */
#         div.stButton > button:hover {
#         border-color: #00ffff !important; /* cyan border */
#         color: #00ffff !important;        /* cyan text */
#         background-color: transparent !important;
#         }

#         /* Active (while clicking): cyan filled */
#         div.stButton > button:active {
#         background-color: #00ffff !important; /* cyan background */
#         color: black !important;               /* white text */
#         border-color: #00ffff !important;      /* cyan border */
#         }

#         /* Focus: same as hover, keep cyan border and text */
#         div.stButton > button:focus-visible,
#         div.stButton > button:focus {
#         border-color: #00ffff !important;
#         color: #00ffff !important;
#         background-color: transparent ;
#         outline: none !important;
#         box-shadow: none !important;
#         }
            
#         /* Remove default Streamlit focus ring and red border */
#         input:focus-visible {
#         border: 3px solid #00ffff !important;  /* Cyan border */
#         box-shadow: none !important;           /* Remove glow */
#         outline: none !important;              /* Remove default outline */
#         }
#         </style>
#         """, unsafe_allow_html=True)

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
                st.warning("⚠︎   Please enter all the fields")
                st.stop()
                
            diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
            if (diab_prediction[0] == 1):
                st.session_state["Diabetesdiagnosis"] = "positive"
            else:
                st.session_state["Diabetesdiagnosis"] = "negative"

        # st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.get("Diabetesdiagnosis") == "positive":
            st.error('⚠︎   The person is probably diabetic. Consulting a doctor is highly recommended')
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

    elif selected == "Parkinsons Detection":
        st.markdown("<h1 style='text-align: center;'>Parkinsons Detection</h1>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
    

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