import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  ScrollView,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import { Text, ActivityIndicator } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import * as Speech from 'expo-speech';
import { COLORS } from '../utils/constants';
import { chatAPI } from '../services/api';
import { storage } from '../utils/storage';

export default function ChatScreen() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const scrollViewRef = useRef();

  useEffect(() => {
    loadUser();
  }, []);

  useEffect(() => {
    if (user) {
      loadConversationHistory();
    }
  }, [user]);

  const loadUser = async () => {
    const userData = await storage.getUser();
    setUser(userData);
  };

  const loadConversationHistory = async () => {
    try {
      const conversations = await chatAPI.getConversations(user.user_id);
      if (conversations.length > 0) {
        const latestConv = conversations[0];
        setConversationId(latestConv.conversation_id);
        const msgs = await chatAPI.getMessages(latestConv.conversation_id);
        setMessages(msgs);
      } else {
        // Welcome message
        setMessages([{
          role: 'assistant',
          content: `Hello ${user.name}! I'm Moltbot, your AI assistant. How can I help you today?`,
          timestamp: new Date().toISOString(),
        }]);
      }
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const handleSend = async () => {
    if (!inputText.trim() || !user) return;

    const userMessage = {
      role: 'user',
      content: inputText,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      const response = await chatAPI.sendMessage(
        user.user_id,
        inputText,
        conversationId
      );

      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      const assistantMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      Alert.alert('Error', 'Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const speakText = (text) => {
    Speech.speak(text, {
      language: 'en',
      pitch: 1,
      rate: 0.9,
    });
  };

  const renderMessage = (message, index) => {
    const isUser = message.role === 'user';
    return (
      <View
        key={index}
        style={[
          styles.messageBubble,
          isUser ? styles.userBubble : styles.assistantBubble,
        ]}
      >
        <Text
          style={[
            styles.messageText,
            isUser ? styles.userText : styles.assistantText,
          ]}
        >
          {message.content}
        </Text>
        {!isUser && (
          <TouchableOpacity
            style={styles.speakButton}
            onPress={() => speakText(message.content)}
          >
            <Ionicons name="volume-medium" size={16} color={COLORS.primary} />
          </TouchableOpacity>
        )}
      </View>
    );
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={90}
    >
      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
        onContentSizeChange={() => scrollViewRef.current?.scrollToEnd()}
      >
        {messages.map((message, index) => renderMessage(message, index))}
        {loading && (
          <View style={styles.loadingBubble}>
            <ActivityIndicator size="small" color={COLORS.primary} />
            <Text style={styles.loadingText}>Thinking...</Text>
          </View>
        )}
      </ScrollView>

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Type a message..."
          value={inputText}
          onChangeText={setInputText}
          onSubmitEditing={handleSend}
          multiline
          placeholderTextColor={COLORS.textSecondary}
        />
        <TouchableOpacity
          style={[styles.sendButton, !inputText.trim() && styles.sendButtonDisabled]}
          onPress={handleSend}
          disabled={!inputText.trim() || loading}
        >
          <Ionicons name="send" size={24} color="#fff" />
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 16,
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 16,
    marginBottom: 12,
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: COLORS.userMessage,
  },
  assistantBubble: {
    alignSelf: 'flex-start',
    backgroundColor: COLORS.assistantMessage,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  userText: {
    color: '#fff',
  },
  assistantText: {
    color: COLORS.text,
  },
  speakButton: {
    marginTop: 8,
    alignSelf: 'flex-end',
  },
  loadingBubble: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    backgroundColor: COLORS.assistantMessage,
    padding: 12,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  loadingText: {
    marginLeft: 8,
    color: COLORS.textSecondary,
    fontSize: 14,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 16,
    backgroundColor: COLORS.surface,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    alignItems: 'center',
  },
  input: {
    flex: 1,
    backgroundColor: COLORS.background,
    borderRadius: 24,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
    maxHeight: 100,
    marginRight: 8,
    color: COLORS.text,
  },
  sendButton: {
    backgroundColor: COLORS.primary,
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    opacity: 0.5,
  },
});