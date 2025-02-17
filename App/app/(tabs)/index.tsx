import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Home from "./Home";
import ManualMode from "./manual";
import SplashScreen from "@/components/SplashScreen"; // Update this path to your actual SplashScreen component
import { useState, useEffect } from "react";

const Stack = createNativeStackNavigator();

export default function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading process (adjust to your real loading logic)
    setTimeout(() => {
      setIsLoading(false);
    }, 2000); // Adjust time based on actual loading time
  }, []);

  return (
    <NavigationContainer independent={true}>
      {isLoading ? (
        <SplashScreen />
      ) : (
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen name="HomeScreen" component={Home} />
          <Stack.Screen name="ManualMode" component={ManualMode} />
        </Stack.Navigator>
      )}
    </NavigationContainer>
  );
}
