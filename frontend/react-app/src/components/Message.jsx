import React from 'react'

function renderMessageContent(message) {
  if (message.document) {
    const { url, name, type } = message.document
    return (
      <>
        <div className="document-card">
          <div className="document-info">
            <div className="document-icon">{type || 'PDF'}</div>
            <div className="document-meta">
              <span className="document-name">{name || 'Resume.pdf'}</span>
              <span className="document-desc">Tap to download</span>
            </div>
          </div>
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            download={name || true}
            className="document-download"
          >
            Download
          </a>
        </div>
        <div className="document-caption">{message.content}</div>
      </>
    )
  }

  return message.content
}

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
            {renderMessageContent(message)}
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

