from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# System mein filhal balance 10,000 rupees hai
user_balance = 10000

# 1. Validation Rule: Cash nikalne ke liye amount ka number (int) hona lazmi hai
class WithdrawRequest(BaseModel):
    amount: int

# 2. GET Request: Balance Check Karna
@app.get("/check-balance")
def check_balance():
    return {"current_balance": user_balance}

# 3. POST Request: Cash Withdraw Karna
@app.post("/withdraw")
def withdraw_money(data: WithdrawRequest):
    global user_balance
    
    # Validation Check: Kya account mein itne paise hain?
    if data.amount > user_balance:
        return {"error": "Inssufficient balance!"}
    
    # Balance update karna
    user_balance = user_balance - data.amount
    
    return {
        "message": f"{data.amount} rupees nikal liye gaye hain.",
        "remaining_balance": user_balance
    }