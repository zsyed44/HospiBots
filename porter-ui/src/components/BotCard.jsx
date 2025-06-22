import React from 'react';
import { Bot, Battery, MapPin, Activity } from 'lucide-react';

const BotCard = ({ bot }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#22c55e';
      case 'charging': return '#eab308';
      case 'offline': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical': return '#ef4444';
      case 'high': return '#f97316';
      case 'normal': return '#3b82f6';
      case 'low': return '#6b7280';
      default: return '#9ca3af';
    }
  };

  return (
    <div className="bot-card">
      <div className="bot-header">
        <div className="bot-info">
          <div className="bot-icon">
            <Bot size={20} style={{ color: getStatusColor(bot.status) }} />
          </div>
          <div>
            <h3 className="bot-name">{bot.name}</h3>
            <p className="bot-status">{bot.status}</p>
          </div>
        </div>
        <div className="bot-battery">
          <Battery size={16} />
          <span>{bot.battery}%</span>
        </div>
      </div>

      <div className="bot-details">
        <div className="bot-location">
          <MapPin size={16} />
          {bot.location}
        </div>
        {bot.task && (
          <div className="bot-task">
            <Activity size={16} />
            {bot.task}
          </div>
        )}
      </div>

      {bot.priority && (
        <div className="bot-priority">
          <div
            className="priority-dot"
            style={{ backgroundColor: getPriorityColor(bot.priority) }}
          ></div>
          <span>{bot.priority} priority</span>
        </div>
      )}
    </div>
  );
};

export default BotCard;