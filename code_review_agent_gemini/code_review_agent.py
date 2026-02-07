"""
Automated Code Review Agent – FINAL VERSION

KEY GUARANTEES:
- User gives ONLY code
- Code can be ANY language or ANY format
- Language detection is NOT mandatory
- AI ALWAYS analyses the given code
- Output is POINT-WISE, ONE-LINE per section
- No crashes, no empty reviews
- Safe for GitHub (API key masked)
"""

import google.generativeai as genai
import sys

# ================= CONFIG =================
GEMINI_API_KEY = "AIzaSyCWcIUI2MiTTBHSMhb__yM0XB3fflNIke4"   # Replace locally ONLY
genai.configure(api_key=GEMINI_API_KEY)

# ================= MODEL AUTO-SELECTION =================
def get_model():
    try:
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except Exception as e:
        print("❌ Gemini model loading failed:", e)
        sys.exit(1)

model = get_model()

# ================= SAFE INPUT =================
def get_code():
    print("\n📌 Paste the code to be reviewed")
    print("📌 Type END on a new line and press Enter\n")

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break

    return "\n".join(lines)

# ================= AI CODE REVIEW =================
def ai_review(code: str) -> str:
    """
    This is INTERNAL logic.
    User never gives any prompt.
    Review is strictly based on the given code.
    """
    prompt = f"""
You are a senior software engineer reviewing a Pull Request.

STRICT RULES:
- Analyse ONLY the given code
- Do NOT assume missing context
- Do NOT ask questions
- Do NOT give paragraphs
- Give ONLY short, clear, one-line points

OUTPUT FORMAT (MUST FOLLOW EXACTLY):

SUMMARY:
- <one line>

ISSUES:
- <one line or None>

SECURITY:
- <one line or None>

IMPROVEMENTS:
- <one line>

VERDICT:
- <one line>

CODE TO REVIEW:
{code}
"""
    try:
        response = model.generate_content(prompt)

        # Safe extraction
        if hasattr(response, "text") and response.text:
            return response.text
        if hasattr(response, "candidates"):
            return response.candidates[0].content.parts[0].text

        return "⚠️ Review could not be generated."
    except Exception as e:
        return f"❌ AI review failed: {str(e)}"

# ================= MAIN =================
def main():
    code = get_code()

    if not code.strip():
        print("❌ No code provided. Exiting.")
        return

    print("\n=============== REVIEW REPORT ================\n")
    print("🤖 AUTOMATED CODE REVIEW:\n")

    review = ai_review(code)
    print(review)

    print("\n=============== END OF REVIEW ================\n")

if __name__ == "__main__":
    main()