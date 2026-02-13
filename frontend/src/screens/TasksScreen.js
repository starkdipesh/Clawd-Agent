import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  Modal,
} from 'react-native';
import { Text, ActivityIndicator } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, TASK_PRIORITIES, TASK_STATUSES } from '../utils/constants';
import { taskAPI } from '../services/api';
import { storage } from '../utils/storage';

export default function TasksScreen() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    priority: 'medium',
  });
  const [filter, setFilter] = useState('all'); // all, pending, completed

  useEffect(() => {
    loadUser();
  }, []);

  useEffect(() => {
    if (user) {
      loadTasks();
    }
  }, [user, filter]);

  const loadUser = async () => {
    const userData = await storage.getUser();
    setUser(userData);
  };

  const loadTasks = async () => {
    try {
      setLoading(true);
      const status = filter === 'all' ? null : filter;
      const tasksData = await taskAPI.getTasks(user.user_id, status);
      setTasks(tasksData);
    } catch (error) {
      console.error('Error loading tasks:', error);
      Alert.alert('Error', 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async () => {
    if (!newTask.title.trim()) {
      Alert.alert('Error', 'Task title is required');
      return;
    }

    try {
      await taskAPI.createTask(
        user.user_id,
        newTask.title,
        newTask.description,
        null,
        newTask.priority
      );
      setNewTask({ title: '', description: '', priority: 'medium' });
      setModalVisible(false);
      loadTasks();
    } catch (error) {
      console.error('Error creating task:', error);
      Alert.alert('Error', 'Failed to create task');
    }
  };

  const handleCompleteTask = async (taskId, currentStatus) => {
    try {
      if (currentStatus === 'completed') {
        await taskAPI.updateTask(taskId, { status: 'pending' });
      } else {
        await taskAPI.completeTask(taskId);
      }
      loadTasks();
    } catch (error) {
      console.error('Error updating task:', error);
      Alert.alert('Error', 'Failed to update task');
    }
  };

  const handleDeleteTask = (taskId) => {
    Alert.alert(
      'Delete Task',
      'Are you sure you want to delete this task?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              await taskAPI.deleteTask(taskId);
              loadTasks();
            } catch (error) {
              console.error('Error deleting task:', error);
              Alert.alert('Error', 'Failed to delete task');
            }
          },
        },
      ]
    );
  };

  const renderTask = (task) => {
    const isCompleted = task.status === 'completed';
    const priorityInfo = TASK_PRIORITIES[task.priority] || TASK_PRIORITIES.medium;

    return (
      <View key={task.task_id} style={styles.taskCard}>
        <TouchableOpacity
          style={styles.taskCheckbox}
          onPress={() => handleCompleteTask(task.task_id, task.status)}
        >
          <Ionicons
            name={isCompleted ? 'checkmark-circle' : 'ellipse-outline'}
            size={28}
            color={isCompleted ? COLORS.success : COLORS.textSecondary}
          />
        </TouchableOpacity>

        <View style={styles.taskContent}>
          <Text
            style={[
              styles.taskTitle,
              isCompleted && styles.taskTitleCompleted,
            ]}
          >
            {task.title}
          </Text>
          {task.description && (
            <Text style={styles.taskDescription}>{task.description}</Text>
          )}
          <View style={styles.taskMeta}>
            <View
              style={[
                styles.priorityBadge,
                { backgroundColor: priorityInfo.color + '20' },
              ]}
            >
              <Text style={[styles.priorityText, { color: priorityInfo.color }]}>
                {priorityInfo.label}
              </Text>
            </View>
          </View>
        </View>

        <TouchableOpacity
          style={styles.deleteButton}
          onPress={() => handleDeleteTask(task.task_id)}
        >
          <Ionicons name="trash-outline" size={20} color={COLORS.error} />
        </TouchableOpacity>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Tasks</Text>
        <TouchableOpacity
          style={styles.addButton}
          onPress={() => setModalVisible(true)}
        >
          <Ionicons name="add" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      <View style={styles.filters}>
        {['all', 'pending', 'completed'].map((f) => (
          <TouchableOpacity
            key={f}
            style={[
              styles.filterButton,
              filter === f && styles.filterButtonActive,
            ]}
            onPress={() => setFilter(f)}
          >
            <Text
              style={[
                styles.filterText,
                filter === f && styles.filterTextActive,
              ]}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={COLORS.primary} />
        </View>
      ) : (
        <ScrollView style={styles.tasksContainer}>
          {tasks.length === 0 ? (
            <View style={styles.emptyContainer}>
              <Ionicons name="list-outline" size={64} color={COLORS.textSecondary} />
              <Text style={styles.emptyText}>No tasks yet</Text>
              <Text style={styles.emptySubtext}>Tap + to create your first task</Text>
            </View>
          ) : (
            tasks.map(renderTask)
          )}
        </ScrollView>
      )}

      <Modal
        visible={modalVisible}
        animationType="slide"
        transparent={true}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>New Task</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Ionicons name="close" size={24} color={COLORS.text} />
              </TouchableOpacity>
            </View>

            <TextInput
              style={styles.input}
              placeholder="Task title"
              value={newTask.title}
              onChangeText={(text) => setNewTask({ ...newTask, title: text })}
              placeholderTextColor={COLORS.textSecondary}
            />

            <TextInput
              style={[styles.input, styles.textArea]}
              placeholder="Description (optional)"
              value={newTask.description}
              onChangeText={(text) => setNewTask({ ...newTask, description: text })}
              multiline
              numberOfLines={4}
              placeholderTextColor={COLORS.textSecondary}
            />

            <Text style={styles.label}>Priority</Text>
            <View style={styles.prioritySelector}>
              {Object.keys(TASK_PRIORITIES).map((priority) => (
                <TouchableOpacity
                  key={priority}
                  style={[
                    styles.priorityOption,
                    newTask.priority === priority && styles.priorityOptionActive,
                    { borderColor: TASK_PRIORITIES[priority].color },
                  ]}
                  onPress={() => setNewTask({ ...newTask, priority })}
                >
                  <Text
                    style={[
                      styles.priorityOptionText,
                      { color: TASK_PRIORITIES[priority].color },
                    ]}
                  >
                    {TASK_PRIORITIES[priority].label}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>

            <TouchableOpacity
              style={styles.createButton}
              onPress={handleCreateTask}
            >
              <Text style={styles.createButtonText}>Create Task</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  addButton: {
    backgroundColor: COLORS.primary,
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  filters: {
    flexDirection: 'row',
    padding: 16,
    gap: 8,
  },
  filterButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: COLORS.surface,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  filterButtonActive: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  filterText: {
    color: COLORS.text,
    fontSize: 14,
    fontWeight: '500',
  },
  filterTextActive: {
    color: '#fff',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  tasksContainer: {
    flex: 1,
    padding: 16,
  },
  taskCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  taskCheckbox: {
    marginRight: 12,
  },
  taskContent: {
    flex: 1,
  },
  taskTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  taskTitleCompleted: {
    textDecorationLine: 'line-through',
    color: COLORS.textSecondary,
  },
  taskDescription: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 8,
  },
  taskMeta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  priorityBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  priorityText: {
    fontSize: 12,
    fontWeight: '600',
  },
  deleteButton: {
    padding: 4,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 64,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginTop: 16,
  },
  emptySubtext: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: 8,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: COLORS.surface,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    padding: 24,
    maxHeight: '80%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  input: {
    backgroundColor: COLORS.background,
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
    color: COLORS.text,
  },
  textArea: {
    height: 100,
    textAlignVertical: 'top',
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  prioritySelector: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 24,
  },
  priorityOption: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    borderWidth: 2,
    alignItems: 'center',
    backgroundColor: COLORS.surface,
  },
  priorityOptionActive: {
    backgroundColor: COLORS.background,
  },
  priorityOptionText: {
    fontSize: 14,
    fontWeight: '600',
  },
  createButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  createButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});