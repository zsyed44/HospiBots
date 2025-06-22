import React from 'react';
import { Search, Plus } from 'lucide-react';
import TaskItem from '../components/TaskItem';

const Tasks = ({ tasks }) => {
  return (
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
};

export default Tasks;