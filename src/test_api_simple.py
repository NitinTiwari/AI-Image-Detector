import base64, requests

HF_API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/Falconsai/Falconsai-SD3-FakeImageDetection-0.1"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

image_path = r"c:/Users/hp/ProdAI/FakeImage/src/sample-80-1.png"
with open(image_path, "rb") as f:
    img_bytes = f.read()

b64 = base64.b64encode(img_bytes).decode('utf-8')
payload = {"inputs": b64}
response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)
print('Status code:', response.status_code)
print('Response:', response.text)
