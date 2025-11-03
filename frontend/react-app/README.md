# React Frontend for RAG Assistant

This is the React frontend for the Avinashh RAG Assistant chatbot.

## Setup

1. **Install dependencies:**
   ```bash
   cd frontend/react-app
   npm install
   ```

2. **Development mode:**
   ```bash
   npm run dev
   ```
   This runs Vite dev server on port 3000 with proxy to Flask backend (port 7860)

3. **Build for production:**
   ```bash
   npm run build
   ```
   This builds the React app to `frontend/static/` which Flask serves.

## Project Structure

```
react-app/
├── src/
│   ├── components/
│   │   ├── ChatHeader.jsx
│   │   ├── ChatInput.jsx
│   │   ├── ConnectionStatus.jsx
│   │   ├── Message.jsx
│   │   ├── MessageList.jsx
│   │   └── TypingIndicator.jsx
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
└── index.html
```

## Integration

The Flask backend serves the built React app from `frontend/static/` directory. 
After running `npm run build`, restart the Flask server to serve the new build.

