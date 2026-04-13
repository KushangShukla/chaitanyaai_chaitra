def business_explanation_prompt(question):
    return f"""### Instruction:
You are an AI business intelligence assistant. 

Answer the following business question clearly and professionally.

Question:
{question}

### Response:
"""

def rag_prompt(context,question):
    return f"""### Instruction:
You are an AI business analyst.

Use ONLY the information provided in the context.

If the context is insufficient, say that more data is required.

Context:
{context}

Question:
{question}

Provide a concise and professional explanation.

### Response:    
"""

def ml_prediction_explanation_prompt(prediction,features):
    return f"""### Instruction:
You are an AI system explaining a machine learning prediction.

Prediction:
{prediction}

Key Features:
{features}

Explain in clear business language why this prediction occured.

### Response:
"""
