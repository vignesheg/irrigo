import React, { useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, TextInput } from "react-native";
import { initializeApp } from "firebase/app";
import { getDatabase, ref, update } from "firebase/database";

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDymuoSQrB855PmttCpUbiOlp6Ag4iraIA",
    authDomain: "irrigo-dfb76.firebaseapp.com",
    databaseURL: "https://irrigo-dfb76-default-rtdb.firebaseio.com",
    projectId: "irrigo-dfb76",
    storageBucket: "irrigo-dfb76.appspot.com",
    messagingSenderId: "962205265859",
    appId: "1:962205265859:web:4bd3bdc9336d24d9c19776",
    measurementId: "G-743R2SL793"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

export default function ManualMode({ navigation }) {
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");

  // Function to update manstarttime and manendtime in the database
  const updateStartEndTime = () => {
    const statusRef = ref(db, 'statuses');

    update(statusRef, {
      manstarttime: startTime, // Update manstarttime
      manendtime: endTime,     // Update manendtime
      mode: 2, // Update mode
    })
    .then(() => {
      console.log("Start and End time updated successfully");
      navigation.goBack(); // Go back to home after updating the time
    })
    .catch((error) => {
      console.error("Error updating time:", error);
    });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.Title}>Manual Mode</Text>
      
      <View style={styles.timingCard}>
        <Text style={styles.name}>Set Start Time</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter Start Time"
          value={startTime}
          onChangeText={setStartTime}
        />
      </View>

      <View style={styles.timingCard}>
        <Text style={styles.name}>Set End Time</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter End Time"
          value={endTime}
          onChangeText={setEndTime}
        />
      </View>

      <TouchableOpacity style={styles.button} onPress={updateStartEndTime}>
        <Text style={styles.buttonText}>Update Time</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#eaeaea",
    padding: 20,
  },
  Title: {
    fontSize: 36,
    fontWeight: "bold",
    marginBottom: 20,
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
  },
  name: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 10,
    textAlign: "center",
  },
  timingCard: {
    textAlign: "center",
    display: "flex",
    alignItems: "center",
    backgroundColor: "#fff",
    flex: 1,
    marginLeft: 10,
    marginRight: 10,
    height: 100,
    marginTop: 20,
    borderRadius: 10,
    padding: 20,
  },
  input: {
    width: "100%",
    height: 40,
    borderColor: "gray",
    borderWidth: 1,
    borderRadius: 5,
    paddingLeft: 10,
    marginTop: 10,
  },
  button: {
    backgroundColor: "#000",
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 30,
    marginTop: 25,
    elevation: 5,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "bold",
    textAlign: "center",
  },
});
