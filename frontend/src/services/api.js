import axios from 'axios';
import { BACKEND_URL } from '../utils/constants';

const apiClient = axios.create({
  baseURL: BACKEND_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  sendMessage: async (userId, message, conversationId = null) => {
    const response = await apiClient.post('/api/chat/message', {
      user_id: userId,
      message,
      conversation_id: conversationId,
      use_voice: false,
    });
    return response.data;
  },

  getConversations: async (userId) => {
    const response = await apiClient.get(`/api/chat/conversations/${userId}`);
    return response.data.conversations;
  },

  getMessages: async (conversationId, limit = 50) => {
    const response = await apiClient.get(`/api/chat/messages/${conversationId}`, {
      params: { limit },
    });
    return response.data.messages;
  },

  deleteConversation: async (conversationId) => {
    const response = await apiClient.delete(`/api/chat/conversation/${conversationId}`);
    return response.data;
  },
};

export const taskAPI = {
  createTask: async (userId, title, description, dueDate, priority) => {
    const response = await apiClient.post('/api/tasks/create', {
      user_id: userId,
      title,
      description,
      due_date: dueDate,
      priority,
    });
    return response.data;
  },

  getTasks: async (userId, status = null, priority = null) => {
    const response = await apiClient.get(`/api/tasks/list/${userId}`, {
      params: { status, priority },
    });
    return response.data.tasks;
  },

  getUpcomingTasks: async (userId, hours = 24) => {
    const response = await apiClient.get(`/api/tasks/upcoming/${userId}`, {
      params: { hours },
    });
    return response.data.tasks;
  },

  completeTask: async (taskId) => {
    const response = await apiClient.put(`/api/tasks/complete/${taskId}`);
    return response.data;
  },

  updateTask: async (taskId, updates) => {
    const response = await apiClient.put(`/api/tasks/update/${taskId}`, updates);
    return response.data;
  },

  deleteTask: async (taskId) => {
    const response = await apiClient.delete(`/api/tasks/delete/${taskId}`);
    return response.data;
  },
};

export const skillAPI = {
  getAllSkills: async () => {
    const response = await apiClient.get('/api/skills/list');
    return response.data.skills;
  },

  getEnabledSkills: async (userId = null) => {
    const response = await apiClient.get('/api/skills/enabled', {
      params: { user_id: userId },
    });
    return response.data.skills;
  },

  enableSkill: async (skillId) => {
    const response = await apiClient.put(`/api/skills/enable/${skillId}`);
    return response.data;
  },

  disableSkill: async (skillId) => {
    const response = await apiClient.put(`/api/skills/disable/${skillId}`);
    return response.data;
  },

  installDefaultSkills: async () => {
    const response = await apiClient.post('/api/skills/install-defaults');
    return response.data;
  },
};

export const userAPI = {
  createUser: async (name, email = null, phone = null) => {
    const response = await apiClient.post('/api/users/create', {
      name,
      email,
      phone,
      preferences: {},
    });
    return response.data;
  },

  getUser: async (userId) => {
    const response = await apiClient.get(`/api/users/get/${userId}`);
    return response.data;
  },

  updateUser: async (userId, updates) => {
    const response = await apiClient.put(`/api/users/update/${userId}`, updates);
    return response.data;
  },

  listUsers: async () => {
    const response = await apiClient.get('/api/users/list');
    return response.data.users;
  },
};

export const memoryAPI = {
  storeMemory: async (userId, key, value, context = '', importance = 5) => {
    const response = await apiClient.post('/api/memory/store', {
      user_id: userId,
      key,
      value,
      context,
      importance,
    });
    return response.data;
  },

  getMemories: async (userId, key = null, limit = 10) => {
    const response = await apiClient.get(`/api/memory/get/${userId}`, {
      params: { key, limit },
    });
    return response.data.memories;
  },

  getUserContext: async (userId) => {
    const response = await apiClient.get(`/api/memory/context/${userId}`);
    return response.data;
  },
};

export const notificationAPI = {
  getNotifications: async (userId, unreadOnly = false, limit = 50) => {
    const response = await apiClient.get(`/api/notifications/list/${userId}`, {
      params: { unread_only: unreadOnly, limit },
    });
    return response.data.notifications;
  },

  markAsRead: async (notificationId) => {
    const response = await apiClient.put(`/api/notifications/read/${notificationId}`);
    return response.data;
  },
};

export const messagingAPI = {
  createBot: async (config) => {
    const response = await apiClient.post('/api/messaging/config/create', config);
    return response.data;
  },

  getBots: async (userId) => {
    const response = await apiClient.get(`/api/messaging/config/list/${userId}`);
    return response.data;
  },

  getBot: async (botId) => {
    const response = await apiClient.get(`/api/messaging/config/get/${botId}`);
    return response.data;
  },

  updateBot: async (botId, updates) => {
    const response = await apiClient.put(`/api/messaging/config/update/${botId}`, updates);
    return response.data;
  },

  deleteBot: async (botId) => {
    const response = await apiClient.delete(`/api/messaging/config/delete/${botId}`);
    return response.data;
  },

  toggleBot: async (botId, enabled) => {
    const response = await apiClient.put(`/api/messaging/config/toggle/${botId}`, { enabled });
    return response.data;
  },

  sendMessage: async (botId, recipient, message, metadata = {}) => {
    const response = await apiClient.post(`/api/messaging/send/${botId}`, {
      recipient,
      message,
      metadata,
    });
    return response.data;
  },

  getMessages: async (botId, limit = 50) => {
    const response = await apiClient.get(`/api/messaging/messages/${botId}`, {
      params: { limit },
    });
    return response.data;
  },
};

export default apiClient;