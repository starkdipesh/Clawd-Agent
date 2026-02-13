import React, { useState, useEffect } from 'react';
import {
  View,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import { Text, ActivityIndicator } from 'react-native-paper';
import { COLORS } from '../utils/constants';
import { userAPI } from '../services/api';
import { storage } from '../utils/storage';

export default function WelcomeScreen({ navigation }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    checkExistingUser();
  }, []);

  const checkExistingUser = async () => {
    try {
      const user = await storage.getUser();
      if (user) {
        navigation.replace('Main');
      }
    } catch (error) {
      console.error('Error checking user:', error);
    } finally {
      setChecking(false);
    }
  };

  const handleGetStarted = async () => {
    if (!name.trim()) {
      Alert.alert('Error', 'Please enter your name');
      return;
    }

    setLoading(true);
    try {
      const response = await userAPI.createUser(name, email || null);
      const user = {
        user_id: response.user_id,
        name: response.name,
        email: email || null,
      };
      await storage.saveUser(user);
      navigation.replace('Main');
    } catch (error) {
      console.error('Error creating user:', error);
      Alert.alert('Error', 'Failed to create user. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (checking) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <View style={styles.content}>
        <Text style={styles.title}>Welcome to Moltbot</Text>
        <Text style={styles.subtitle}>
          Your AI-powered personal assistant
        </Text>

        <View style={styles.form}>
          <TextInput
            style={styles.input}
            placeholder="What's your name?"
            value={name}
            onChangeText={setName}
            placeholderTextColor={COLORS.textSecondary}
          />
          <TextInput
            style={styles.input}
            placeholder="Email (optional)"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
            placeholderTextColor={COLORS.textSecondary}
          />

          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={handleGetStarted}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.buttonText}>Get Started</Text>
            )}
          </TouchableOpacity>
        </View>

        <View style={styles.features}>
          <Text style={styles.featureText}>✨ AI Chat Assistant</Text>
          <Text style={styles.featureText}>🧠 Persistent Memory</Text>
          <Text style={styles.featureText}>📋 Task Management</Text>
          <Text style={styles.featureText}>🎯 Smart Skills</Text>
          <Text style={styles.featureText}>🔔 Proactive Notifications</Text>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
  content: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginBottom: 48,
    textAlign: 'center',
  },
  form: {
    marginBottom: 32,
  },
  input: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
    color: COLORS.text,
  },
  button: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  features: {
    alignItems: 'center',
  },
  featureText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 8,
  },
});