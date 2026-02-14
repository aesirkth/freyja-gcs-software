#!/bin/bash
# Wait for the backend to be fully up (adjust time if needed)
sleep 10

# Hide the mouse cursor after 5 seconds of inactivity
unclutter -idle 5 &

# Launch Chromium in Kiosk mode
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ~/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' ~/.config/chromium/Default/Preferences

chromium --kiosk --noerrdialogs --disable-infobars http://localhost:5000
