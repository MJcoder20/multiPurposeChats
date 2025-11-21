# import streamlit as st
# import requests
#
# # API_BASE = st.secrets.get("api_base", "http://backend:8000")  # docker compose friendly
# st.title("Multi Purpose Chats")
# st.write("We recommend a chatbot according to your intended use.")
#
# uploaded = st.text_field("Write why you need a chatbot")
# # priority = st.selectbox("Task Priority", ["Top", "Average", "Low"])
#
# if uploaded is not None:
#     if st.button("Process"):
#         with st.spinner("Processing..."):
#             r = requests.post(f"{API_BASE}", data=uploaded, timeout=600)
#             if r.status_code != 200:
#                 st.error(f"Error: {r.text}")
#             else:
#                 j = r.json()
#                 st.success("Done!")


import streamlit as st

from services.ollama import chat_with_gpt, chat_with_gemini


# from processing.fileProcessing import (
#     extract_text_from_pdf,
#     extract_text_from_docx,
# )
# from services.ollama import (
#     RESUME_PROMPT,
#     RESUME_PROMPT2,
#     RESUME_PROMPT3,
#     make_request,
#     extract_info,
#     shortlist,
#     final_analysis,
# )
# from embedding.embeddingGen import EmbeddingGenerator
# from testing.test_File import test_pdfFile_parsing, test_docxFile_parsing, test_embedding, test_similarity, \
#     test_threshold, \
#     test_request, test_extraction, test_shortlisting, test_analysis


def main():
    st.title("Multi Purpose Chat")
    st.write("We recommend a chatbot according to your intended use.")

    # To enter user's intended use text
    purposeOfUse = st.text_input("Write why you need a chatbot")

    if purposeOfUse:
        # To choose method of execution
        choice = st.selectbox("Would you like to use a specific chatbot or a suggested one according to your use?",
                              ["Suggested Chatbot", "Specific Chatbot"])
        preferedChatbot = ""
        if choice == "Specific Chatbot":
            # To choose the chatbot for execution in case the user has chosen the specific chatbot option
            preferedChatbot = st.selectbox("Select a Chatbot",
                                           ["Google Gemini", "Claude", "Copilot", "ChatGPT", "DeepSeek", "Perplexity",
                                            "Jasper", "Grok"])
        if preferedChatbot == "ChatGPT":
            # Streamlit UI
            # st.title("Chat with ChatGPT")
            # st.markdown("Ask me anything!")

            # Input box for the user
            # user_input = st.text_input("You:", "")

            # Display chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # if user_input:
            #     # Add user message to history
            #     st.session_state.messages.append(f"You: {user_input}")

            # Get response from ChatGPT
            chatbot_response = chat_with_gpt(purposeOfUse)
            st.session_state.messages.append(f"ChatGPT: \n{chatbot_response}")

            # Display all chat history
            for message in st.session_state.messages:
                st.write(message)

        elif preferedChatbot == "Google Gemini":
            # Display chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            image = ""
            # Get response from Gemini
            gemini_response = chat_with_gemini(purposeOfUse, image)
            st.session_state.messages.append(f"Gemini: \n{gemini_response}")

            # Display all chat history
            for message in st.session_state.messages:
                st.write(message)


    # resume_files = sl.file_uploader(
    #     "Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True
    # )
    #
    # # User-defined criteria
    # sl.write("### Evaluation Criteria")
    # required_skills = sl.text_input(
    #     "Required skills (comma-separated)", "Python, Machine Learning"
    # )
    # min_experience = sl.number_input(
    #     "Minimum years of experience required", min_value=0, value=3
    # )
    # education_level = sl.selectbox("Required Education Level", ["Bachelor's Degree", "Master's Degree",
    #                                                             "PHD Degree", "None"])

    # Submit button
    if st.button("Process"):
        with st.spinner("Processing..."):
            if purposeOfUse:
                try:
                    # Validate Purpose of Use text
                    if not purposeOfUse.strip():
                        st.error("The purpose of use field is empty.")
                        return

                    # Extract text from resumes
                    # st.write("Extracting text from resumes...")
                    # resumes = []
                    # for f in resume_files:
                    #     if f.name.endswith(".pdf"):
                    #         text = extract_text_from_pdf(f)
                    #     elif f.name.endswith(".docx"):
                    #         text = extract_text_from_docx(f)
                    #     else:
                    #         sl.error(f"Unsupported resume file format: {f.name}")
                    #         return
                    #     if not text:
                    #         sl.error("No valid resume texts found.")
                    #         return
                    #     else:
                    #         resumes.append(Resume(text))

                    # Generating Embedding for the job description and resumes
                    # embedder = EmbeddingGenerator()
                    # job_embedding = embedder.generate(job_text)
                    # for i, resume in enumerate(resumes):
                    #     emb = embedder.generate(resume.text)
                    #     resume.embedding = emb
                    # Generating cosine similarity of each resume using the generated embedding
                    # for the job description and the resume
                    # resume.similarity = calculate_similarity(job_embedding, emb)

                    # returns sorted shortlisted resumes based on a threshold value compared
                    # with the cosine similarity of each resume
                    # resumes = filter_by_threshold(resumes, 0.5450)

                    # Extracting key features from the resumes
                    # resume_features = [
                    #     make_request(extract_info(
                    #         resumes,
                    #         resume.text,
                    #         job_text,
                    #         RESUME_PROMPT,
                    #         min_experience,
                    #         required_skills,
                    #         education_level,
                    #
                    #     ))
                    #     for resume in resumes
                    # ]

                    # output the extracted features and cosine similarity for each resume
                    # sl.write("### Extracted Resume Features:")
                    # resumes_f = []
                    # i = 1
                    # for features, res in zip(resume_features, resumes):
                    #     sl.write(f"Resume {i}:")
                    #     sl.write(features)
                    #     sl.write(f"Cosine Similarity: {res.similarity}")
                    #     resume = f"Resume {i}: {features}\nCosine Similarity: {res.similarity}"
                    #     resumes_f.append(resume)
                    #     i = i + 1

                    # # shortlist the resumes into top 5
                    # short = make_request(shortlist(RESUME_PROMPT2, resumes_f))
                    # # Analyze top candidates' strengths and weaknesses, then conclude the best resume
                    # analysis = make_request(final_analysis(RESUME_PROMPT3, job_text, short))

                    # sl.write(short)  # output shortlist
                    # sl.write(analysis)  # output analysis

                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please upload the purpose of use.")


if __name__ == "__main__":
    main()
    # Testing functions
    # test_pdfFile_parsing()
    # test_docxFile_parsing()
    # test_embedding()
    # test_similarity()
    # test_threshold()
    # test_request()
    # test_extraction()
    # test_shortlisting()
    # test_analysis()
