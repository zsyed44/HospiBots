import React, { useState } from 'react';
import { Mic, MicOff } from 'lucide-react';

const VoiceControl = () => {
  const [isListening, setIsListening] = useState(false);

  return (
    <div className="page">
      <h1>Voice Control</h1>

      <div className="voice-panel">
        <div className="voice-center">
          <div className={`voice-circle ${isListening ? 'listening' : ''}`}>
            {isListening ? (
              <Mic size={40} style={{ color: '#ef4444' }} />
            ) : (
              <MicOff size={40} style={{ color: '#6b7280' }} />
            )}
          </div>

          <h2>
            {isListening ? 'Listening...' : 'Voice Commands'}
          </h2>
          <p className="voice-description">
            {isListening ? 'Say "Porter" followed by your command' : 'Click to start voice control'}
          </p>

          <button
            onClick={() => setIsListening(!isListening)}
            className={isListening ? 'stop-button' : 'primary-button'}
          >
            {isListening ? 'Stop Listening' : 'Start Listening'}
          </button>
        </div>
      </div>

      <div className="commands-panel">
        <h3>Available Commands</h3>
        <div className="commands-list">
          <div className="command-item">
            <code>"Porter, navigate to Room 301"</code>
            <p>Commands a bot to navigate to specified location</p>
          </div>
          <div className="command-item">
            <code>"Porter, answer question"</code>
            <p>Activates question answering mode</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VoiceControl;