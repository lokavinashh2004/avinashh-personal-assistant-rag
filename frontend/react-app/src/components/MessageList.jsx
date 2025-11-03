import React from 'react'
import Message from './Message'

function MessageList({ messages, getCurrentTime }) {
  return (
    <>
      {messages.map((message) => (
        <Message
          key={message.id}
          message={message}
          getCurrentTime={getCurrentTime}
        />
      ))}
    </>
  )
}

export default MessageList

