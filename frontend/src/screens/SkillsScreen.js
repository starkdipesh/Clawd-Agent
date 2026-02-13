import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Alert,
  Switch,
} from 'react-native';
import { Text, ActivityIndicator } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../utils/constants';
import { skillAPI } from '../services/api';

const SKILL_ICONS = {
  Information: 'information-circle',
  Productivity: 'checkmark-circle',
  Communication: 'chatbubbles',
  Entertainment: 'game-controller',
  Utilities: 'construct',
};

export default function SkillsScreen() {
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSkills();
  }, []);

  const loadSkills = async () => {
    try {
      setLoading(true);
      const skillsData = await skillAPI.getAllSkills();
      setSkills(skillsData);
    } catch (error) {
      console.error('Error loading skills:', error);
      Alert.alert('Error', 'Failed to load skills');
    } finally {
      setLoading(false);
    }
  };

  const toggleSkill = async (skillId, currentlyEnabled) => {
    try {
      if (currentlyEnabled) {
        await skillAPI.disableSkill(skillId);
      } else {
        await skillAPI.enableSkill(skillId);
      }
      loadSkills();
    } catch (error) {
      console.error('Error toggling skill:', error);
      Alert.alert('Error', 'Failed to toggle skill');
    }
  };

  const renderSkill = (skill) => {
    const icon = SKILL_ICONS[skill.category] || 'star';

    return (
      <View key={skill.skill_id} style={styles.skillCard}>
        <View style={styles.skillIcon}>
          <Ionicons name={icon} size={32} color={COLORS.primary} />
        </View>

        <View style={styles.skillContent}>
          <Text style={styles.skillName}>{skill.name}</Text>
          <Text style={styles.skillDescription}>{skill.description}</Text>
          <View style={styles.skillMeta}>
            <View style={styles.categoryBadge}>
              <Text style={styles.categoryText}>{skill.category}</Text>
            </View>
            <Text style={styles.versionText}>v{skill.version}</Text>
          </View>
        </View>

        <Switch
          value={skill.enabled}
          onValueChange={() => toggleSkill(skill.skill_id, skill.enabled)}
          trackColor={{ false: COLORS.border, true: COLORS.primary }}
          thumbColor={skill.enabled ? '#fff' : COLORS.textSecondary}
        />
      </View>
    );
  };

  const groupSkillsByCategory = () => {
    const grouped = {};
    skills.forEach((skill) => {
      if (!grouped[skill.category]) {
        grouped[skill.category] = [];
      }
      grouped[skill.category].push(skill);
    });
    return grouped;
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  const groupedSkills = groupSkillsByCategory();

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Skills</Text>
        <Text style={styles.headerSubtitle}>
          {skills.filter((s) => s.enabled).length} of {skills.length} enabled
        </Text>
      </View>

      <ScrollView style={styles.scrollContainer}>
        {skills.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Ionicons name="extension-puzzle" size={64} color={COLORS.textSecondary} />
            <Text style={styles.emptyText}>No skills available</Text>
            <Text style={styles.emptySubtext}>Skills will appear here once loaded</Text>
          </View>
        ) : (
          Object.keys(groupedSkills).map((category) => (
            <View key={category} style={styles.categorySection}>
              <Text style={styles.categoryTitle}>{category}</Text>
              {groupedSkills[category].map(renderSkill)}
            </View>
          ))
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
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
  headerSubtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scrollContainer: {
    flex: 1,
  },
  categorySection: {
    padding: 16,
  },
  categoryTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  skillCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: COLORS.border,
    alignItems: 'center',
  },
  skillIcon: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: COLORS.primary + '15',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  skillContent: {
    flex: 1,
  },
  skillName: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  skillDescription: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 8,
  },
  skillMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  categoryBadge: {
    backgroundColor: COLORS.background,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  categoryText: {
    fontSize: 12,
    color: COLORS.textSecondary,
    fontWeight: '500',
  },
  versionText: {
    fontSize: 12,
    color: COLORS.textSecondary,
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
});