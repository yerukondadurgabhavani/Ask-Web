# 🚀 Advanced AI Website Chatbot

## 📋 Project Overview

The **Advanced AI Website Chatbot** is a next-generation intelligent assistant that transforms any website into an interactive knowledge base. Using cutting-edge AI technologies, it can scrape websites, extract text from images, understand voice commands, and provide intelligent responses about the website's content.

### 🌟 Key Features

- **🕷️ Intelligent Web Scraping**: Advanced parallel scraping with smart URL discovery
- **🖼️ OCR Text Extraction**: Extract text from images using EasyOCR/Tesseract
- **🎤 Voice Interaction**: Speech-to-text input and text-to-speech responses
- **💾 Persistent Storage**: ChromaDB vector database for semantic search
- **🤖 AI-Powered Responses**: Google Gemini integration for intelligent answers
- **⚡ Real-time Processing**: Fast parallel processing with progress tracking
- **📊 Source Attribution**: Complete traceability of information sources

### 🎯 Use Cases

- **Enterprise Documentation**: Query company websites and documentation
- **Research Assistant**: Extract information from academic and technical sites
- **Customer Support**: Answer questions about products and services
- **Competitive Analysis**: Analyze competitor websites and offerings
- **Educational Tool**: Interactive learning from educational websites

---

## 🖥️ System Requirements

### Minimum Requirements
- **Python**: 3.9 or higher (3.11 recommended)
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: Stable connection for API calls and web scraping

### Supported Operating Systems
- ✅ **macOS**: 10.15+ (Intel and Apple Silicon)
- ✅ **Windows**: 10/11 (64-bit)
- ✅ **Linux**: Ubuntu 18.04+, Debian 10+, CentOS 7+

---

# 📦 Installation Guide

## 🍎 macOS Installation

### Step 1: Install Homebrew (if not installed)
```bash
# Install Homebrew package manager
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python 3.11
```bash
# Install Python 3.11
brew install python@3.11

# Verify installation
python3.11 --version
```

### Step 3: Install System Dependencies
```bash
# Install audio dependencies
brew install portaudio

# Install OCR dependencies
brew install tesseract

# Optional: Install FFmpeg for better audio processing
brew install ffmpeg
```

### Step 4: Install Google Chrome
```bash
# Install Chrome via Homebrew
brew install --cask google-chrome

# Or download from: https://www.google.com/chrome/
```

### Step 5: Install ChromeDriver
```bash
# Install ChromeDriver
brew install chromedriver

# Verify ChromeDriver installation
chromedriver --version
```

### Step 6: Clone and Setup Project
```bash
# Clone the repository (or download the files)
mkdir advanced-chatbot
cd advanced-chatbot

# Create virtual environment
python3.11 -m venv chatbot_env
source chatbot_env/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r advanced_requirements.txt
```

---

## 🐧 Linux Installation

### Step 1: Update System Packages
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL/Fedora
sudo yum update -y
# OR for newer versions:
sudo dnf update -y
```

### Step 2: Install Python 3.11
```bash
# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip -y

# CentOS/RHEL (Enable EPEL repository first)
sudo yum install epel-release -y
sudo yum install python311 python311-pip -y

# Fedora
sudo dnf install python3.11 python3.11-pip -y

# Verify installation
python3.11 --version
```

### Step 3: Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt install -y \
    portaudio19-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    ffmpeg \
    wget \
    unzip

# CentOS/RHEL
sudo yum install -y \
    portaudio-devel \
    tesseract \
    tesseract-langpack-eng \
    ffmpeg \
    wget \
    unzip

# Fedora
sudo dnf install -y \
    portaudio-devel \
    tesseract \
    tesseract-langpack-eng \
    ffmpeg \
    wget \
    unzip
```

### Step 4: Install Google Chrome
```bash
# Ubuntu/Debian
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable -y

# CentOS/RHEL/Fedora
sudo yum install -y https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
```

### Step 5: Install ChromeDriver
```bash
# Download and install ChromeDriver
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# Verify installation
chromedriver --version
```

### Step 6: Clone and Setup Project
```bash
# Create project directory
mkdir advanced-chatbot
cd advanced-chatbot

# Create virtual environment
python3.11 -m venv chatbot_env
source chatbot_env/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r advanced_requirements.txt
```

---

## 🪟 Windows Installation

### Step 1: Install Python 3.11
1. **Download Python 3.11** from [python.org](https://www.python.org/downloads/windows/)
2. **Run the installer** and make sure to:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install for all users" (optional)
   - ✅ Choose "Customize installation"
   - ✅ Select all optional features
3. **Verify installation**:
```cmd
python --version
pip --version
```

### Step 2: Install Git (Optional but Recommended)
1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Install with default settings

### Step 3: Install Google Chrome
1. Download from [google.com/chrome](https://www.google.com/chrome/)
2. Install with default settings

### Step 4: Install ChromeDriver
```cmd
# Option 1: Manual Installation
# 1. Check your Chrome version: Chrome menu > Help > About Google Chrome
# 2. Download matching ChromeDriver from: https://chromedriver.chromium.org/
# 3. Extract chromedriver.exe to a folder in your PATH (e.g., C:\Windows\System32)

# Option 2: Using Chocolatey (if installed)
choco install chromedriver

# Verify installation
chromedriver --version
```

### Step 5: Install Audio Dependencies
**Option 1: Using pip (Recommended)**
```cmd
# PyAudio wheels are available for Windows
pip install PyAudio
```

**Option 2: Manual Installation (if pip fails)**
1. Download PyAudio wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Install: `pip install PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl`

### Step 6: Setup Project
```cmd
# Create project directory
mkdir advanced-chatbot
cd advanced-chatbot

# Create virtual environment
python -m venv chatbot_env

# Activate virtual environment
chatbot_env\Scripts\activate

# Install Python packages
pip install --upgrade pip
pip install -r advanced_requirements.txt
```

---

# 🔧 Configuration Setup

## Step 1: Create Environment File
Create a `.env` file in your project directory:

```bash
# Create .env file
touch .env  # macOS/Linux
# OR
echo. > .env  # Windows
```

Add your API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Step 2: Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

## Step 3: Verify Installation
Test your setup:

```bash
# Activate virtual environment (if not already active)
source chatbot_env/bin/activate  # macOS/Linux
# OR
chatbot_env\Scripts\activate  # Windows

# Test imports
python -c "import streamlit, selenium, chromadb, easyocr, speech_recognition; print('✅ All packages imported successfully!')"

# Test ChromeDriver
chromedriver --version
```

---

# 🚀 Running the Application

## Step 1: Activate Environment
```bash
# Navigate to project directory
cd advanced-chatbot

# Activate virtual environment
source chatbot_env/bin/activate  # macOS/Linux
# OR
chatbot_env\Scripts\activate  # Windows
```

## Step 2: Launch the Chatbot
```bash
# Run the Streamlit application
streamlit run advanced_chatbot.py
```

## Step 3: Access the Application
1. **Automatic opening**: Your browser should open automatically
2. **Manual access**: Open your browser and go to:
   - Local URL: `http://localhost:8501`
   - Network URL: `http://192.168.x.x:8501` (for other devices)

---

# 📖 Usage Instructions

## 🔧 Initial Setup
1. **Enter API Key**: Add your Gemini API key in the sidebar
2. **Configure Settings**: Adjust scraping parameters as needed
   - Max pages: 15-20 for most websites
   - Parallel workers: 3-4 for optimal performance
   - Enable OCR if the site has important images
   - Enable voice responses for audio interaction

## 🕷️ Scraping a Website
1. **Enter Website URL**: Input the target website URL
2. **Click "Start Advanced Scraping"**: Begin the scraping process
3. **Monitor Progress**: Watch real-time scraping progress
4. **Review Results**: Check scraped content and statistics

## 💬 Chatting with Content
1. **Type Questions**: Use the chat input to ask about the website
2. **Voice Interaction**: Click "Ask Question by Voice" (if enabled)
3. **View Sources**: Expand "Sources used" to see information origins
4. **Audio Responses**: Listen to AI-generated voice responses

## 🎤 Voice Features
1. **Enable Voice**: Check "Enable voice responses" in sidebar
2. **Ask by Voice**: Click the voice button and speak immediately
3. **Clear Speech**: Speak clearly for 2-10 seconds
4. **Listen to Responses**: Audio responses are generated automatically

---

# 🛠️ Troubleshooting

## Common Issues and Solutions

### 🔴 ChromeDriver Issues
**Problem**: `selenium.common.exceptions.WebDriverException`
```bash
# Solution: Update ChromeDriver
brew upgrade chromedriver  # macOS
# Or download latest from chromedriver.chromium.org
```

### 🔴 Audio/PyAudio Issues
**Problem**: `OSError: No Default Input Device Available`
```bash
# macOS: Install PortAudio
brew install portaudio

# Linux: Install audio development packages
sudo apt install portaudio19-dev  # Ubuntu/Debian

# Windows: Reinstall PyAudio
pip uninstall pyaudio
pip install pyaudio
```

### 🔴 OCR Issues
**Problem**: OCR not working or poor results
```bash
# Install Tesseract language data
brew install tesseract-lang  # macOS
sudo apt install tesseract-ocr-all  # Linux
```

### 🔴 Memory Issues
**Problem**: Application running slowly or crashing
- **Reduce max pages**: Set to 10-15 for large sites
- **Decrease workers**: Use 2-3 parallel workers
- **Disable OCR**: Turn off image text extraction for text-heavy sites

### 🔴 API Issues
**Problem**: Gemini API errors
- **Check API key**: Ensure it's correctly set in `.env`
- **Verify quotas**: Check your API usage limits
- **Network issues**: Ensure stable internet connection

---

# 📊 Performance Tips

## 🚀 Optimal Settings
- **Max Pages**: 15-20 for balanced speed and coverage
- **Workers**: 3-4 for most systems (adjust based on CPU cores)
- **OCR**: Enable only for image-heavy websites
- **GPU OCR**: Use if you have a compatible GPU

## 💾 Storage Management
- **Regular cleanup**: Clear `./chroma_db` folder periodically
- **Collection naming**: Use descriptive names for different websites
- **Backup**: Important collections can be backed up by copying the database folder

## 🔧 System Resources
- **RAM Usage**: ~500MB-2GB depending on content
- **CPU Usage**: High during scraping, low during chat
- **Storage**: ~10-50MB per website collection

---

# 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black advanced_chatbot.py
flake8 advanced_chatbot.py
```

---

# 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# 🆘 Support

## Getting Help
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join community discussions
- **Documentation**: Check this README and inline code comments

## Useful Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Google AI Studio](https://makersuite.google.com/)
- [Selenium WebDriver](https://selenium-python.readthedocs.io/)

---

# 🔄 Updates and Changelog

## Version 1.0.0
- ✅ Initial release with core features
- ✅ Web scraping with parallel processing
- ✅ OCR integration (EasyOCR + Tesseract)
- ✅ Voice interaction system
- ✅ Persistent vector storage
- ✅ AI-powered responses

## Upcoming Features
- 🔜 Multi-language support
- 🔜 Advanced filtering options
- 🔜 Export/import functionality
- 🔜 Custom AI model integration
- 🔜 Enhanced security features

---

**🎉 You're now ready to use the Advanced AI Website Chatbot!**

Start by scraping your first website and experience the power of AI-enhanced web content interaction. Happy chatting! 🚀
