import streamlit as st
import requests

# Page settings
st.set_page_config(page_title="AWS AI Assistant", layout="centered")
st.title("🧠 AWS AI Assistant")
st.markdown(
    """
    Welcome to your AI-powered AWS Assistant.  
    You can ask questions about AWS best practices, generate Python or CloudFormation code,  
    or request architecture diagrams based on your input.
    """
)

# Input field
query = st.text_input("Enter your query", placeholder="e.g. Draw architecture for EC2 connected to S3 and RDS")

# Submit button
if st.button("Submit"):
    if not query.strip():
        st.warning("Please enter a valid query.")
    else:
        st.info("Sending your request to the AI backend...")

        try:
            # TODO: Replace with your deployed API Gateway URL
            endpoint = "https://<api-id>.execute-api.<region>.amazonaws.com/Prod/query"

            # Use PUT method for diagram requests, POST/GET for others if needed
            response = requests.put(endpoint, params={"query": query})

            if response.status_code == 200:
                data = response.json()

                # If diagram was generated
                if "diagram_url" in data:
                    st.success("Architecture diagram generated:")
                    st.image(data["diagram_url"], caption="Generated Diagram")

                # If it's a textual response
                elif "ans" in data:
                    st.success("Here’s the AI's response:")
                    st.markdown(data["ans"])

                    if data.get("docs"):
                        st.markdown("**Related Resources:**")
                        for doc in data["docs"].split("\n"):
                            if doc.strip():
                                st.write(f"- {doc}")

                # Fallback to raw content
                else:
                    st.code(data)

            else:
                st.error(f"Error from backend: {response.status_code}")
                st.text(response.text)

        except Exception as e:
            st.error("Something went wrong 😢")
            st.exception(e)
