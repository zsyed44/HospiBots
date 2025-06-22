import React from 'react';
import {
  Bot,
  Package,
  FileText,
  Pill,
  Users,
  Settings,
  Activity,
  Mic
} from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
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
  );
};

export default Sidebar;