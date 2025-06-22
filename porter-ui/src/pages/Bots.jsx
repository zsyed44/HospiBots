import React from 'react';
import { Filter, Plus } from 'lucide-react';
import BotCard from '../components/BotCard';

const Bots = ({ bots }) => {
  return (
    <div className="page">
      <div className="page-header">
        <h1>Bot Fleet</h1>
        <div className="page-actions">
          <button className="secondary-button">
            <Filter size={16} />
            Filter
          </button>
          <button className="primary-button">
            <Plus size={16} />
            Add Bot
          </button>
        </div>
      </div>

      <div className="bots-grid">
        {bots.map(bot => (
          <BotCard key={bot.id} bot={bot} />
        ))}
      </div>
    </div>
  );
};

export default Bots;