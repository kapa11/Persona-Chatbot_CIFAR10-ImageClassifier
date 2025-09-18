# 🤖 Kapa's Persona Chatbot

Interactive conversational AI system featuring 5 distinct personalities with shared memory and Streamlit-based web interface.

## TLDR
This program implements an interactive persona-based chatbot system using HuggingFace's Inference API and Streamlit. It features 5 unique AI personalities (RoastBot, ShakespeareBot, EmojiBot, PhilosopherBot, and PirateBot) that maintain individual conversation histories while sharing context through a unified memory system. Each persona has specialized prompts and response styles, resulting in engaging, character-driven interactions. The application includes conversation management, message styling, user feedback collection, and a professional web interface for a seamless user experience.

---

## About the Application
A sophisticated chatbot platform that demonstrates natural language processing capabilities through character-driven AI interactions. Built using modern web technologies and cloud-based AI inference, it showcases personality modeling in conversational AI systems.

## Application Specifications
- **Personas**: 5 unique character personalities with specialized behaviors
- **Backend**: HuggingFace Inference API with Cerebras provider
- **Frontend**: Streamlit-based web interface
- **Memory System**: Shared conversation history across all personas
- **Authentication**: Environment-based API key management
- **Deployment**: Web-ready with responsive design

## Persona Architecture

### Core Personas System
The application implements distinct AI personalities through specialized system prompts and response patterns, each designed for unique interaction styles and user engagement scenarios.

**RoastBot**: delivers witty and sarcastic responses with clever humor while maintaining light-hearted interactions. It uses the conversation history to make references and create personalized roasts, ensuring entertainment without crossing boundaries into genuinely offensive content.

**ShakespeareBot**: responds in eloquent Shakespearean English with iambic pentameter, "thee," "thou," and "thy" constructions. It transforms modern topics into classical poetic expressions, creating an educational and entertaining experience that bridges contemporary conversations with literary tradition.

**EmojiBot**: communicates primarily through emojis and brief text, making conversations visually engaging and universally accessible. It translates complex ideas into emoji sequences, adding minimal explanatory text to create a fun and modern communication style.

**PhilosopherBot**: provides deep, thoughtful responses with philosophical insights and existential contemplation. It encourages critical thinking by exploring the deeper meanings behind questions and connecting everyday topics to profound philosophical concepts and life questions.

**PirateBot**: speaks in authentic pirate vernacular with "ahoy," "matey," and seafaring terminology. It maintains the adventurous spirit of maritime culture while providing helpful responses, creating an entertaining and thematically consistent interaction experience.

## Technical Implementation

### API Integration
The system uses HuggingFace's Inference API through the Cerebras provider, enabling access to state-of-the-art language models without local computational requirements. Environment variable authentication ensures secure API access while maintaining deployment flexibility across different platforms.

### Memory Management
A sophisticated conversation tracking system maintains individual chat histories for each persona while enabling cross-persona context sharing. Messages are stored with timestamps, user feedback, and persona identification, creating a comprehensive interaction database for enhanced user experience.

### User Interface Design
Streamlit powers the responsive web interface with custom CSS styling, sidebar navigation, and real-time chat display. The interface features persona selection, conversation clearing, message copying, and user feedback collection through an intuitive and accessible design.

## Core Functions

### Persona Management
Processes user input through the selected persona's system prompt, incorporating conversation history for contextual awareness and generating character-appropriate responses.

### Interface Controls
Manages chat history storage, retrieval, and clearing functionality while maintaining session state across user interactions and persona switches.

## User Interface Features

### **Interactive Elements:**
- **Persona Selection**: Dropdown menu with 5 distinct character options
- **Real-time Chat**: Immediate response generation with typing indicators
- **Message Management**: Copy functionality and conversation clearing options
- **User Feedback**: Emoji-based rating system for response quality

### **Visual Design:**
- **Responsive Layout**: Sidebar navigation with main chat area
- **Message Styling**: Custom CSS for user/bot message differentiation  
- **Professional Aesthetics**: Clean, modern interface with consistent branding
- **Accessibility Features**: Clear typography and intuitive navigation

### **Conversation Flow:**
- **Session Persistence**: Messages maintained throughout browser session
- **Context Awareness**: Each persona can reference previous interactions
- **Multi-persona Memory**: Shared conversation history across all characters
- **Real-time Updates**: Instant message display and response generation

## 🚀 Getting Started

### Step 1: Clone the Repository
First, download the project to your local machine by cloning the repository from GitHub:
You may choose to copy this command into your terminal: 
1. ``` git clone https://github.com/kapa11/persona-chatbot.git```
2. ``` cd persona-chatbot```

### Step 2: Virtual environment(recommended)
You can create a virtual environment to keep this project’s dependencies separate:
1. Copy and paste the command: ``` python -m venv venv```
2. If you're on Windows, to activate: ``` venv\Scripts\activate```
3. If you're on Linux/Mac, to activate: ``` source venv/bin/activate```

### Step 3: Install Required Python Packages
Before running the chatbot, make sure all the necessary Python packages are installed. The project uses Streamlit and Hugging Face Hub, which are not included in the standard Python library.
Copy-paste and run the command:  ``` pip install streamlit huggingface_hub```

### Step 4: Get your Hugging Face Token
The chatbot uses Hugging Face’s models, which require an access token to authenticate
1. Go to Hugging Face and sign up or log in
2. Click on your profile picture → Settings → Access Tokens
3. Click New token, give it a name (e.g., persona-chatbot-token), select “Read” access, and generate the token.
4. Copy the token as you will need it to run the chatbot.
5. If you're on Windows, set your token in(in the terminal): ``` set HF_TOKEN=your_token_here```
6. If you're on Linux/Mac, set your token in(in the terminal): ``` export HF_TOKEN=your_token_here```

### Step 5: Finally!
Now that the code, dependencies, and Hugging Face token are ready, you can launch the chatbot using Streamlit.
Note: Make sure your virtual environment is activated and your Hugging Face token is set.
Use the command: ``` streamlit run finalApp.py```

#🎉🔥✨ *Et voila* ✨🔥🎉





