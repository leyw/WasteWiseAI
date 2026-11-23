import os, time, sys

env = {}
with open('.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

api_key = env.get('AI_API_KEY', '')
model = env.get('GEMINI_MODEL', 'gemini-2.5-flash')

print(f'Testing Gemini API connection...')
print(f'Model: {model}')

from google import genai
client = genai.Client(api_key=api_key)

start = time.time()
try:
    response = client.models.generate_content(
        model=model,
        contents=['Balas HANYA dengan JSON: {"test":"ok"}']
    )
    elapsed = time.time() - start
    print(f'Connection OK in {elapsed:.1f}s')
    print(f'Response: {response.text[:200]}')
except Exception as e:
    elapsed = time.time() - start
    print(f'Error after {elapsed:.1f}s: {type(e).__name__}: {e}')
    sys.exit(1)
