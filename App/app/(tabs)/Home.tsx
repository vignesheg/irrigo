import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Image, TouchableOpacity } from "react-native";
import { initializeApp } from "firebase/app";
import { getDatabase, ref, onValue, query, limitToLast } from "firebase/database";
import { useNavigation } from '@react-navigation/native';
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

export default function Home() {
  const [sensorData, setSensorData] = useState({});
  const [statuses, setStatuses] = useState({
    starttime: "",
    endtime: "",
  });
  const navigation = useNavigation(); // Hook to use navigation

  useEffect(() => {
    // Fetch latest sensor data
    const sensorRef = ref(db, 'sensors');
    onValue(sensorRef, (snapshot) => {
      const data = snapshot.val();
      const latestKey = Object.keys(data).slice(-1)[0]; // Get the latest timestamp entry
      setSensorData(data[latestKey]); // Update sensor data
    });

    // Fetch statuses data (for starttime and endtime)
    const statusRef = ref(db, 'statuses');
    onValue(statusRef, (snapshot) => {
      const statusData = snapshot.val();
      setStatuses({
        starttime: statusData.starttime || "Loading...",
        endtime: statusData.endtime || "Loading..."
      });
    });
  }, []);

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.Title}>Irrigo</Text>
        <View style={styles.blurContainer}>
          <View style={styles.row}>
            <View style={styles.detailsContainer}>
              <Text style={styles.name}>Automatic Mode</Text>

              <View style={styles.fieldDataContainer}>
                <View style={styles.ImageContainer}>
                  <Image
                    style={styles.cloudImage}
                    source={require("../../assets/images/cloud.png")}
                  />
                  <Text style={styles.temperature}>
                    {sensorData.temperature ? `${sensorData.temperature} ºC` : "Loading..."}
                  </Text>
                </View>

                <View style={styles.line}></View>
                <View style={styles.Datas}>
                  <View style={styles.DataValue}>
                    <Text style={styles.values}>Humidity</Text>
                    <Text style={styles.values}>
                      {sensorData.humidity ? `${sensorData.humidity}%` : "Loading..."}
                    </Text>
                  </View>
                  <View style={styles.DataValue}>
                    <Text style={styles.values}>Moisture</Text>
                    <Text style={styles.values}>
                      {sensorData.soilmoisture ? `${sensorData.soilmoisture}%` : "Loading..."}
                    </Text>
                  </View>
                  <View style={styles.DataValue}>
                    <Text style={styles.values}>Wind Speed</Text>
                    <Text style={styles.values}>
                      {sensorData.windspeed ? `${sensorData.windspeed} m/s` : "Loading..."}
                    </Text>
                  </View>
                </View>
              </View>
            </View>
          </View>
        </View>

        <View style={styles.MotorTiming}>
          <View style={styles.timingCard}>
            <Text style={styles.name}>Start Time</Text>
            <Text style={styles.timingValue}>
              {statuses.starttime}
            </Text>
          </View>
          <View style={styles.timingCard}>
            <Text style={styles.name}>End Time</Text>
            <Text style={styles.timingValue}>
              {statuses.endtime}
            </Text>
          </View>
        </View>
      </View>

      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate("ManualMode")}
      >
        <Text style={styles.buttonText}>Manual Mode</Text>
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
  values: {
    marginBottom: 10,
    marginLeft: 10,
    marginRight: 3,
  },
  timingValue: {
    fontSize: 17,
    marginTop: 10,
  },
  MotorTiming: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
  },

  timingCard: {
    textAlign: "center",
    display: "flex",
    alignItems: "center",
    backgroundColor: "#ffff",
    flex: 1,
    marginLeft: 10,
    marginRight: 10,
    height: 130,
    marginTop: 10,
    borderRadius: 10,
    padding: 10,
  },

  line: {
    width: "100%",
    height: 0.5,
    marginTop: 15,
    backgroundColor: "#000",
    marginVertical: 10,
  },

  card: {
    borderRadius: 12,
    overflow: "hidden",
    marginBottom: 20,
  },

  button: {
    backgroundColor: "#000000",
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 30,
    marginTop:25,
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
  blurContainer: {
    backgroundColor: "#ffff",
    marginTop: 10,
    borderRadius: 10,
    marginBottom: 30,
    padding: 10,
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
  },
  avatarContainer: {
    marginRight: 15,
  },

  DataValue: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },

  ImageContainer: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-evenly",
    marginTop: 10,
  },

  temperature: {
    fontSize: 45,
  },
  cloudImage: {
    height: 70,
    width: 70,
  },
  Datas: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
    marginTop: 5,
  },
  fieldDataContainer: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    borderWidth: 2,
    borderColor: "#fff",
  },
  detailsContainer: {
    flex: 1,
  },
  name: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
  },
  position: {
    fontSize: 12,
    color: "gray",
  },
  salaryContainer: {
    marginLeft: "auto",
  },
  salary: {
    fontSize: 16,
    fontWeight: "bold",
  },
});
