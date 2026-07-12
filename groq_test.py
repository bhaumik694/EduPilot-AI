from groq import Groq

# 🔴 PASTE YOUR KEY DIRECTLY HERE (no env)
client = Groq(api_key="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")

res = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "hello"}]
)

print(res.choices[0].message.content)