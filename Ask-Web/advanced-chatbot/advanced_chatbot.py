# Next-Level Website Chatbot with Advanced Features
# Enhanced with Image OCR, Voice Interaction, Persistent Storage & Advanced Scraping

import streamlit as st
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util
import torch
import requests
from urllib.parse import urljoin, urlparse
import time
import re
import os
import io
import base64
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from streamlit_webrtc import webrtc_streamer


# Advanced imports for new features
import chromadb
from chromadb.config import Settings
import easyocr
import pytesseract
from PIL import Image
import speech_recognition as sr
from gtts import gTTS
import tempfile

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="Advanced AI Website Chatbot", 
    page_icon="🤖", 
    layout="wide"
)

st.title("🚀 Advanced AI Website Chatbot")
st.markdown("**Next-level chatbot with Image OCR, Voice Interaction, Persistent Storage & Advanced Scraping**")

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "website_content" not in st.session_state:
    st.session_state.website_content = []
if "collection" not in st.session_state:
    st.session_state.collection = None
if "chroma_client" not in st.session_state:
    st.session_state.chroma_client = None
if "encoder" not in st.session_state:
    st.session_state.encoder = None
if "last_url" not in st.session_state:
    st.session_state.last_url = ""
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = False

class AdvancedWebsiteScraper:
    def __init__(self, use_gpu_ocr=True):
        self.setup_drivers()
        self.setup_ocr(use_gpu_ocr)
        
    def setup_drivers(self):
        """Setup multiple Chrome drivers for parallel scraping"""
        self.drivers = []
        self.max_drivers = 3  # Limit to prevent resource exhaustion
        
    def get_driver(self):
        """Get or create a Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-images")  # Skip images for faster loading
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.implicitly_wait(5)
            return driver
        except Exception as e:
            st.error(f"Error setting up Chrome driver: {e}")
            return None
    
    def setup_ocr(self, use_gpu=True):
        """Setup OCR engines"""
        self.use_gpu_ocr = use_gpu
        try:
            if use_gpu:
                # EasyOCR - better for GPU
                self.ocr_reader = easyocr.Reader(['en'])
                st.success("✅ EasyOCR (GPU) initialized")
            else:
                # Tesseract - better for CPU
                self.ocr_reader = None
                st.success("✅ Tesseract (CPU) ready")
        except Exception as e:
            st.warning(f"OCR setup warning: {e}")
            self.ocr_reader = None
    
    def extract_text_from_images(self, driver):
        """Extract text from images on the current page"""
        extracted_texts = []
        
        try:
            # Find all images on the page
            images = driver.find_elements(By.TAG_NAME, "img")
            
            for i, img in enumerate(images[:5]):  # Limit to first 5 images
                try:
                    # Get image src
                    img_src = img.get_attribute("src")
                    if not img_src or img_src.startswith("data:"):
                        continue
                    
                    # Download image
                    response = requests.get(img_src, timeout=10)
                    if response.status_code == 200:
                        # Convert to PIL Image
                        pil_img = Image.open(io.BytesIO(response.content))
                        
                        # Extract text using OCR
                        if self.use_gpu_ocr and self.ocr_reader:
                            # EasyOCR
                            results = self.ocr_reader.readtext(response.content)
                            text = " ".join([result[1] for result in results])
                        else:
                            # Tesseract
                            text = pytesseract.image_to_string(pil_img)
                        
                        if text.strip():
                            extracted_texts.append(f"Image {i+1}: {text.strip()}")
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            st.warning(f"Image OCR error: {e}")
            
        return extracted_texts
    
    def normalize_url(self, url):
        """Normalize URL by removing fragments and normalizing case"""
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc.lower()}{parsed.path}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        return normalized.rstrip('/')
    
    def is_same_domain(self, url1, url2):
        """Check if two URLs belong to the same domain"""
        domain1 = urlparse(url1).netloc.lower().replace('www.', '')
        domain2 = urlparse(url2).netloc.lower().replace('www.', '')
        return domain1 == domain2
    
    def is_valid_url(self, url):
        """Check if URL is valid for scraping"""
        if not url:
            return False
        
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
            
        # Skip certain file types
        skip_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.doc', '.docx', '.mp4', '.avi']
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return False
            
        return True
    
    def scrape_single_page(self, url, extract_images=True):
        """Scrape content from a single page with image OCR"""
        driver = self.get_driver()
        if not driver:
            return None
            
        try:
            driver.get(url)
            time.sleep(2)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header", "sidebar", "aside", "ads"]):
                element.decompose()
            
            # Extract title
            title = soup.title.string if soup.title else "No Title"
            
            # Extract main content
            content = soup.get_text()
            lines = (line.strip() for line in content.splitlines())
            content = ' '.join(line for line in lines if line)
            
            # Extract text from images if enabled
            image_texts = []
            if extract_images:
                image_texts = self.extract_text_from_images(driver)
            
            # Combine regular content and image text
            full_content = content
            if image_texts:
                full_content += "\n\nText from Images:\n" + "\n".join(image_texts)
            
            if len(full_content.strip()) > 100:
                return {
                    'url': url,
                    'title': title.strip(),
                    'content': full_content[:12000],  # Increased limit for image content
                    'image_count': len(image_texts)
                }
                
        except Exception as e:
            st.warning(f"Error scraping {url}: {e}")
        finally:
            driver.quit()
            
        return None
    
    def parallel_scrape_pages(self, urls, max_workers=3, extract_images=True):
        """Scrape multiple pages in parallel"""
        scraped_content = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit scraping jobs
            future_to_url = {
                executor.submit(self.scrape_single_page, url, extract_images): url 
                for url in urls
            }
            
            completed = 0
            total = len(urls)
            
            for future in as_completed(future_to_url):
                completed += 1
                url = future_to_url[future]
                
                status_text.text(f"Scraping page {completed}/{total}: {url}")
                progress_bar.progress(completed / total)
                
                try:
                    result = future.result()
                    if result:
                        scraped_content.append(result)
                except Exception as e:
                    st.warning(f"Error scraping {url}: {e}")
        
        progress_bar.empty()
        status_text.empty()
        
        return scraped_content
    
    def intelligent_url_discovery(self, base_url, max_pages=20):
        """Intelligent URL discovery with prioritization"""
        discovered_urls = set()
        priority_patterns = [
            '/about', '/services', '/products', '/blog', '/news', '/faq', 
            '/contact', '/help', '/docs', '/documentation', '/api'
        ]
        
        driver = self.get_driver()
        if not driver:
            return [base_url]
        
        try:
            driver.get(base_url)
            time.sleep(2)
            
            # Get all links
            links = driver.find_elements(By.TAG_NAME, "a")
            base_domain = urlparse(base_url).netloc.lower().replace('www.', '')
            
            prioritized_urls = []
            regular_urls = []
            
            for link in links:
                try:
                    href = link.get_attribute("href")
                    if not href:
                        continue
                    
                    absolute_url = urljoin(base_url, href)
                    normalized_url = self.normalize_url(absolute_url)
                    
                    if (self.is_valid_url(absolute_url) and 
                        self.is_same_domain(absolute_url, base_url) and
                        normalized_url not in discovered_urls):
                        
                        discovered_urls.add(normalized_url)
                        
                        # Prioritize URLs with important patterns
                        if any(pattern in normalized_url.lower() for pattern in priority_patterns):
                            prioritized_urls.append(absolute_url)
                        else:
                            regular_urls.append(absolute_url)
                            
                except Exception:
                    continue
            
            # Combine prioritized and regular URLs
            all_urls = [base_url] + prioritized_urls + regular_urls
            return all_urls[:max_pages]
            
        except Exception as e:
            st.warning(f"Error discovering URLs: {e}")
            return [base_url]
        finally:
            driver.quit()

class VoiceInteraction:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def speech_to_text(self, audio_data):
        """Convert speech to text"""
        try:
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            return f"Could not request results; {e}"
    
    def text_to_speech(self, text, lang='en'):
        """Convert text to speech and return as audio bytes"""
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                
                # Read the file and return bytes
                with open(tmp_file.name, 'rb') as f:
                    audio_bytes = f.read()
                
                # Clean up
                os.unlink(tmp_file.name)
                
                return audio_bytes
        except Exception as e:
            st.error(f"Text-to-speech error: {e}")
            return None

class PersistentVectorStorage:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self.encoder = None
        
    def initialize_storage(self):
        """Initialize ChromaDB persistent storage"""
        try:
            # Create ChromaDB client with persistence
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            
            # Initialize sentence transformer
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            
            st.success(f"✅ Persistent storage initialized at {self.persist_directory}")
            return True
            
        except Exception as e:
            st.error(f"Error initializing storage: {e}")
            return False
    
    def create_or_get_collection(self, collection_name="website_content"):
        """Create or get existing collection"""
        try:
            # Try to get existing collection first
            try:
                self.collection = self.client.get_collection(collection_name)
                st.info(f"📚 Retrieved existing collection: {collection_name}")
            except:
                # Create new collection if doesn't exist
                self.collection = self.client.create_collection(
                    name=collection_name,
                    metadata={"description": "Website content with OCR text"}
                )
                st.success(f"🆕 Created new collection: {collection_name}")
            
            return True
        except Exception as e:
            st.error(f"Error with collection: {e}")
            return False
    
    def store_content(self, content_list, website_url):
        """Store scraped content in ChromaDB"""
        if not self.collection or not self.encoder:
            return False
        
        try:
            documents = []
            metadatas = []
            ids = []
            
            for i, item in enumerate(content_list):
                # Create chunks for better search
                content = item['content']
                chunk_size = 800
                words = content.split()
                
                for j, chunk_start in enumerate(range(0, len(words), chunk_size)):
                    chunk = ' '.join(words[chunk_start:chunk_start + chunk_size])
                    
                    if len(chunk.strip()) > 100:
                        doc_id = f"{website_url}_{i}_{j}_{int(time.time())}"
                        
                        documents.append(chunk)
                        metadatas.append({
                            'url': item['url'],
                            'title': item['title'],
                            'website': website_url,
                            'chunk_index': j,
                            'image_count': item.get('image_count', 0),
                            'timestamp': time.time()
                        })
                        ids.append(doc_id)
            
            if documents:
                # Store in ChromaDB
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                
                st.success(f"💾 Stored {len(documents)} content chunks in persistent database")
                return True
            
        except Exception as e:
            st.error(f"Error storing content: {e}")
            return False
    
    def search_content(self, query, n_results=5):
        """Search stored content"""
        if not self.collection:
            return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            search_results = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    search_results.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if results.get('distances') else 0
                    })
            
            return search_results
            
        except Exception as e:
            st.error(f"Error searching content: {e}")
            return []
    
    def get_collection_stats(self):
        """Get statistics about stored content"""
        if not self.collection:
            return None
        
        try:
            count = self.collection.count()
            return {
                'total_chunks': count,
                'collection_name': self.collection.name
            }
        except Exception as e:
            st.error(f"Error getting stats: {e}")
            return None

def generate_response_with_gemini(query, relevant_content, api_key):
    """Generate response using Gemini AI"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prepare context from relevant content
        context = ""
        for i, item in enumerate(relevant_content):
            metadata = item.get('metadata', {})
            content = item.get('content', '')
            context += f"\n\nSource {i+1} (from {metadata.get('title', 'Unknown')}):\n{content}"
        
        prompt = f"""Based on the following website content (including text extracted from images), please answer the user's question accurately and helpfully.

Website Content:
{context}

User Question: {query}

Instructions:
1. Answer based only on the provided website content
2. If the information isn't available in the content, say so
3. Include relevant source references when possible
4. Be concise but comprehensive
5. If you reference specific information, mention which source it came from

Answer:"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error generating response: {e}"

def autoplay_audio(audio_bytes):
    """Create HTML for autoplaying audio"""
    b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    return audio_html

# Main Application
def main():
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Advanced Configuration")
        
        # API Key
        gemini_api_key = st.text_input("Gemini API Key", type="password", 
                                      help="Get your API key from Google AI Studio")
        
        # Website URL
        website_url = st.text_input("Website URL", 
                                   help="Enter the website URL to scrape")
        
        # Advanced settings
        st.subheader("🔧 Scraping Settings")
        max_pages = st.slider("Max pages to scrape", 1, 50, 15)
        max_workers = st.slider("Parallel workers", 1, 5, 3)
        extract_images = st.checkbox("Extract text from images (OCR)", value=True)
        use_gpu_ocr = st.checkbox("Use GPU for OCR (EasyOCR)", value=True)
        
        # Voice settings
        st.subheader("🎙️ Voice Settings")
        voice_enabled = st.checkbox("Enable voice responses", value=False)
        
        # Storage settings
        st.subheader("💾 Storage Settings")
        collection_name = st.text_input("Collection name", value="website_content")
        
        # Initialize storage
        if "storage" not in st.session_state:
            st.session_state.storage = PersistentVectorStorage()
            if st.session_state.storage.initialize_storage():
                st.session_state.storage.create_or_get_collection(collection_name)
        
        # Display storage stats
        if st.session_state.storage and st.session_state.storage.collection:
            stats = st.session_state.storage.get_collection_stats()
            if stats:
                st.metric("Stored chunks", stats['total_chunks'])
        
        # Scraping button
        if st.button("🚀 Start Advanced Scraping", disabled=not (website_url and gemini_api_key)):
            if website_url != st.session_state.last_url:
                with st.spinner("Advanced scraping in progress..."):
                    # Initialize scraper
                    scraper = AdvancedWebsiteScraper(use_gpu_ocr=use_gpu_ocr)
                    
                    # Discover URLs intelligently
                    st.info("🔍 Discovering URLs...")
                    urls = scraper.intelligent_url_discovery(website_url, max_pages)
                    
                    # Parallel scraping with OCR
                    st.info(f"🔄 Scraping {len(urls)} pages with {max_workers} workers...")
                    content = scraper.parallel_scrape_pages(urls, max_workers, extract_images)
                    
                    if content:
                        st.session_state.website_content = content
                        st.session_state.last_url = website_url
                        
                        # Store in persistent database
                        if st.session_state.storage:
                            st.session_state.storage.store_content(content, website_url)
                        
                        # Show success metrics
                        image_count = sum(item.get('image_count', 0) for item in content)
                        st.success(f"✅ Scraped {len(content)} pages with {image_count} images processed!")
                        st.session_state.messages = []  # Clear conversation
                    else:
                        st.error("No content scraped. Please check the URL.")
        
        
        #new 
        # Voice interaction
        if voice_enabled:
            st.subheader("🎤 Real-Time Voice Input")
            
            # Initialize voice-related session states
            if "recording" not in st.session_state:
                st.session_state.recording = False
            if "listening_for_voice" not in st.session_state:
                st.session_state.listening_for_voice = False
            
            # Create columns for better layout
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Voice recording button
                if st.button("🎤 Ask Question by Voice", type="primary", key="voice_btn"):
                    if st.session_state.storage:
                        st.session_state.listening_for_voice = True
                    else:
                        st.error("Please scrape a website first!")
            
            with col2:
                if st.session_state.storage:
                    st.info("💡 Click the button and speak your question")
                else:
                    st.warning("⚠️ Scrape a website first to enable voice queries")
            
            # Process voice input when button is clicked
            if st.session_state.listening_for_voice and st.session_state.storage:
                try:
                    # Initialize voice interaction
                    voice = VoiceInteraction()
                    
                    # Show listening indicator
                    with st.spinner("🎤 Listening... Please speak your question now!"):
                        # Record audio with enhanced microphone setup
                        with voice.microphone as source:
                            # Adjust for ambient noise
                            voice.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                            
                            # Listen for speech with reasonable timeout
                            try:
                                audio_data = voice.recognizer.listen(
                                    source, 
                                    timeout=2,  # Wait 2 seconds for speech to start
                                    phrase_time_limit=10  # Allow up to 10 seconds of speech
                                )
                                
                                # Convert speech to text
                                with st.spinner("🧠 Converting speech to text..."):
                                    text_query = voice.recognizer.recognize_google(audio_data)
                                
                                if text_query and len(text_query.strip()) > 0:
                                    st.success(f"🎤 **You asked:** {text_query}")
                                    
                                    # Process the voice query exactly like a text query
                                    with st.spinner("🔍 Searching content and generating response..."):
                                        # Search stored content
                                        relevant_content = st.session_state.storage.search_content(text_query, n_results=5)
                                        
                                        if relevant_content:
                                            # Generate response using Gemini
                                            response = generate_response_with_gemini(text_query, relevant_content, gemini_api_key)
                                            
                                            # Display the response
                                            st.write("🤖 **AI Response:**")
                                            st.write(response)
                                            
                                            # Add to chat history (so it appears in the chat below)
                                            st.session_state.messages.append({
                                                "role": "user", 
                                                "content": f"🎤 {text_query}"
                                            })
                                            st.session_state.messages.append({
                                                "role": "assistant", 
                                                "content": response
                                            })
                                            
                                            # Generate and play voice response
                                            with st.spinner("🔊 Generating voice response..."):
                                                audio_bytes = voice.text_to_speech(response)
                                                if audio_bytes:
                                                    st.audio(audio_bytes, format="audio/mp3", autoplay=False)
                                                    st.success("🔊 Voice response generated! Click play above to hear it.")
                                            
                                            # Show sources used
                                            with st.expander("📚 Sources used for your voice query"):
                                                for i, item in enumerate(relevant_content):
                                                    metadata = item.get('metadata', {})
                                                    st.write(f"**Source {i+1}:** {metadata.get('title', 'Unknown')}")
                                                    st.caption(
                                                        f"📍 URL: {metadata.get('url', 'Unknown')} | "
                                                        f"🖼️ Images: {metadata.get('image_count', 0)} | "
                                                        f"📊 Relevance: {1 - item.get('distance', 0):.2f}"
                                                    )
                                                    st.write(item.get('content', '')[:300] + "...")
                                                    st.divider()
                                        else:
                                            st.warning("❌ No relevant content found for your voice query. Make sure the website contains information related to your question.")
                                else:
                                    st.error("❌ No speech detected or speech was unclear. Please try again.")
                                    
                            except sr.WaitTimeoutError:
                                st.error("⏰ No speech detected within 2 seconds. Please click the button and speak immediately.")
                            except sr.UnknownValueError:
                                st.error("❌ Could not understand the speech. Please speak more clearly and try again.")
                            except sr.RequestError as e:
                                st.error(f"❌ Speech recognition service error: {e}")
                                
                except Exception as e:
                    st.error(f"❌ Voice processing error: {e}")
                finally:
                    # Reset the listening flag
                    st.session_state.listening_for_voice = False
            
            # Instructions for voice input
            with st.expander("📖 Voice Input Instructions"):
                st.markdown("""
                **How to use Voice Input:**
                1. 🌐 **First scrape a website** using the sidebar
                2. ✅ **Enable "Enable voice responses"** in the sidebar  
                3. 🎤 **Click "Ask Question by Voice"** button above
                4. 🗣️ **Speak immediately** after clicking (you have 2 seconds to start)
                5. 🕒 **Speak your question clearly** (up to 10 seconds)
                6. ⏳ **Wait for processing** - speech converts to text automatically
                7. 🤖 **Get AI response** with voice playback and source citations
                
                **Tips for better recognition:**
                - Speak clearly and at normal pace
                - Minimize background noise
                - Ask specific questions about the scraped website content
                - Wait for the "Listening..." message before speaking
                """)
            
            # Quick TTS test
            with st.expander("🔊 Test Text-to-Speech"):
                test_text = st.text_area(
                    "Test voice synthesis:", 
                    placeholder="Enter text to convert to speech...",
                    height=100
                )
                if st.button("🔊 Generate Speech") and test_text:
                    voice = VoiceInteraction()
                    with st.spinner("Creating audio..."):
                        audio_bytes = voice.text_to_speech(test_text)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
                            st.success("✅ Audio generated successfully!")
                        else:
                            st.error("❌ Failed to generate audio")
            
            st.divider()
        # Display scraped content info
        if st.session_state.website_content:
            st.success(f"📄 {len(st.session_state.website_content)} pages loaded")
            
            with st.expander("📋 View scraped content"):
                for item in st.session_state.website_content:
                    st.write(f"**{item['title']}**")
                    st.caption(f"URL: {item['url']} | Images: {item.get('image_count', 0)}")
                    st.write(item['content'][:300] + "...")
                    st.divider()
    
    # Main chat interface
    st.header("💬 Advanced AI Chat")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask anything about the website content...", 
                              disabled=not (st.session_state.storage and gemini_api_key)):
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching stored content and generating response..."):
                if st.session_state.storage and st.session_state.storage.collection:
                    # Search stored content
                    relevant_content = st.session_state.storage.search_content(prompt, n_results=5)
                    
                    if relevant_content:
                        # Generate response
                        response = generate_response_with_gemini(prompt, relevant_content, gemini_api_key)
                        st.write(response)
                        
                        # Generate voice response if enabled
                        if voice_enabled:
                            voice = VoiceInteraction()
                            audio_bytes = voice.text_to_speech(response)
                            if audio_bytes:
                                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                        
                        # Show sources
                        with st.expander("📚 Sources used"):
                            for i, item in enumerate(relevant_content):
                                metadata = item.get('metadata', {})
                                st.write(f"**Source {i+1}:** {metadata.get('title', 'Unknown')}")
                                st.caption(f"URL: {metadata.get('url', 'Unknown')} | "
                                         f"Images: {metadata.get('image_count', 0)} | "
                                         f"Relevance: {1 - item.get('distance', 0):.2f}")
                                st.write(item.get('content', '')[:300] + "...")
                                st.divider()
                        
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        error_msg = "No relevant content found for your query."
                        st.write(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                else:
                    error_msg = "Please scrape a website first or check your storage connection."
                    st.write(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Instructions
    if not st.session_state.website_content:
        st.info("""
        ### 🚀 Advanced Features:
        
        **🔥 Image OCR**: Automatically extracts text from images on websites
        **🎤 Voice Interaction**: Talk to your chatbot and get voice responses  
        **💾 Persistent Storage**: Content saved permanently with ChromaDB
        **⚡ Parallel Scraping**: Fast scraping with multiple workers
        **🎯 Smart URL Discovery**: Intelligently finds important pages
        
        **How to use:**
        1. Enter your Gemini API Key
        2. Configure scraping settings (OCR, workers, etc.)
        3. Enter website URL and start advanced scraping
        4. Enable voice features for hands-free interaction
        5. Chat with your content - everything is stored permanently!
        """)

if __name__ == "__main__":
    main()