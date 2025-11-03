import React from 'react'

function ChatHeader() {
  return (
    <div className="chat-header">
      <div className="header-avatar">
        <div className="avatar">👤</div>
      </div>
      <div className="header-info">
        <div className="contact-name">Lok Avinashh's Personal Assistant</div>
        <div className="contact-status">online</div>
      </div>
      <div className="header-actions">
        <button className="icon-btn" title="Search">🔍</button>
        <button className="icon-btn" title="Menu">⋮</button>
      </div>
    </div>
  )
}

export default ChatHeader

