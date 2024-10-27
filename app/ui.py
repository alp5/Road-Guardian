import streamlit as st
from backend.document_processing import handle_query_submission
from app.sidebar import sidebar  # Assuming sidebar is defined in app.sidebar


def render_ui(driver_metadata_paths, rider_metadata_paths, driver_image_folders, rider_image_folders):
    # Display the sidebar
    sidebar()

# Set the correct password
PASSWORD = "Tptest"

# Create a password input field
password = st.text_input("Enter Password:", type="password")

# Display the disclaimer in a collapsible expander
with st.expander("IMPORTANT NOTICE", expanded=False):
    st.write("""
    This web application is a prototype developed for educational purposes only. 
    The information provided here is NOT intended for real-world usage and should 
    not be relied upon for making any decisions, especially those related to 
    financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. 
    You assume full responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalised advice.
    """)

# Check if the password is correct
if password == PASSWORD:
    st.success("Welcome!")
    
    # Learner type selection
    learner_type = st.radio("Choose learner type", options=["Learner Driver", "Learner Rider"])

    # Set metadata paths based on learner type
    if learner_type == "Learner Driver":
        metadata_paths = driver_metadata_paths
        image_folders = driver_image_folders
    else:
        metadata_paths = rider_metadata_paths
        image_folders = rider_image_folders

    # Query input
    query = st.text_area("Enter your question")

    common_words = {"a", "an", "the", "is", "are", "in", "on", "at", "for", "to", "and", "but", "if", "or"}

    if st.button("Submit"):
        if query.strip() == "":
            st.warning("Please enter a question.")
        else:
            query_words = set(query.strip().lower().split())
            if query_words.issubset(common_words):
                st.warning("Please enter a more relevant question.")
            else:
                # Show a loading bar with progress increments
                progress_bar = st.progress(0)

                with st.spinner("Processing your query, please wait..."):
                    # Simulate the steps with a progress bar and detailed updates
                    progress_bar.progress(10)
                    st.write("Step 1: Retrieving relevant information from theory books...")
                    findings, llm_response, mcqs = handle_query_submission(query, metadata_paths, image_folders)

                    progress_bar.progress(70)
                    st.write("Step 2: Generating response from the LLM...")

                    # Finalizing the progress bar
                    progress_bar.progress(100)

                # Display findings, LLM response, and MCQs
                if findings:
                    st.markdown("### Theory Book Matches")
                    for i, finding in enumerate(findings):
                        with st.expander(f"Match {i + 1}: {finding.page_content[:100]}..."):
                            st.write(f"Content: {finding.page_content}")
                            st.write(f"Metadata: {finding.metadata}")

                    st.markdown("### LLM Response")
                    st.write(llm_response)

                    # Display "Test Me" questions
                    st.write("Step 3: Creating 'Test Me' questions...")
                    st.markdown("### Test Me: Knowledge Retention")
                    st.write(mcqs)
                else:
                    st.write("No relevant data found in the theory books.")
else:
    st.warning("Incorrect password. Please try again.")


