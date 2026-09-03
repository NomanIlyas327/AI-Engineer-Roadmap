import gradio as gr
from groq import Groq

client = Groq(api_key="")

# PakShop knowledge base
knowledge = """
PAKSHOP POLICIES:

1. RETURN POLICY:
   - 7 din ke andar return kar sakte hain
   - Product original condition mein hona chahiye

2. DELIVERY:
   - Lahore: 1-2 din
   - Karachi: 2-3 din
   - Islamabad: 2-3 din
   - Free delivery Rs. 2000 se upar

3. PAYMENT:
   - Cash on Delivery
   - JazzCash
   - Easypaisa

4. CUSTOMER SERVICE:
   - Phone: 0300-1234567
   - Hours: 9am-9pm
"""

def chat(message, history):
    messages = [
        {
            "role": "system",
            "content": f"""Tum PakShop ka AI assistant ho.
            Sirf is data se jawab do:
            {knowledge}
            Urdu mein jawab do. Polite raho."""
        }
    ]
    
    # History add karo
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    
    messages.append({"role": "user", "content": message})
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )
    
    return response.choices[0].message.content

# Gradio UI
demo = gr.ChatInterface(
    fn=chat,
    title="🛍️ PakShop AI Assistant",
    description="PakShop ka AI chatbot — Urdu mein sawal karein!",
    examples=[
        "Return policy kya hai?",
        "Delivery kitne din mein hogi?",
        "Payment methods kya hain?"
    ]
)

demo.launch()