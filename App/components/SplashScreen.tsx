import React, { useEffect, useRef } from "react";
import { View, Text, Animated, StyleSheet } from "react-native";
import * as expoScreen from "expo-splash-screen";

expoScreen.preventAutoHideAsync();

export default function SplashScreen() {
  const fadeAnim = useRef(new Animated.Value(0)).current; 
  const translateYAnim = useRef(new Animated.Value(50)).current;

  useEffect(() => {
    Animated.sequence([
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 2000,
          useNativeDriver: true,
        }),
        Animated.timing(translateYAnim, {
          toValue: 0,
          duration: 2000,
          useNativeDriver: true,
        }),
      ]),
    ]).start(() => {
      expoScreen.hideAsync(); 
        });
  }, [fadeAnim, translateYAnim]);

  return (
    <View style={styles.container}>
      <Animated.Text
        style={[
          styles.animatedText,
          {
            opacity: fadeAnim, // Bind opacity to animated value
            transform: [{ translateY: translateYAnim }], // Bind Y translation
          },
        ]}
      >
        Irrigo
      </Animated.Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#ffffff", // Change this to the background color you want
  },
  animatedText: {
    fontSize: 48,
    fontWeight: "bold",
    color: "#4CAF50", // Customize text color (Irrigo green, for example)
  },
});
