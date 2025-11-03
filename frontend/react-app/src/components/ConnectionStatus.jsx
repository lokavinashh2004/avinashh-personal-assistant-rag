import React from 'react'

function ConnectionStatus({ status }) {
  if (!status.message) return null

  return (
    <div className={`connection-status ${status.type}`}>
      {status.message}
    </div>
  )
}

export default ConnectionStatus

