import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Alert,
  TextInput,
  Modal,
} from 'react-native';
import { Text, ActivityIndicator, Card, Chip } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../utils/constants';
import { messagingAPI } from '../services/api';
import { storage } from '../utils/storage';

const PLATFORMS = [
  { id: 'telegram', name: 'Telegram', icon: 'paper-plane', color: '#0088cc' },
  { id: 'discord', name: 'Discord', icon: 'logo-discord', color: '#5865F2' },
  { id: 'whatsapp', name: 'WhatsApp', icon: 'logo-whatsapp', color: '#25D366' },
  { id: 'slack', name: 'Slack', icon: 'logo-slack', color: '#4A154B' },
];

export default function MessagingScreen() {
  const [bots, setBots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [user, setUser] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [botName, setBotName] = useState('');
  const [botToken, setBotToken] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadUser();
  }, []);

  useEffect(() => {
    if (user) {
      loadBots();
    }
  }, [user]);

  const loadUser = async () => {
    const userData = await storage.getUser();
    setUser(userData);
  };

  const loadBots = async () => {
    try {
      setLoading(true);
      const response = await messagingAPI.getBots(user.user_id);
      setBots(response.bots);
    } catch (error) {
      console.error('Error loading bots:', error);
      Alert.alert('Error', 'Failed to load bot configurations');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    loadBots();
  };

  const handleAddBot = (platform) => {
    setSelectedPlatform(platform);
    setBotName('');
    setBotToken('MOCK_TOKEN');
    setShowAddModal(true);
  };

  const handleSaveBot = async () => {
    if (!botName.trim()) {
      Alert.alert('Error', 'Please enter a bot name');
      return;
    }

    setSaving(true);
    try {
      await messagingAPI.createBot({
        user_id: user.user_id,
        platform: selectedPlatform.id,
        bot_name: botName,
        bot_token: botToken || 'MOCK_TOKEN',
        settings: {},
      });

      Alert.alert('Success', `${selectedPlatform.name} bot configured!`);
      setShowAddModal(false);
      loadBots();
    } catch (error) {
      console.error('Error creating bot:', error);
      Alert.alert('Error', error.response?.data?.detail || 'Failed to create bot');
    } finally {
      setSaving(false);
    }
  };

  const handleToggleBot = async (bot) => {
    try {
      await messagingAPI.toggleBot(bot.bot_id, !bot.enabled);
      loadBots();
    } catch (error) {
      console.error('Error toggling bot:', error);
      Alert.alert('Error', 'Failed to toggle bot');
    }
  };

  const handleDeleteBot = async (bot) => {
    Alert.alert(
      'Delete Bot',
      `Are you sure you want to delete ${bot.bot_name}?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              await messagingAPI.deleteBot(bot.bot_id);
              loadBots();
            } catch (error) {
              console.error('Error deleting bot:', error);
              Alert.alert('Error', 'Failed to delete bot');
            }
          },
        },
      ]
    );
  };

  const getPlatformIcon = (platformId) => {
    const platform = PLATFORMS.find((p) => p.id === platformId);
    return platform ? platform.icon : 'chatbubble';
  };

  const getPlatformColor = (platformId) => {
    const platform = PLATFORMS.find((p) => p.id === platformId);
    return platform ? platform.color : COLORS.primary;
  };

  const renderBot = (bot) => {
    const platformColor = getPlatformColor(bot.platform);
    const stats = bot.stats || {};

    return (
      <Card key={bot.bot_id} style={styles.botCard}>
        <View style={styles.botHeader}>
          <View style={styles.botInfo}>
            <View style={[styles.platformIcon, { backgroundColor: platformColor }]}>
              <Ionicons
                name={getPlatformIcon(bot.platform)}
                size={24}
                color="#fff"
              />
            </View>
            <View style={styles.botDetails}>
              <Text style={styles.botName}>{bot.bot_name}</Text>
              <Text style={styles.botPlatform}>{bot.platform}</Text>
            </View>
          </View>
          <Chip
            style={[
              styles.statusChip,
              { backgroundColor: bot.enabled ? COLORS.success : COLORS.error },
            ]}
            textStyle={styles.statusChipText}
          >
            {bot.enabled ? 'Active' : 'Inactive'}
          </Chip>
        </View>

        <View style={styles.statsContainer}>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{stats.total_messages || 0}</Text>
            <Text style={styles.statLabel}>Messages</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{stats.incoming_messages || 0}</Text>
            <Text style={styles.statLabel}>Received</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{stats.outgoing_messages || 0}</Text>
            <Text style={styles.statLabel}>Sent</Text>
          </View>
        </View>

        <View style={styles.botActions}>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => handleToggleBot(bot)}
          >
            <Ionicons
              name={bot.enabled ? 'pause' : 'play'}
              size={20}
              color={COLORS.primary}
            />
            <Text style={styles.actionButtonText}>
              {bot.enabled ? 'Disable' : 'Enable'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => handleDeleteBot(bot)}
          >
            <Ionicons name="trash" size={20} color={COLORS.error} />
            <Text style={[styles.actionButtonText, { color: COLORS.error }]}>
              Delete
            </Text>
          </TouchableOpacity>
        </View>
      </Card>
    );
  };

  const renderAddModal = () => (
    <Modal
      visible={showAddModal}
      transparent
      animationType="slide"
      onRequestClose={() => setShowAddModal(false)}
    >
      <View style={styles.modalContainer}>
        <View style={styles.modalContent}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>
              Add {selectedPlatform?.name} Bot
            </Text>
            <TouchableOpacity onPress={() => setShowAddModal(false)}>
              <Ionicons name="close" size={24} color={COLORS.text} />
            </TouchableOpacity>
          </View>

          <TextInput
            style={styles.input}
            placeholder="Bot Name"
            value={botName}
            onChangeText={setBotName}
            placeholderTextColor={COLORS.textSecondary}
          />

          <TextInput
            style={styles.input}
            placeholder="Bot Token (Use MOCK_TOKEN for testing)"
            value={botToken}
            onChangeText={setBotToken}
            placeholderTextColor={COLORS.textSecondary}
            secureTextEntry
          />

          <Text style={styles.helperText}>
            💡 Use "MOCK_TOKEN" for testing. Add real token later in settings.
          </Text>

          <TouchableOpacity
            style={[styles.saveButton, saving && styles.saveButtonDisabled]}
            onPress={handleSaveBot}
            disabled={saving}
          >
            {saving ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.saveButtonText}>Add Bot</Text>
            )}
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title}>Messaging Integrations</Text>
          <Text style={styles.subtitle}>
            Connect your messaging platforms to Moltbot
          </Text>
        </View>

        {bots.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Connected Bots</Text>
            {bots.map((bot) => renderBot(bot))}
          </View>
        )}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Add New Platform</Text>
          <View style={styles.platformsGrid}>
            {PLATFORMS.map((platform) => {
              const isConnected = bots.some((b) => b.platform === platform.id);
              return (
                <TouchableOpacity
                  key={platform.id}
                  style={[
                    styles.platformCard,
                    isConnected && styles.platformCardConnected,
                  ]}
                  onPress={() => !isConnected && handleAddBot(platform)}
                  disabled={isConnected}
                >
                  <View
                    style={[
                      styles.platformIconLarge,
                      { backgroundColor: platform.color },
                    ]}
                  >
                    <Ionicons name={platform.icon} size={32} color="#fff" />
                  </View>
                  <Text style={styles.platformName}>{platform.name}</Text>
                  {isConnected && (
                    <Chip
                      style={styles.connectedChip}
                      textStyle={styles.connectedChipText}
                    >
                      Connected
                    </Chip>
                  )}
                </TouchableOpacity>
              );
            })}
          </View>
        </View>
      </ScrollView>

      {renderAddModal()}
    </View>
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
  },
  header: {
    padding: 20,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  section: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
  },
  botCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    elevation: 2,
  },
  botHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  botInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  platformIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  botDetails: {
    flex: 1,
  },
  botName: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  botPlatform: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textTransform: 'capitalize',
  },
  statusChip: {
    height: 28,
  },
  statusChipText: {
    fontSize: 12,
    color: '#fff',
    fontWeight: '600',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 12,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: COLORS.border,
    marginBottom: 12,
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  botActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
  },
  actionButtonText: {
    marginLeft: 4,
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '500',
  },
  platformsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  platformCard: {
    width: '48%',
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginBottom: 12,
    borderWidth: 2,
    borderColor: COLORS.border,
  },
  platformCardConnected: {
    opacity: 0.6,
    borderColor: COLORS.success,
  },
  platformIconLarge: {
    width: 64,
    height: 64,
    borderRadius: 32,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  platformName: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  connectedChip: {
    backgroundColor: COLORS.success,
    marginTop: 4,
  },
  connectedChipText: {
    color: '#fff',
    fontSize: 10,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: COLORS.surface,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    padding: 20,
    minHeight: 400,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  modalTitle: {
    fontSize: 20,
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
  helperText: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginBottom: 20,
    fontStyle: 'italic',
  },
  saveButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  saveButtonDisabled: {
    opacity: 0.6,
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
