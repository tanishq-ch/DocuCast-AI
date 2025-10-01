# AI Podcast Creator 🎙️✨

**Transform any PDF or text document into a dynamic, multi-speaker podcast using the power of generative AI.**

This full-stack web application provides a seamless user experience for converting static text into engaging audio conversations. Simply upload your file, and let our AI pipeline handle the text extraction, script generation, and high-quality voice synthesis.

---

## ✨ Core Features

*   **Secure User Authentication:** Full user registration and login system to manage personal podcast libraries.
*   **Flexible File Uploads:** Supports both `.pdf` and `.txt` file formats.
*   **Intelligent Text Extraction:** Automatically parses uploaded documents to extract clean, readable text.
*   **AI-Powered Script Generation:** Leverages the **Google Gemini API** to analyze the source text and generate a natural, two-speaker (Host & Expert) podcast script.
*   **High-Quality Text-to-Speech:** Uses the lightweight and efficient **KittenTTS** model to generate clear, human-like voices directly on the CPU.
*   **Dynamic Audio Creation:**
    *   Splits long paragraphs into sentences for robust and natural-sounding audio generation.
    *   Assigns distinct voices to the Host and Expert roles.
    *   Stitches individual audio clips into a final `.mp3` podcast file.
*   **User Dashboard & History:**
    *   Displays a paginated history of all generated podcasts with their status (Completed, Failed).
    *   Provides secure download links for completed audio files.
    *   Allows users to delete old or failed entries to manage their history.
*   **Professional UI/UX:** A modern, responsive, dark-mode interface built for a great user experience, complete with animations and user feedback.

---

## 🛠️ Technology Stack

This project integrates a variety of modern technologies to create a complete, end-to-end application.

*   **Backend:**
    *   **Framework:** Flask
    *   **Database:** SQLAlchemy ORM with SQLite
    *   **Authentication:** Flask-Login, Flask-Bcrypt
    *   **Migrations:** Flask-Migrate
    *   **Forms:** Flask-WTF

*   **AI & Machine Learning:**
    *   **Language Model (Scripting):** Google Gemini API (`google-generativeai`)
    *   **Text-to-Speech (Voicing):** KittenTTS (`kittentts`)
    *   **PDF Parsing:** PyMuPDF
    *   **Audio Manipulation:** pydub
    *   **Sentence Splitting:** NLTK (Natural Language Toolkit)
    *   **ML Framework:** PyTorch

*   **Frontend:**
    *   **HTML Templating:** Jinja2
    *   **Styling:** Custom CSS (with Pico.css as a base)
    *   **Icons:** Font Awesome
    *   **JavaScript:** Vanilla JS for UI enhancements.

---

## ⚙️ Local Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

*   Python 3.10+
*   Git

### 2. Clone the Repository

Clone the project to your local machine.
```bash
git clone https://github.com/tanishq-ch/AI-PDF---To---Podcast-Creator.git
cd AI-Podcast-Creator
```

### 3. Set Up the Environment

Create a Python virtual environment and activate it.

*   **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

*   **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 4. Install Dependencies

Install all the required packages from the `requirements.txt` file. This command uses an extra index for the specific PyTorch version needed.
```bash
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
```

### 5. Configure Environment Variables

Create a `.env` file in the root of the project and add your secret keys.

```env
# Generate a new secret key for Flask sessions
SECRET_KEY='a_very_long_random_string'

# Add your Google Gemini API Key
GEMINI_API_KEY='your_google_gemini_api_key_here'
```

### 6. Set Up the Database

Initialize and upgrade the database to create the necessary tables.
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
*(Note: If the `migrations` folder already exists, you can skip `flask db init`.)*

### 7. Run the Application

Launch the Flask development server.
```bash
flask run
```
The application will be available at `http://127.0.0.1:5000`.

---

## 🚀 How It Works: The AI Pipeline

1.  **Upload:** A user uploads a PDF or TXT file.
2.  **Text Extraction:** `PyMuPDF` reads the file and extracts all text content.
3.  **Script Generation:** The extracted text is sent to the **Gemini API** with a carefully crafted prompt, asking it to create a conversational script between a "Host" and an "Expert".
4.  **Sentence Splitting:** The generated script is broken down into individual sentences using `NLTK` to ensure the TTS engine receives manageable chunks of text.
5.  **Voice Synthesis:** For each sentence, **KittenTTS** generates a `.wav` audio clip using a different pre-defined voice for the Host and the Expert.
6.  **Audio Assembly:** `pydub` stitches all the individual `.wav` clips together, adding short pauses between them, and exports the final product as a single `.mp3` file.
7.  **Completion:** The database is updated with the "Completed" status and the path to the final `.mp3` file, which the user can then download.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
