import time


# from dotenv import load_dotenv
import os

import openai
import requests
from openai import OpenAI

CHATBOT_CHOICE_PROMPT = """
    For general conversations and various tasks, ChatGPT is one of the most versatile.
    Google Gemini is ideal if you want real-time, up-to-date factual info, especially for research.
    Claude is best when safety, ethics, and minimizing bias are top priorities.
    Grok is for social media integration and interactions with Musk’s platforms.
    Perplexity excels at combining AI-driven search with aggregated answers from multiple sources.
    GitHub Copilot is specifically designed for developers, assisting with code generation and debugging.
    Jasper focuses heavily on helping marketers with content creation, especially for SEO and copywriting.
"""

# load_dotenv()
# API_URL = os.getenv("API_URL")
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
client = OpenAI()


# Function to get response from ChatGPT (or GPT-3.5/4)
def chat_with_gpt(user_input):
    # response = client.responses.create(
    #     model="gpt-4.1",
    #     input="Tell me a three sentence bedtime story about a unicorn."
    # )
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # You can use "gpt-4" if you have access to GPT-4
        prompt=user_input,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()


def make_request(prompt):
    try:
        # OpenRouter API configuration
        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": OLLAMA_MODEL,  # model name as shown in openrouter website
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        }

        # Make the API request
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes

        # Debug: Print the response and status code
        print("API Response Status Code:", response.status_code)
        print("API Response Content:", response.text)

        # Extract the response content
        result = response.json()
        return (
            result["choices"][0]["message"]["content"] if "choices" in result else None
        )

    except Exception as e:
        print(f"Error: {e}")
        return f"{e}"


def extract_info(resume_texts, text, job_text, prompt_template, min_experience=None, required_skills=None,
                 education_level=None):
    # Inject user criteria into the prompt
    prompt = prompt_template.format(
        min_experience=min_experience,
        required_skills=required_skills,
        education_level=education_level,
        job_text=job_text,
        resume_texts=resume_texts).replace("{text}", text)
    return prompt


def shortlist(prompt_template, prev_data):
    # Inject resumes and their extracted features into the prompt
    prompt = prompt_template.format(prev_data=prev_data)
    return prompt


def final_analysis(prompt_template, job_text, prev_data):
    # Inject shortlisted resumes and job description into the prompt
    prompt = prompt_template.format(job_text=job_text, prev_data=prev_data)
    return prompt