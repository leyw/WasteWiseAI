import sys

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

print('Semua model yang tersedia:')
for m in client.models.list():
    name = getattr(m, 'name', str(m))
    print(' ', name)
