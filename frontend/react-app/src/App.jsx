import React, { useState, useEffect, useRef } from 'react'
import ChatHeader from './components/ChatHeader'
import MessageList from './components/MessageList'
import ChatInput from './components/ChatInput'
import TypingIndicator from './components/TypingIndicator'
import ConnectionStatus from './components/ConnectionStatus'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      content: "Hello! 👋\nI'm Lok Avinashh's Personal Assistant. I'm here to help you learn about him. Ask me anything about his resume, skills, experience, or background!",
      isSent: false,
      isWelcome: true,
      timestamp: new Date()
    }
  ])
  const [isTyping, setIsTyping] = useState(false)
  const [inputEnabled, setInputEnabled] = useState(false)
  const [status, setStatus] = useState({ message: '', type: '' })
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  useEffect(() => {
    checkConnection()
    setInputEnabled(true)
  }, [])

  const checkConnection = async () => {
    try {
      const response = await fetch('/health')
      const data = await response.json()
      if (data.status === 'ok') {
        setStatus({ message: `Connected (${data.generator} mode)`, type: 'success' })
        setTimeout(() => setStatus({ message: '', type: '' }), 2000)
      }
    } catch (error) {
      setStatus({ message: 'Unable to connect to backend', type: 'error' })
      setInputEnabled(false)
    }
  }

  const getCurrentTime = () => {
    const now = new Date()
    const hours = now.getHours().toString().padStart(2, '0')
    const minutes = now.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  }

  const sendMessage = async (messageText) => {
    if (!messageText.trim() || !inputEnabled) return

    // Add user message
    const userMessage = {
      id: Date.now().toString(),
      content: messageText,
      isSent: true,
      timestamp: new Date()
    }

    setMessages(prev => {
      // Remove welcome message if present
      return prev.filter(msg => msg.id !== 'welcome').concat(userMessage)
    })

    setInputEnabled(false)
    setIsTyping(true)

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: messageText })
      })

      const data = await response.json()
      setIsTyping(false)

      if (response.ok && data.answer) {
        const botMessage = {
          id: (Date.now() + 1).toString(),
          content: data.answer.trim(),
          isSent: false,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, botMessage])
        setStatus({ message: '', type: '' })
      } else {
        const errorMsg = data.error || 'Unknown error occurred'
        const errorMessage = {
          id: (Date.now() + 1).toString(),
          content: `Sorry, I encountered an error: ${errorMsg}`,
          isSent: false,
          isError: true,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, errorMessage])
        setStatus({ message: 'Error: ' + errorMsg, type: 'error' })
      }
    } catch (error) {
      setIsTyping(false)
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        content: `Sorry, I couldn't reach the server. Please make sure it's running.`,
        isSent: false,
        isError: true,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
      setStatus({ message: `Connection error: ${error.message}`, type: 'error' })
    } finally {
      setInputEnabled(true)
    }
  }

  return (
    <div className="whatsapp-container">
      <ChatHeader />
      <div className="chat-messages">
        <MessageList messages={messages} getCurrentTime={getCurrentTime} />
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>
      <ConnectionStatus status={status} />
      <ChatInput onSend={sendMessage} enabled={inputEnabled} />
    </div>
  )
}

export default App

