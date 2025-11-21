import time
from dotenv import load_dotenv
import os
import requests
import json
from openrouter import OpenRouter

CHATBOT_CHOICE_PROMPT = f"""
    Recommend a Chatbot to answer the given query based on the information provided below:
    
    Information:
        For general conversations and various tasks, ChatGPT is one of the most versatile.
        Google Gemini is ideal if you want real-time, up-to-date factual info, especially for research.
        Claude is best when safety, ethics, and minimizing bias are top priorities.
        Grok is for social media integration and interactions with Musk’s platforms.
        Perplexity excels at combining AI-driven search with aggregated answers from multiple sources.
        GitHub Copilot is specifically designed for developers, assisting with code generation and debugging.
        Jasper focuses heavily on helping marketers with content creation, especially for SEO and copywriting.
"""

load_dotenv()
# API_URL = os.getenv("API_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Function to get response from ChatGPT (or GPT-3.5/4)
def chat_with_gpt(user_input):
    # First API call with reasoning
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }

            ], "extra_body": {"reasoning": {"enabled": True}}
        })
    )

    # Extract the assistant message with reasoning_details
    response = response.json()
    response = response['choices'][0]['message']

    # Preserve the assistant message with reasoning_details
    messages = [
        {"role": "user", "content": user_input},
        {
            "role": "assistant",
            "content": response.get('content'),
            "reasoning_details": response.get('reasoning_details')  # Pass back unmodified
        },
        {"role": "user", "content": "Are you sure? Think carefully."}
    ]

    # Second API call - model continues reasoning from where it left off
    response2 = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "openai/gpt-oss-20b:free",
            "messages": messages,  # Includes preserved reasoning_details
            "extra_body": {"reasoning": {"enabled": True}}
        })
    )

    response_json = response2.json()
    if "choices" in response_json:
        return response_json["choices"][0]["message"]["content"]
    else:
        return f"Error: {response_json.get('error', 'Unexpected response format')}"


def chat_with_gemini(user_input, image):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            # "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            # "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        data=json.dumps({
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_input
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image
                            }
                        }
                    ]
                }
            ]
        })
    )
    response_json = response.json()
    if "choices" in response_json:
        return response_json["choices"][0]["message"]["content"]
    else:
        return f"Error: {response_json.get('error', 'Unexpected response format')}"


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