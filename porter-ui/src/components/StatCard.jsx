import React from 'react';

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

export default StatCard;