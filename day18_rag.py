# # %%
# from groq import Groq
# import numpy as np
# import torch
# import torch.nn as nn
# import json

# client = Groq(api_key=input("Enter your Groq Key: "))  # apni key yahan daalo")

# print("Loading model...")


# # %%
# # PakShop ka knowledge base
# pakshop_data = """
# PAKSHOP POLICIES:

# 1. RETURN POLICY:
#    - 7 din ke andar return kar sakte hain
#    - Product original condition mein hona chahiye
#    - Receipt zaroori hai

# 2. DELIVERY:
#    - Lahore: 1-2 din
#    - Karachi: 2-3 din
#    - Islamabad: 2-3 din
#    - Other cities: 3-5 din
#    - Free delivery Rs. 2000 se upar

# 3. PAYMENT:
#    - Cash on Delivery available
#    - JazzCash accepted
#    - Easypaisa accepted
#    - Credit/Debit card accepted

# 4. CUSTOMER SERVICE:
#    - Phone: 0300-1234567
#    - Email: support@pakshop.pk
#    - Hours: 9am-9pm Monday to Saturday

# 5. ORDER TRACKING:
#    - SMS pe tracking number aata hai
#    - Website pe track kar sakte hain
#    - App se bhi track ho sakta hai
# """

# print("Knowledge base ready!")
# print(f"Total characters: {len(pakshop_data)}")

# # %%
# def ask_pakshop(question):
#     response = client.chat.completions.create(
#         model="openai/gpt-oss-20b",
#         messages=[
#             {
#                 "role": "system",
#                 "content": f"""Tum PakShop ka customer service agent ho.
#                 Sirf is information ke basis pe jawab do:
                
#                 {pakshop_data}
                
#                 Agar jawab is data mein nahi hai to kaho:
#                 "Mujhe is baare mein pata nahi"
#                 roman Urdu mein jawab do."""
#             },
#             {
#                 "role": "user",
#                 "content": question
#             }
#         ]
#     )
#     return response.choices[0].message.content

# # Test karo
# print("Q: Delivery kitnay din may hogi?")
# print("A:", ask_pakshop("Delivery kitnay din may hogi?"))

# # %%
# questions = [
#     "Delivery kitnay din may hogi?",
#     "Return policy kya hai?",
#     "Order Tracking kaise karein?",
#     "Payment methods kya hain?",
# ]

# print("\nTesting multiple questions:")
# for q in questions:
#     print(f"Q: {q}")
#     print("A:", ask_pakshop(q))
#     print()

# # %%
# print("Testing unknown question:")
# unknown_question = "Kya aap international delivery karte hain?"
# print(f"Q: {unknown_question}")
# print("A:", ask_pakshop(unknown_question))



# # %%
# from groq import Groq
# import json

# query = "delivery kitne din mein hogi?"
# knowledge_base = ["Return policy: 7 din ke andar return kar sakte hain.",
#                   "Delivery: Lahore: 1-2 din, Karachi: 2-3 din"]

# for sentance in knowledge_base:
#     if any(word in sentance.lower() for word in query.lower().split()):
#         print("Found relevant information:", sentance)

# # %%
# import json
# from groq import Groq

# # 1. Initialize Client
# client = Groq(api_key="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")

# # 2. Knowledge Base (Chunks Data)
# KNOWLEDGE_BASE = [
#     {
#         "category": "return",
#         "content": "PakShop ki return policy 7 din ki hai. Original receipt aur unused item zaroori hai."
#     },
#     {
#         "category": "delivery",
#         "content": "Lahore mein 1-2 din, baki cities mein 3-5 din lagte hain. Rs. 2000 se upar order par delivery FREE hai."
#     },
#     {
#         "category": "payment",
#         "content": "Hum Cash on Delivery (COD), JazzCash, Easypaisa, aur Credit/Debit Card accept karte hain."
#     }
# ]

# # 3. Simple Retriever Function (Keyword-based Context Search)
# def retrieve_relevant_context(query):
#     query_lower = query.lower()
#     retrieved_chunks = []
    
#     for item in KNOWLEDGE_BASE:
#         # Check if query matches category or content keywords
#         if item["category"] in query_lower or any(word in item["content"].lower() for word in query_lower.split()):
#             retrieved_chunks.append(item["content"])
            
#     # Agar koi match na mile to saara context bhej do (Fallback)
#     if not retrieved_chunks:
#         retrieved_chunks = [item["content"] for item in KNOWLEDGE_BASE]
        
#     return "\n".join(retrieved_chunks)

# # 4. System Prompt Builder
# def build_system_prompt(context):
#     return f"""Tum PakShop ke ek smart Customer Support AI Assistant ho.

# KNOWLEDGE BASE:
# {context}

# INSTRUCTIONS:
# 1. Sirf upar diye gaye KNOWLEDGE BASE ke mutabiq jawab do.
# 2. Agar query ka jawab KNOWLEDGE BASE mein na ho, toh saaf kah do: "Mujhe is baare mein maloomat nahi hai."
# 3. Hamesha Roman Urdu mein chota aur to-the-point jawab do.
# 4. User ke sath pichli guftagu (Chat History) ko zehen mein rakhte hue jawab do."""

# # 5. RAG Chat Engine
# class RAGChatbot:
#     def __init__(self):
#         self.conversation_history = []

#     def chat(self, user_query):
#         # Step A: Relevant Context Retrieve Karein
#         context = retrieve_relevant_context(user_query)
        
#         # Step B: System Prompt Update Karein
#         system_message = {"role": "system", "content": build_system_prompt(context)}
        
#         # Step C: Messages Payload Prepare Karein
#         messages_payload = [system_message] + self.conversation_history + [{"role": "user", "content": user_query}]
        
#         # Step D: Groq API Call
#         response = client.chat.completions.create(
#             model="openai/gpt-oss-20b",
#             messages=messages_payload,
#             temperature=0.1
#         )
        
#         ai_response = response.choices[0].message.content
        
#         # Step E: Memory Update
#         self.conversation_history.append({"role": "user", "content": user_query})
#         self.conversation_history.append({"role": "assistant", "content": ai_response})
        
#         return ai_response

# # 6. Interactive Terminal Loop
# if __name__ == "__main__":
#     bot = RAGChatbot()
#     print("--- PakShop RAG Chatbot Started (Type 'exit' to quit) ---")
    
#     while True:
#         user_input = input("\nAap: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("Allah Hafiz!")
#             break
            
#         response = bot.chat(user_input)
#         print(f"PakShop Bot: {response}")

# # %%
# import json
# from groq import Groq

# client = Groq(api_key="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")

# KNOWLEDGE_BASE = [
#     {
#         "category": "return",
#         "content": "PakShop ki return policy 7 din ki hai. Original receipt aur unused item zaroori hai."
#     },
#     {
#         "category": "delivery",
#         "content": "Lahore mein 1-2 din, baki cities mein 3-5 din lagte hain. Rs. 2000 se upar order par delivery FREE hai."
#     },
#     {
#         "category": "payment",
#         "content": "Hum Cash on Delivery (COD), JazzCash, Easypaisa, aur Credit/Debit Card accept karte hain."
#     }
# ]

# # simple retriever function
# def retrieve_relevant_context(query):
#     query_lower = query.lower()
#     retrieved_chunks = []
    
#     for item in KNOWLEDGE_BASE:
#         if item["category"] in query_lower or any(word in item["content"].lower() for word in query_lower.split()):
#             retrieved_chunks.append(item["content"])
            
#     if not retrieved_chunks:
#         retrieved_chunks = [item["content"] for item in KNOWLEDGE_BASE]
        
#     return "\n".join(retrieved_chunks)
# # system prompt builder
# def build_system_prompt(context):
#     return f"""Tum PakShop ke ek smart Customer Support AI Assistant ho.
# KNOWLEDGE BASE:
# {context}
# Instructions:
# 1. Sirf upar diye gaye KNOWLEDGE BASE ke mutabiq jawab do
# 2. Agar query ka jawab KNOWLEDGE BASE mein na ho, toh saaf kah do: "Mujhe is baare mein maloomat nahi hai."
# 3. Hamesha Roman Urdu mein chota aur to-the-point jawab do.
# 4. User ke sath pichli guftagu (Chat History) ko zehen mein rakhte hue jawab do."""


# # RAG Chat Engine
# class RAGChatbot:
#     def __init__(self):
#         self.conversation_history = []

#     def chat(self, user_query):
#         context = retrieve_relevant_context(user_query)
#         system_message = {"role": "system", "content": build_system_prompt(context)}

#         messages_payload = [system_message] + self.conversation_history + [{"role": "user", "content": user_query}]

#         response = client.chat.completions.create(
#             model="openai/gpt-oss-20b", 
#             messages=messages_payload,
#             temperature=0.1
#         )

#         ai_response = response.choices[0].message.content
#         self.conversation_history.append({"role": "user", "content": user_query})
#         self.conversation_history.append({"role": "assistant", "content": ai_response})
#         return ai_response

# if __name__ == "__main__":
#     bot = RAGChatbot()
#     print("--- PakShop RAG Chatbot Started (Type 'exit' to quit) ---")
#     while True:
#         user_input = input("\nAap: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("Allah Hafiz!")
#             break
#         response = bot.chat(user_input)
#         print(f"PakShop Bot: {response}")
        
        



# %%
import json
from groq import Groq
import streamlit as st

client = Groq(api_key="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")

KNOWLEDGE_BASE = [
    {
        "category": "Python",
        "content": "Python Course: Duration 2 months, Fee Rs. 5000."
    },
    {
        "category": "Web Dev",
        "content": "Web Dev Course: Duration 3 months, Fee Rs. 8000."
    },
    {
        "category": "Refund",
        "content": "Refund Policy: 3 din ke andar 100% money back guarantee."
    }
]

def retrieve_relevant_context(query):
    query_lower = query.lower()
    retrieved_chunks = []
    
    for item in KNOWLEDGE_BASE:
        if item["category"].lower() in query_lower or any(word in item["content"].lower() for word in query_lower.split()):
            retrieved_chunks.append(item["content"])
            
    if not retrieved_chunks:
        return "Mujhe is baare mein maloomat nahi hai."
        
    return "\n".join(retrieved_chunks)

def build_system_prompt(context):
    return f"""Tum TechCourse Academy ke ek smart aur polite Customer Support AI Assistant ho.

KNOWLEDGE BASE:
{context}

INSTRUCTIONS:
1.User ke sawal ka jawab bilkul short, direct aur to-the-point (ziada se ziada 1-2 lines) mein do.
2. Agar user general gup-shup kare (jaise "hi", "hello", "kaise ho"), toh polite jawab do aur sath batao ke tum sirf Courses aur Refund Policy ke baare mein help kar sakte ho.
3. Jab user kisi course ya refund ke baare mein pooche, toh KNOWLEDGE BASE ke mutabiq Roman Urdu mein to-the-point jawab do.
4. Ye nahi btao k tum kya think karte ho ya tumhari capabilities kya hain. Sirf user ke sawal ka jawab do.ye na bolo k here is the information you requested. Sirf short aur polite jawab do. 
"Do not include any thinking process, reasoning, or internal thought tags like <think> in your response. Output ONLY the final answer."  
"""

# RAG Chat Engine
class RAGChatbot:
    def __init__(self):
        self.conversation_history = []

    def chat(self, user_query):
        context = retrieve_relevant_context(user_query)
        system_message = {"role": "system", "content": build_system_prompt(context)}

        messages_payload = [system_message] + self.conversation_history + [{"role": "user", "content": user_query}]

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b", 
            messages=messages_payload,
            temperature=0.1,
        )

        ai_response = response.choices[0].message.content

        self.conversation_history.append({"role": "user", "content": user_query})
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response

# --- SCRIPT KE NEECHE WALA PART (Streamlit UI) ---

st.set_page_config(page_title="PakShop AI", page_icon="🤖")
st.title("PakShop AI Assistant")

# Memory State Setup
if "bot" not in st.session_state:
    st.session_state.bot = RAGChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani Chat History Display Karna
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User Input Aur Bot Response Handle Karna
if user_query := st.chat_input("Apna sawal likhein..."):
    # User message screen par show karna
    st.chat_message("user").write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Bot reply fetch karke display karna
    bot_reply = st.session_state.bot.chat(user_query)
    st.chat_message("assistant").write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})