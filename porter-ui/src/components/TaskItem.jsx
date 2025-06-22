import React from 'react';
import { MoreVertical } from 'lucide-react';

const TaskItem = ({ task }) => {
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
};

export default TaskItem;