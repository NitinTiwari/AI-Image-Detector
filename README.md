# AI vs Real Image Detector

A Streamlit web app that detects whether an uploaded image is AI‑generated or a real photograph using **Sightengine's `genai` model**.

---

## ✨ Features
- 📤 Upload any JPG/PNG image (or use the sample image).  
- 🔍 Extracts EXIF metadata when available.  
- 🧠 Calls Sightengine API to get an `ai_generated` confidence score.  
- ✅ Shows a friendly verdict: "Likely AI‑generated" or "Likely Real Image" with a confidence percentage displayed inside a blue badge.  
- 🚫 No raw JSON is shown to the user – only a clean, styled UI.

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-image-detector.git
   cd ai-image-detector
   ```
2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # on Windows
   pip install -r requirements.txt
   ```
3. **Add your Sightengine credentials**
   - Create a file named `.env` in the project root:
   ```dotenv
   SIGHTENGINE_USER=YOUR_USER_ID
   SIGHTENGINE_SECRET=YOUR_API_SECRET
   ```
   - Or, if you deploy to Streamlit Cloud, add these keys under **Settings → Secrets**.

---

## 🚀 Running locally
```bash
streamlit run src/app.py
```
Open the URL shown in the terminal (usually `http://localhost:8501`).

---

## 📸 Usage guide
1. Click **"Choose an image"** and select a JPG/PNG file, or enable the sample image checkbox.
2. Press **"Analyze Image"**.
3. The app will:
   - Upload the image to Sightengine.
   - Retrieve the `ai_generated` confidence (0‑1).
   - Display a verdict with a blue badge containing the confidence percentage.
   - Show any camera EXIF data if present.

---

## 🛠️ Technical details
- **Core stack**: Python, Streamlit, Requests, Pillow.
- **API call** (`src/app.py`):
  ```python
  def query_sightengine(image_path, api_user, api_secret):
      params = {"models": "genai", "api_user": api_user, "api_secret": api_secret}
      with open(image_path, "rb") as f:
          files = {"media": f}
          r = requests.post("https://api.sightengine.com/1.0/check.json", files=files, data=params)
      return r.json()
  ```
- The confidence is extracted from `response["type"]["ai_generated"]` (or older formats).
- The UI renders the verdict using `st.markdown` with an inline styled `<span>` for the blue badge.

---

## 📂 Project structure
```
ai-image-detector/
│
├─ src/                # Streamlit app source
│   ├─ app.py          # Main application
│   ├─ test_api_simple.py  # Simple API test script
│   └─ fakeimage/__init__.py
│
├─ .env                # (not committed) environment variables
├─ requirements.txt    # Python dependencies
└─ README.md           # THIS FILE
```

---

## ☁️ Deployment to Streamlit Cloud
1. Push the repository to GitHub.
2. In Streamlit Cloud, *New app* → connect the repo and set the **Main file path** to `src/app.py`.
3. Add the two secrets (`SIGHTENGINE_USER` and `SIGHTENGINE_SECRET`) under **Settings → Secrets**.
4. Deploy – Streamlit Cloud will install the packages from `requirements.txt` (including `python-dotenv`).

---

## 📄 License
This project is licensed under the MIT License – see the `LICENSE` file for details.

---

## 🙏 Acknowledgments
- **Sightengine** – for providing the AI‑generated detection API.
- **Streamlit** – for making rapid UI prototyping effortless.
- **OpenAI** – for guidance and code assistance.

---

*Happy detecting!*
