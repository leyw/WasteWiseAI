import time

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

# Semua kandidat model yang mungkin mendukung vision
candidates = [
    "models/gemini-flash-latest",
    "models/gemini-pro-latest",
    "models/gemini-2.5-flash-lite",
    "models/gemini-2.5-flash-image",
    "models/gemini-3-flash-preview",
    "models/gemini-3.1-flash-lite",
    "models/gemini-3.1-flash-image",
    "models/gemini-3.1-flash-lite-image",
]

working = None
for model in candidates:
    print(f'Testing: {model}')
    start = time.time()
    try:
        response = client.models.generate_content(
            model=model,
            contents=['Balas HANYA: {"test":"ok"}']
        )
        elapsed = time.time() - start
        print(f'  WORKS in {elapsed:.1f}s: {response.text[:60]}')
        working = model
        break
    except Exception as e:
        elapsed = time.time() - start
        msg = str(e)[:100]
        print(f'  Failed after {elapsed:.1f}s: {msg}')

if working:
    print(f'\nModel yang berfungsi: {working}')
else:
    print('\nTidak ada model yang berfungsi saat ini.')
