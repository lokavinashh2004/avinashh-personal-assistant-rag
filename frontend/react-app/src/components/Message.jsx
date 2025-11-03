import React from 'react'

function Message({ message, getCurrentTime }) {
  if (message.isWelcome) {
    return (
      <div className="welcome-message">
        <div className="welcome-avatar">
          <div className="avatar">👤</div>
        </div>
        <div className="welcome-text">
          {message.content.split('\n').map((line, i) => (
            <p key={i}>{line}</p>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className={`message ${message.isSent ? 'sent' : 'received'} ${message.isError ? 'error' : ''}`}>
      <div className="message-row">
        <div className="message-bubble">
          <div className="message-content">
            {message.content}
          </div>
          <div className="message-time">
            {getCurrentTime()}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Message

