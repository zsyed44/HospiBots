import React from 'react';

const PlaceholderPage = ({ icon: Icon, title, description }) => {
  return (
    <div className="placeholder">
      <Icon size={64} />
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
};

export default PlaceholderPage;