import React, { useState, useRef, useEffect } from 'react'

function ChatInput({ onSend, enabled }) {
  const [input, setInput] = useState('')
  const inputRef = useRef(null)

  useEffect(() => {
    if (enabled && inputRef.current) {
      inputRef.current.focus()
    }
  }, [enabled])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() && enabled) {
      onSend(input)
      setInput('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="chat-input-area">
      <button className="attach-btn" title="Attach">📎</button>
      <div className="input-wrapper">
        <input
          ref={inputRef}
          type="text"
          className="message-input"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={!enabled}
          autoComplete="off"
        />
      </div>
      <button
        type="submit"
        className="send-btn"
        disabled={!enabled || !input.trim()}
        onClick={handleSubmit}
        title="Send"
      >
        <span className="send-icon">➤</span>
      </button>
    </div>
  )
}

export default ChatInput

