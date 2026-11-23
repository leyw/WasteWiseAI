import time, json

env = {}
with open('.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

api_key = env.get('AI_API_KEY', '')
model = "models/gemini-3-flash-preview"

from google import genai
from google.genai import types as genai_types

client = genai.Client(api_key=api_key)

# Baca gambar
with open('test_plastik.jpg', 'rb') as f:
    image_bytes = f.read()

prompt = """Analisis gambar ini. Kembalikan HANYA JSON:
{
  "waste_name": "nama objek",
  "category": "plastik",
  "material": "material",
  "description": "deskripsi singkat"
}"""

print(f'Testing vision with model: {model}')
start = time.time()
try:
    response = client.models.generate_content(
        model=model,
        contents=[
            genai_types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            prompt,
        ],
    )
    elapsed = time.time() - start
    print(f'OK in {elapsed:.1f}s')
    print(f'Response: {response.text[:300]}')
except Exception as e:
    elapsed = time.time() - start
    print(f'Error after {elapsed:.1f}s: {e}')
