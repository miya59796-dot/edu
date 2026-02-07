import streamlit as st
import pandas as pd
import plotly.express as px
from certification_model import CertificationModel

# Set page config
st.set_page_config(
    page_title="EduCert - Educational App Certification",
    page_icon="🎓",
    layout="wide"
)

# Initialize Model
@st.cache_resource
def get_model():
    return CertificationModel()

model = get_model()

# Sidebar
st.sidebar.title("EduCert 🎓")
st.sidebar.info("A Learning-Science-Based Certification Model for Educational Apps")
page = st.sidebar.radio("Navigation", ["Home", "Evaluate App", "Pilot Study", "Methodology"])

if page == "Home":
    st.title("Welcome to EduCert")
    st.markdown("""
    ### About the Project
    This tool provides a systematic, learning-science-based certification framework for educational apps.
    It evaluates apps based on four key dimensions:
    
    1. **Cognitive Development**: Alignment with cognitive science.
    2. **Instructional Design**: Pedagogical effectiveness.
    3. **Motivation & Engagement**: Mechanics that sustain interest.
    4. **Learning Outcomes**: Measurable evidence of learning.
    
    ### Get Started
    Navigate to **Evaluate App** to start a new assessment.
    """)
    
    st.image("https://images.unsplash.com/photo-1509062522246-3755977927d7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", caption="Educational Technology")

elif page == "Evaluate App":
    st.title("Evaluate an Educational App")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("App Details")
        app_name = st.text_input("App Name", placeholder="e.g., Duolingo")
        app_desc = st.text_area("App Description", placeholder="Brief description of the app...")
        
        st.markdown("---")
        st.subheader("Rubric Assessment")
        
        user_scores = {}
        
        for category in model.rubric:
            with st.expander(f"**{category.name}**", expanded=True):
                st.markdown(f"*{category.description}*")
                for criterion in category.criteria:
                    st.markdown(f"**{criterion.name}**")
                    st.caption(criterion.description)
                    score = st.slider(
                        f"Rate {criterion.name} (1-5)", 
                        min_value=1, 
                        max_value=5, 
                        value=3, 
                        key=criterion.id
                    )
                    user_scores[criterion.id] = float(score)

    with col2:
        st.subheader("Certification Results")
        if st.button("Calculate Certification", type="primary"):
            if not app_name:
                st.error("Please enter an App Name.")
            else:
                results = model.evalutate_app(user_scores)
                
                # Display Badge
                level = results['certification_level']
                color = "gray"
                if "Platinum" in level: color = "#E5E4E2"
                elif "Gold" in level: color = "#FFD700"
                elif "Silver" in level: color = "#C0C0C0"
                elif "Bronze" in level: color = "#CD7F32"
                
                st.markdown(f"""
                <div style="background-color: {color}; padding: 20px; border-radius: 10px; text-align: center; color: black;">
                    <h2>{level}</h2>
                    <h1>{results['final_score']}%</h1>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### Category Breakdown")
                cat_scores = results['category_scores']
                
                # Radar Chart
                df = pd.DataFrame(dict(
                    r=list(cat_scores.values()),
                    theta=list(cat_scores.keys())
                ))
                fig = px.line_polar(df, r='r', theta='theta', line_close=True)
                fig.update_traces(fill='toself')
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
                st.plotly_chart(fig, use_container_width=True)
                
                st.json(results)

elif page == "Methodology":
    st.title("Certification Methodology")
    st.markdown("The EduCert model uses a weighted scoring system based on learning sciences research.")
    
    for category in model.rubric:
        st.markdown(f"### {category.name} (Weight: {int(category.weight*100)}%)")
        st.markdown(category.description)
        st.markdown("| Criterion | Description | Weight |")
        st.markdown("| --- | --- | --- |")
        for crit in category.criteria:
            st.markdown(f"| **{crit.name}** | {crit.description} | {crit.weight} |")
        st.markdown("---")

elif page == "Pilot Study":
    st.title("Pilot Assessment Results")
    st.markdown("We applied the EduCert framework to several popular educational apps to validate the model.")
    
    # Pilot Data
    pilot_data = [
        {
            "name": "Duolingo",
            "description": "Language learning app using gamification.",
            "scores": {
                "cog_1": 5, "cog_2": 4, "cog_3": 5, "cog_4": 3,
                "inst_1": 4, "inst_2": 5, "inst_3": 5, "inst_4": 5,
                "mot_1": 3, "mot_2": 5, "mot_3": 4,
                "out_1": 3, "out_2": 2
            }
        },
        {
            "name": "Khan Academy",
            "description": "Video lessons and practice exercises.",
            "scores": {
                "cog_1": 4, "cog_2": 5, "cog_3": 4, "cog_4": 2,
                "inst_1": 5, "inst_2": 4, "inst_3": 5, "inst_4": 5,
                "mot_1": 5, "mot_2": 2, "mot_3": 5,
                "out_1": 5, "out_2": 4
            }
        },
         {
            "name": "Quizlet",
            "description": "Flashcards and study tools.",
            "scores": {
                "cog_1": 4, "cog_2": 3, "cog_3": 4, "cog_4": 4,
                "inst_1": 3, "inst_2": 3, "inst_3": 2, "inst_4": 5,
                "mot_1": 3, "mot_2": 4, "mot_3": 4,
                "out_1": 3, "out_2": 2
            }
        }
    ]
    
    selected_app_name = st.selectbox("Select an App to view Certification details:", [app["name"] for app in pilot_data])
    
    for app in pilot_data:
        if app["name"] == selected_app_name:
            st.subheader(f"{app['name']}")
            st.write(app['description'])
            
            results = model.evalutate_app(app['scores'])
            
            col1, col2 = st.columns(2)
            with col1:
                level = results['certification_level']
                color = "gray"
                if "Platinum" in level: color = "#E5E4E2"
                elif "Gold" in level: color = "#FFD700"
                elif "Silver" in level: color = "#C0C0C0"
                elif "Bronze" in level: color = "#CD7F32"
                
                st.markdown(f"""
                <div style="background-color: {color}; padding: 20px; border-radius: 10px; text-align: center; color: black;">
                    <h2>{level}</h2>
                    <h1>{results['final_score']}%</h1>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                # Radar Chart
                cat_scores = results['category_scores']
                df = pd.DataFrame(dict(
                    r=list(cat_scores.values()),
                    theta=list(cat_scores.keys())
                ))
                fig = px.line_polar(df, r='r', theta='theta', line_close=True)
                fig.update_traces(fill='toself')
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### Detailed Scores")
            st.write(app['scores'])
