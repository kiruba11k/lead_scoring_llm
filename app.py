import streamlit as st
import pandas as pd

from core.apify_extractor import LinkedInAPIExtractor
from core.feature_builder import FeatureBuilderLLM
from core.groq_scorer import GroqLeadScorer


st.set_page_config(page_title="LLM Lead Scoring", layout="wide")


class App:
    def __init__(self):
        self.state = st.session_state

        if "last_url" not in self.state:
            self.state.last_url = ""
        if "linkedin_data" not in self.state:
            self.state.linkedin_data = None
        if "payload" not in self.state:
            self.state.payload = None
        if "llm_result" not in self.state:
            self.state.llm_result = None

        if "user_input" not in self.state:
            self.state.user_input = {
                "company_name": "",
                "company_size": "",
                "annual_revenue": "",
                "industry": "",
            }

        apify_key = st.secrets.get("APIFY", "")
        groq_key = st.secrets.get("GROQ_API_KEY", "")

        self.linkedin = LinkedInAPIExtractor(apify_key) if apify_key else None
        self.builder = FeatureBuilderLLM()
        self.scorer = GroqLeadScorer(groq_key) if groq_key else None

    def run(self):
        st.title(" Groq LLM Lead Scoring Platform")

        st.caption("Dynamic scoring + reasons for ANY sector. No static defaults.")

        left, right = st.columns([2, 1])

        with right:
            st.subheader("Manual Company Input")
            with st.form("manual_form"):
                self.state.user_input["company_name"] = st.text_input("Company Name", self.state.user_input["company_name"])
                self.state.user_input["company_size"] = st.text_input("Company Size", self.state.user_input["company_size"])
                self.state.user_input["annual_revenue"] = st.text_input("Annual Revenue", self.state.user_input["annual_revenue"])
                self.state.user_input["industry"] = st.text_input("Industry", self.state.user_input["industry"])

                if st.form_submit_button("Save"):
                    st.success("Saved manual company info")

        with left:
            st.subheader("Step 1: Extract LinkedIn Data")

            linkedin_url = st.text_input("LinkedIn Profile URL", placeholder="https://www.linkedin.com/in/username/")

            # FIX: Clear old data when new URL comes
            if linkedin_url and linkedin_url != self.state.last_url:
                self.state.last_url = linkedin_url
                self.state.linkedin_data = None
                self.state.payload = None
                self.state.llm_result = None

            if st.button("Extract Profile", type="primary", disabled=not linkedin_url):
                if not self.linkedin:
                    st.error("APIFY key missing in secrets.")
                else:
                    with st.spinner("Extracting LinkedIn profile + posts..."):
                        data = self.linkedin.extract_profile(linkedin_url)

                    if not data:
                        st.error("Extraction failed.")
                    else:
                        self.state.linkedin_data = data
                        self.state.payload = self.builder.build_payload(data, self.state.user_input)
                        st.success("Extraction completed!")

            if self.state.payload:
                st.subheader("Extracted Preview (Payload)")
                st.json(self.state.payload)

            st.subheader("Step 2: Generate Score (Groq LLM)")

            if st.button("Generate Lead Score", type="primary", disabled=(self.state.payload is None)):
                if not self.scorer:
                    st.error("GROQ_API_KEY missing in secrets.")
                else:
                    with st.spinner("Scoring lead using Groq LLM..."):
                        result = self.scorer.score(self.state.payload)

                    if not result:
                        st.error("Scoring failed.")
                    else:
                        self.state.llm_result = result

            if self.state.llm_result:
                st.subheader("Scoring Results")
                st.json(self.state.llm_result)

                # Show pretty table
                reasons = self.state.llm_result.get("reasons", [])
                if reasons:
                    st.markdown("###  Reasons")
                    for r in reasons:
                        st.write("•", r)

                next_steps = self.state.llm_result.get("next_steps", [])
                if next_steps:
                    st.markdown("###  Next Steps")
                    for s in next_steps:
                        st.write("->", s)


if __name__ == "__main__":
    App().run()
