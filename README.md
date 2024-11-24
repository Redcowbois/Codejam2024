### **📚 Inspiration**  

We created **Omni** after noticing a growing trend: while students increasingly rely on online lecture recordings and slides, these tools are often underutilized. Many of our peers struggled to effectively engage with and retain lecture content, even with these resources at their fingertips. Recordings became something to skim at double speed, and slides became just another file lost in the chaos of study materials.  

Our vision with Omni was to breathe life into these passive materials. By transforming lecture recordings and slides into dynamic, interactive learning tools, Omni empowers students to actively engage with content in a way that adapts to their unique learning styles.  

### **✨ What it does**  
**Omni** is your all-in-one learning companion that transforms lecture content into multiple engaging formats:  

- Converts lecture recordings and slides into concise, topic-focused podcasts for on-the-go learning  
- Automatically generates comprehensive flashcard decks that highlight key concepts and definitions  
- Creates intelligent quizzes that test understanding and help identify knowledge gaps  
- Provides a unified platform where all these learning tools work together seamlessly  

### **🛠️ How we built it**  
Our tech stack combines powerful open-source tools with custom solutions:  

- Built the core backend using Django and Python.  
- Leveraged (locally) OpenAI's Whisper model for audio-to-text transcription.  
- Utilized a locally hosted Qwen 2.5 model for text generation and analysis.  
- Developed custom audio processing algorithms for the lecture-to-podcast conversion.  
- Integrated an SQLite database for content management and user data storage.  

### **🚧 Challenges we ran into**  
Developing **Omni** presented several significant technical challenges:  

- Managing memory usage with locally hosted large language models (LLMs) while maintaining reasonable processing speeds.  
- Fine-tuning model outputs to generate educationally valuable content instead of irrelevant responses.  
- Balancing processing speed with the quality of generated content.  
- Ensuring consistent formatting across various types of lecture materials.  

### **🏆 Accomplishments that we're proud of**  
- Successfully implemented local hosting for the language model, eliminating reliance on external API calls.  
- Created a robust system for generating podcasts that produces engaging and coherent content.  
- Developed an intelligent quiz generation system that creates relevant and challenging questions.  
- Built a scalable architecture capable of handling multiple file formats and content types.  
- Achieved fast processing times while maintaining high-quality output.  

### **💡 What we learned**  
- Practical implementation of local LLMs and their optimization  
- Prompt engineering in the context of a local model  
- Using a LLM in a context other than web-hosted ones like ChatGPT, Claude, or Gemini  

### **🚀 What's next for Omni**  
The way we built the app is highly scalable, allowing for many additional features, such as:  
- Adding support for multiple languages  
- Custom voice options and personalities for podcast hosts  
- Mobile app development  
