import streamlit as st
from PIL import Image
from services.ollama import chat_with_deepseek, chat_with_gpt, chat_with_gemini, chat_with_grok



def main():
    st.set_page_config(page_title="Multi Purpose Chat", layout="wide")
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
                                           ["Google Gemini", "Claude", "Copilot", "ChatGPT", "DeepSeek", "Grok"])
       
    # Submit button
    if st.button("Process"):
        with st.spinner("Processing..."):
            if purposeOfUse:
                try:
                    # Validate Purpose of Use text
                    if not purposeOfUse.strip():
                        st.error("The purpose of use field is empty.")
                        return
                    if preferedChatbot == "ChatGPT":
                        # Display chat history
                        if "messages" not in st.session_state:
                            st.session_state.messages = []

                        # Get response from ChatGPT
                        chatbot_response = chat_with_gpt(purposeOfUse)
                        st.session_state.messages.append(f"ChatGPT: \n{chatbot_response}")

                        # Display all chat history
                        for message in st.session_state.messages:
                            st.write(message)

                    elif preferedChatbot == "Google Gemini":
                        image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
                        if image_file is not None:
                            # Read image with PIL
                            image = Image.open(image_file)
                            # Show image
                            st.image(image, caption="Uploaded Image", use_column_width=True)
                            st.success("Image uploaded successfully!")

                        # Display chat history
                        if "messages" not in st.session_state:
                            st.session_state.messages = []

                        # Get response from Gemini
                        gemini_response = chat_with_gemini(purposeOfUse, image_file)
                        st.session_state.messages.append(f"Gemini: \n{gemini_response}")

                        # Display all chat history
                        for message in st.session_state.messages:
                            st.write(message)

                    elif preferedChatbot == "Grok":
                        if "messages" not in st.session_state:
                            st.session_state.messages= []
                        grok_response = chat_with_grok(purposeOfUse)
                        st.session_state.messages.append(f"Grok: \n{grok_response}")
                        for message in st.session_state.messages:
                            st.write(message)
                    elif preferedChatbot == "DeepSeek":
                        if "messages" not in st.session_state:
                            st.session_state.messages = []
                        deepseek_response = chat_with_deepseek(purposeOfUse)
                        st.session_state.messages.append(f"DeepSeek: \n{deepseek_response}")
                        for message in st.session_state.messages:
                            st.write(message)

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
