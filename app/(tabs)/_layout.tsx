import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import DetectScreen from './detect';

export default function AppLayout() {
  return (
    <View style={{ flex: 1, backgroundColor: '#0b1220' }}>
      <AppHeader />
      <DetectScreen />
    </View>
  );
}

function AppHeader() {
  return (
    <View style={styles.headerContainer}>
      <Text style={styles.appBadge}>IoT</Text>
      <Text style={styles.headerTitle}>Mobile IoT Detector</Text>
      <Text style={styles.headerSubtitle}>Nhận diện board • Camera / Thư viện</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  headerContainer: {
    backgroundColor: '#0b1220', // nền tối giống mockup
    paddingTop: 52,
    paddingBottom: 16,
    paddingHorizontal: 20,
    alignItems: 'center',
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.18,
    shadowRadius: 12,
    elevation: 10,
  },
  appBadge: {
    color: '#22c55e',
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 1.5,
    textTransform: 'uppercase',
    opacity: 0.9,
  },
  headerTitle: {
    color: '#fff',
    fontSize: 24,
    fontWeight: '800',
    letterSpacing: 0.8,
    marginTop: 4,
  },
  headerSubtitle: {
    color: '#93a3b8',
    fontSize: 12,
    marginTop: 6,
  },
  // Xóa style tab bar detect pill
});
