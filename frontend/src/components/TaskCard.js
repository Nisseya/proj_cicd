import React from 'react';
import { useTask } from '../contexts/TaskContext';
import PropTypes from 'prop-types';

const TaskCard = ({ task, onEditTask }) => {
  const { deleteTask } = useTask();

  return (
    <div className="task-card">
      <h3>{task.title}</h3>
      <p>{task.description}</p>
      <p>Priority: {task.priority}</p>
      <p>Assigned to: {task.assignedTo || 'Unassigned'}</p>
      <p>Status: {task.status}</p>
      <p>Created at: {task.createdAt}</p>
      <button onClick={() => onEditTask(task)}>Edit</button>
      <button onClick={() => deleteTask(task.id)}>Delete</button>
    </div>
  );
};

TaskCard.propTypes = {
  task: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    title: PropTypes.string.isRequired,
    description: PropTypes.string,
    priority: PropTypes.oneOf(['high', 'medium', 'low']).isRequired,
    assignedTo: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    status: PropTypes.oneOf(['todo', 'progress', 'done']).isRequired,
    createdAt: PropTypes.string.isRequired,
  }).isRequired,
  onEditTask: PropTypes.func.isRequired,
};

export default TaskCard;
