import streamlit as st
from gtts import gTTS
from io import BytesIO

# Ensure the environment has streamlit and gtts installed
# Run in terminal: pip install streamlit gtts

def text_to_speech(text, lang='en', slow=False):
    """Convert text to speech using gTTS and return an MP3 file-like object."""
    try:
        tts = gTTS(text=text, lang=lang, slow=slow)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

# Streamlit UI Configuration
st.set_page_config(
    page_title="Text to Speech App",
    page_icon="🗣️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Header
st.title("🗣️ Text to Speech Converter")
st.markdown("""
Convert your text into speech in **English** or **Tamil**.  
Type your text, choose a language, and listen or download the audio instantly!
""")

# User Input
text = st.text_area(
    "Enter the text you want to convert:",
    height=150,
    placeholder="Type something like 'Hello, world!' or 'வணக்கம்! எப்படி இருக்கீங்க?'"
)

lang_options = [("English", "en"), ("Tamil", "ta")]
lang = st.selectbox(
    "Choose Language",
    options=lang_options,
    format_func=lambda x: x[0]
)

slow = st.toggle("Speak Slowly", value=False)

# Convert Button
if st.button("🔊 Convert to Speech", use_container_width=True):
    if not text.strip():
        st.warning("⚠️ Please enter some text to convert.")
    else:
        with st.spinner("Generating speech..."):
            mp3_fp = text_to_speech(text=text, lang=lang[1], slow=slow)
            if mp3_fp:
                st.success("✅ Speech is ready!")
                
                # Display audio player
                st.audio(mp3_fp, format="audio/mp3", start_time=0)
                
                # Reset buffer for download
                mp3_fp.seek(0)
                st.download_button(
                    label="⬇️ Download MP3",
                    data=mp3_fp,
                    file_name="tts_output.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )

# Footer
st.markdown("---")
st.markdown("Built by SHA using Streamlit and gTTS | Supports English and Tamil")