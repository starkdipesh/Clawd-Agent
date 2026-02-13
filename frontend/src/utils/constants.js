import Constants from 'expo-constants';

export const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

export const COLORS = {
  primary: '#6366f1',
  secondary: '#8b5cf6',
  background: '#f8fafc',
  surface: '#ffffff',
  text: '#1e293b',
  textSecondary: '#64748b',
  border: '#e2e8f0',
  error: '#ef4444',
  success: '#10b981',
  warning: '#f59e0b',
  info: '#3b82f6',
  userMessage: '#6366f1',
  assistantMessage: '#f1f5f9',
};

export const TASK_PRIORITIES = {
  low: { label: 'Low', color: '#10b981' },
  medium: { label: 'Medium', color: '#f59e0b' },
  high: { label: 'High', color: '#ef4444' },
};

export const TASK_STATUSES = {
  pending: 'Pending',
  completed: 'Completed',
  cancelled: 'Cancelled',
};