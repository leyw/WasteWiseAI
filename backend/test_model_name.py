import time, sys

env = {}
with open('.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

api_key = env.get('AI_API_KEY', '')

from google import genai
client = genai.Client(api_key=api_key)

# Test berbagai nama model
models_to_test = [
    "models/gemini-2.5-flash",
    "gemini-flash-latest",
    "models/gemini-flash-latest",
]

for model in models_to_test:
    print(f'\nTesting model: {model}')
    start = time.time()
    try:
        response = client.models.generate_content(
            model=model,
            contents=['Balas HANYA: {"test":"ok"}']
        )
        elapsed = time.time() - start
        print(f'  OK in {elapsed:.1f}s — response: {response.text[:80]}')
        break
    except Exception as e:
        elapsed = time.time() - start
        print(f'  Error after {elapsed:.1f}s: {str(e)[:120]}')
