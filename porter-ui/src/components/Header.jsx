import React from 'react';
import { Bot, Clock, Wifi } from 'lucide-react';

const Header = ({ currentTime }) => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">
            <Bot size={24} />
          </div>
          <div className="header-info">
            <h1>Porter</h1>
            <p>Hospital Bot Management</p>
          </div>
        </div>

        <div className="header-right">
          <div className="header-status">
            <Clock size={16} />
            <span>{currentTime.toLocaleTimeString()}</span>
          </div>
          <div className="header-status">
            <Wifi size={16} style={{ color: '#22c55e' }} />
            <span>Connected</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;