import React, { useState, useEffect } from 'react';
import {
  Bot,
  Navigation,
  Package,
  FileText,
  Pill,
  Users,
  Settings,
  Activity,
  Clock,
  MapPin, // Keep MapPin for the map button
  Mic,
  MicOff,
  Play,
  Pause,
  CheckCircle,
  AlertCircle,
  Battery,
  Wifi,
  Calendar,
  Plus,
  Search,
  Filter,
  MoreVertical
} from 'lucide-react';
import './App.css';
import MapComponent from './MapComponent'; // Import the MapComponent

const PorterUI = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [bots, setBots] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [showMap, setShowMap] = useState(false); // New state to toggle map visibility

  useEffect(() => {
    const baseURL = import.meta.env.VITE_API_BASE_URL;

    fetch(`${baseURL}/api/bots`)
      .then(res => res.json())
      .then(data => setBots(data))
      .catch(err => console.error("Failed to fetch bots:", err));

    fetch(`${baseURL}/api/tasks`)
      .then(res => res.json())
      .then(data => setTasks(data))
      .catch(err => console.error("Failed to fetch tasks:", err));
  }, []);

  const [isListening, setIsListening] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical': return '#ef4444';
      case 'high': return '#f97316';
      case 'normal': return '#3b82f6';
      case 'low': return '#6b7280';
      default: return '#9ca3af';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#22c55e';
      case 'charging': return '#eab308';
      case 'offline': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const StatCard = ({ title, value, icon: Icon, trend, color = "#1e293b" }) => (
    <div className="stat-card" style={{ backgroundColor: color }}>
      <div className="stat-content">
        <div className="stat-info">
          <p className="stat-title">{title}</p>
          <p className="stat-value">{value}</p>
          {trend && <p className="stat-trend">↗ {trend}</p>}
        </div>
        <div className="stat-icon">
          <Icon size={24} />
        </div>
      </div>
    </div>
  );

  const BotCard = ({ bot }) => (
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

  const TaskItem = ({ task }) => (
    <div className="task-item">
      <div className="task-content">
        <div className="task-header">
          <div
            className="priority-dot"
            style={{ backgroundColor: getPriorityColor(task.priority) }}
          ></div>
          <span className="task-type">{task.type}</span>
          <span className="task-room">Room {task.room}</span>
        </div>
        <p className="task-description">{task.item || task.request || task.nurse}</p>
        {task.assignedBot && (
          <p className="task-assigned">Assigned to {task.assignedBot}</p>
        )}
      </div>
      <div className="task-actions">
        <span className={`task-status ${task.status}`}>
          {task.status}
        </span>
        <button className="task-menu">
          <MoreVertical size={16} />
        </button>
      </div>
    </div>
  );

  const renderDashboard = () => (
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

  const renderBots = () => (
    <div className="page">
      <div className="page-header">
        <h1>Bot Fleet</h1>
        <div className="page-actions">
          <button className="secondary-button" onClick={() => setShowMap(!showMap)}>
            <MapPin size={16} />
            {showMap ? 'Hide Map' : 'Show Map'}
          </button>
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

      {showMap && (
        <div className="map-section">
          <h2>Hospital Floor Plan</h2>
          <MapComponent bots={bots} />
        </div>
      )}

      <div className="bots-grid">
        {bots.map(bot => (
          <BotCard key={bot.id} bot={bot} />
        ))}
      </div>
    </div>
  );

  const renderTasks = () => (
    <div className="page">
      <div className="page-header">
        <h1>Task Queue</h1>
        <div className="page-actions">
          <div className="search-box">
            <Search size={16} />
            <input type="text" placeholder="Search tasks..." />
          </div>
          <button className="primary-button">
            <Plus size={16} />
            New Task
          </button>
        </div>
      </div>

      <div className="tasks-list">
        {tasks.map(task => (
          <TaskItem key={task.id} task={task} />
        ))}
      </div>
    </div>
  );

  const renderVoiceControl = () => (
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

  const navigation = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'bots', label: 'Bots', icon: Bot },
    { id: 'tasks', label: 'Tasks', icon: Package },
    { id: 'voice', label: 'Voice Control', icon: Mic },
    { id: 'prescriptions', label: 'Prescriptions', icon: Pill },
    { id: 'scribing', label: 'Scribing', icon: FileText },
    { id: 'patients', label: 'Patients', icon: Users },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  return (
    <div className="app">
      {/* Header */}
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

      <div className="layout">
        {/* Sidebar */}
        <nav className="sidebar">
          <ul className="nav-list">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <li key={item.id}>
                  <button
                    onClick={() => setActiveTab(item.id)}
                    className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                  >
                    <Icon size={20} />
                    <span>{item.label}</span>
                  </button>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Main Content */}
        <main className="main">
          {activeTab === 'dashboard' && renderDashboard()}
          {activeTab === 'bots' && renderBots()}
          {activeTab === 'tasks' && renderTasks()}
          {activeTab === 'voice' && renderVoiceControl()}
          {activeTab === 'prescriptions' && (
            <div className="placeholder">
              <Pill size={64} />
              <h2>Prescriptions</h2>
              <p>Prescription management coming soon...</p>
            </div>
          )}
          {activeTab === 'scribing' && (
            <div className="placeholder">
              <FileText size={64} />
              <h2>Scribing</h2>
              <p>Note-taking interface coming soon...</p>
            </div>
          )}
          {activeTab === 'patients' && (
            <div className="placeholder">
              <Users size={64} />
              <h2>Patients</h2>
              <p>Patient management coming soon...</p>
            </div>
          )}
          {activeTab === 'settings' && (
            <div className="placeholder">
              <Settings size={64} />
              <h2>Settings</h2>
              <p>System configuration coming soon...</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default PorterUI;