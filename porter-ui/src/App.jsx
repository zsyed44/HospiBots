import React, { useState, useEffect } from 'react';
import { Pill, FileText, Users, Settings } from 'lucide-react';

// Component imports
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import PlaceholderPage from './components/PlaceholderPage';

// Page imports
import Dashboard from './pages/Dashboard';
import Bots from './pages/Bots';
import Tasks from './pages/Tasks';
import VoiceControl from './pages/VoiceControl';

import './App.css';
import Prescriptions from './pages/Perscriptions';
import Patients from './pages/Patients';

const PorterUI = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [bots, setBots] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [patients, setPatients] = useState([]);
  const [currentTime, setCurrentTime] = useState(new Date());

  // Fetch data from API
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


    fetch(`${baseURL}/api/patients`)
      .then(res => res.json())
      .then(data => setPatients(data))
      .catch(err => console.error("Failed to fetch tasks:", err));
  }, []);

  // Update current time every second
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const renderMainContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard bots={bots} tasks={tasks} />;
      case 'bots':
        return <Bots bots={bots} />;
      case 'tasks':
        return <Tasks tasks={tasks} />;
      case 'voice':
        return <VoiceControl />;
      case 'prescriptions':
        return (
          // <PlaceholderPage
          //   icon={Pill}
          //   title="Prescriptions"
          //   description="Prescription management coming soon..."
          // />
          <Prescriptions />
        );
      case 'scribing':
        return (
          <PlaceholderPage
            icon={FileText}
            title="Scribing"
            description="Note-taking interface coming soon..."
          />
        );
      case 'patients':
        return (
          <Patients patients={ patients } />
        );
      case 'settings':
        return (
          <PlaceholderPage
            icon={Settings}
            title="Settings"
            description="System configuration coming soon..."
          />
        );
      default:
        return <Dashboard bots={bots} tasks={tasks} />;
    }
  };

  return (
    <div className="app">
      <Header currentTime={currentTime} />

      <div className="layout">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

        <main className="main">
          {renderMainContent()}
        </main>
      </div>
    </div>
  );
};

export default PorterUI;