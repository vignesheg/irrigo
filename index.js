// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.0/firebase-app.js";
import { getDatabase, ref, onValue, set } from "https://www.gstatic.com/firebasejs/10.13.0/firebase-database.js";

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDymuoSQrB855PmttCpUbiOlp6Ag4iraIA",
    authDomain: "irrigo-dfb76.firebaseapp.com",
    projectId: "irrigo-dfb76",
    storageBucket: "irrigo-dfb76.appspot.com",
    messagingSenderId: "962205265859",
    appId: "1:962205265859:web:4bd3bdc9336d24d9c19776",
    measurementId: "G-743R2SL793"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const statusRef = ref(db, 'mt-status');

// Function to update UI
function updateUI(status) {
    const statusCircle = $('#status-circle');
    const statusText = $('#status-text');
    const toggleButton = $('#toggle-button');

    if (status === 1) {
        statusCircle.removeClass('off').addClass('on');
        statusText.text('Status: On');
        toggleButton.text('Turn Off');
    } else {
        statusCircle.removeClass('on').addClass('off');
        statusText.text('Status: Off');
        toggleButton.text('Turn On');
    }
}

// Listen for changes to 'mt-status' in the database
onValue(statusRef, (snapshot) => {
    const status = snapshot.val();
    updateUI(status);
}, (error) => {
    console.error('Error fetching data:', error);
});

// Toggle button functionality
$('#toggle-button').click(function() {
    const currentStatus = $('#status-circle').hasClass('on') ? 1 : 0;
    set(statusRef, currentStatus === 1 ? 0 : 1);
});

// Sample function to update sidebar content (replace with real data if available)
function updateSidebar(weatherPressure, soilConditions) {
    $('#weather-pressure-link').text(`Weather Pressure: ${weatherPressure}`).attr('href', '#');
    $('#soil-conditions-link').text(`Soil Conditions: ${soilConditions}`).attr('href', '#');
}

// Example update (you can replace this with real-time updates)
updateSidebar('1013 hPa', 'Moist');

// Toggle sidebar visibility
$('#show-sidebar').click(function() {
    const sidebar = $('#sidebar');
    sidebar.toggleClass('sidebar-hidden sidebar-visible');
    $(this).text(sidebar.hasClass('sidebar-hidden') ? '☰' : '×');
});
