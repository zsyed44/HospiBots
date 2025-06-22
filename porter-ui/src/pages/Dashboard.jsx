import React from 'react';
import { Bot, Clock, CheckCircle, Activity, Settings, Plus } from 'lucide-react';
import StatCard from '../components/StatCard';
import BotCard from '../components/BotCard';
import TaskItem from '../components/TaskItem';

const Dashboard = ({ bots, tasks }) => {
  return (
    <div className="dashboard">
      <div className="stats-grid">
        <StatCard title="Active Bots" value="2" icon={Bot} trend="+1 today" />
        <StatCard title="Pending Tasks" value="7" icon={Clock} trend="-3 from yesterday" />
        <StatCard title="Completed Today" value="24" icon={CheckCircle} trend="+15%" />
        <StatCard title="System Health" value="98%" icon={Activity} trend="Excellent" />
      </div>

      <div className="content-grid">
        <div className="panel">
          <div className="panel-header">
            <h2>Active Bots</h2>
            <button className="icon-button">
              <Settings size={20} />
            </button>
          </div>
          <div className="bots-list">
            {bots.filter(bot => bot.status === 'active').map(bot => (
              <BotCard key={bot.id} bot={bot} />
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2>Recent Tasks</h2>
            <button className="primary-button">
              <Plus size={16} />
              New Task
            </button>
          </div>
          <div className="tasks-list">
            {tasks.slice(0, 3).map(task => (
              <TaskItem key={task.id} task={task} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;