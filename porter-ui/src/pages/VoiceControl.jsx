import React, { useState, useEffect, useRef } from 'react'
import { Mic, MicOff } from 'lucide-react'

const VoiceControl = () => {
  const [isListening, setIsListening] = useState(false)
  const [botMessage, setBotMessage] = useState('')
  const [logs, setLogs] = useState([])
  const [path, setPath] = useState([])
  const recognitionRef = useRef(null)

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) {
      console.warn('SpeechRecognition not supported in this browser')
      return
    }
    const rec = new SpeechRecognition()
    rec.lang = 'en-US'
    rec.interimResults = false
    rec.maxAlternatives = 1

    rec.onresult = ({ results }) => {
      const transcript = results[0][0].transcript.trim()
      if (transcript) sendCommand(transcript)
    }

    rec.onend = () => {
      setIsListening(false)
    }

    recognitionRef.current = rec
  }, [])

  const sendCommand = async (text) => {
    try {
      setBotMessage('')
      setLogs([])
      setPath([])

      const res = await fetch('/api/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ commandText: text }),
      })
      const data = await res.json()

      // Core message
      setBotMessage(data.message || 'No response')

      // Full terminal-style log
      if (data.log && Array.isArray(data.log)) {
        setLogs(data.log)
      }

      // Path array (if provided)
      if (data.path && Array.isArray(data.path)) {
        setPath(data.path)
      }
    } catch (err) {
      console.error('Error sending command', err)
      setBotMessage('Error communicating with bot')
    }
  }

  const startListening = () => {
    const rec = recognitionRef.current
    if (!rec) return
    setBotMessage('')
    setIsListening(true)
    rec.start()
  }

  const stopListening = () => {
    recognitionRef.current?.stop()
  }

  return (
    <div className="page">
      <h1>Voice Control</h1>

      <div className="voice-panel">
        <div className="voice-center">
          <div className={`voice-circle ${isListening ? 'listening' : ''}`}>
            {isListening
              ? <Mic size={40} style={{ color: '#ef4444' }} />
              : <MicOff size={40} style={{ color: '#6b7280' }} />
            }
          </div>

          <h2>{isListening ? 'Listening...' : 'Voice Commands'}</h2>
          <p className="voice-description">
            {isListening
              ? 'Speak now'
              : 'Click to start voice control'}
          </p>

          <button
            onClick={isListening ? stopListening : startListening}
            className={isListening ? 'stop-button' : 'primary-button'}
          >
            {isListening ? 'Stop Listening' : 'Start Listening'}
          </button>
        </div>
      </div>

      {botMessage && (
        <div className="bot-response">
          <strong>Porter says:</strong> {botMessage}
        </div>
      )}

      {logs.length > 0 && (
        <pre className="bot-log">
          {logs.join('\n')}
        </pre>
      )}

      {path.length > 0 && (
        <div className="path-panel">
          <h4>Computed Path:</h4>
          <ol>
            {path.map((node, index) => (
              <li key={index}>{node}</li>
            ))}
          </ol>
        </div>
      )}

      <div className="commands-panel">
        <h3>Available Commands</h3>
        <div className="commands-list">
          <div className="command-item">
            <code>"Porter, navigate to Room 301"</code>
            <p>Commands the bot to navigate to the specified room</p>
          </div>
          <div className="command-item">
            <code>"Porter, shutdown"</code>
            <p>Signals the bot to shut down</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VoiceControl
