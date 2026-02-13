# Moltbot - AI-Powered Personal Assistant Mobile App

A comprehensive mobile application built with React Native that replicates all Moltbot features, including AI chat, persistent memory, task management, skills system, and more.

## 🚀 Features

### ✅ Implemented Features

1. **AI Chat Assistant**
   - Real-time conversation with AI (using Emergent LLM key)
   - Streaming responses
   - Conversation history
   - Context-aware responses
   - Voice output (text-to-speech)

2. **Persistent Memory System**
   - Stores user preferences and context
   - Remembers past conversations
   - Learns from interactions
   - Auto-extracts insights from conversations
   - Long-term memory across sessions

3. **Task Management**
   - Create, update, and delete tasks
   - Task priorities (low, medium, high)
   - Task status tracking (pending, completed)
   - Filter tasks by status and priority
   - Due date support
   - Recurring tasks support

4. **Skills/Plugins System**
   - Extensible skills architecture
   - Enable/disable skills
   - Built-in skills:
     - Weather
     - Web Search
     - Calendar
     - Email
     - Notes
   - Categorized skills (Information, Productivity, Communication, etc.)

5. **User Profile & Settings**
   - User registration and authentication
   - Profile management
   - Settings configuration
   - Logout functionality

6. **Proactive Notifications**
   - Daily briefings
   - Task reminders
   - System notifications
   - Unread notification tracking

7. **Cross-Platform Mobile App**
   - React Native + Expo
   - Works on iOS, Android, and Web
   - Beautiful, modern UI
   - Smooth animations and interactions

## 🛠️ Tech Stack

### Frontend
- **Framework**: React Native + Expo
- **Navigation**: React Navigation (Stack + Bottom Tabs)
- **UI Library**: React Native Paper
- **State Management**: React Hooks + Context API
- **HTTP Client**: Axios
- **Storage**: AsyncStorage
- **Voice**: Expo Speech (TTS)

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **AI**: OpenAI (via Emergent LLM key)
- **Background Tasks**: APScheduler

## 📁 Project Structure

```
/app
├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── routes/
│   │   ├── chat.py            # Chat endpoints
│   │   ├── tasks.py           # Task management
│   │   ├── skills.py          # Skills management
│   │   ├── users.py           # User management
│   │   ├── memory.py          # Memory system
│   │   └── notifications.py   # Notifications
│   ├── services/
│   │   ├── ai_service.py      # AI integration
│   │   ├── memory_service.py  # Memory management
│   │   ├── task_service.py    # Task operations
│   │   ├── skill_service.py   # Skills management
│   │   └── notification_service.py
│   ├── skills/                # Pluggable skills modules
│   └── requirements.txt       # Python dependencies
│
└── frontend/
    ├── App.js                 # Main app entry
    ├── src/
    │   ├── screens/
    │   │   ├── WelcomeScreen.js
    │   │   ├── ChatScreen.js
    │   │   ├── TasksScreen.js
    │   │   ├── SkillsScreen.js
    │   │   └── SettingsScreen.js
    │   ├── navigation/
    │   │   └── MainNavigator.js
    │   ├── services/
    │   │   └── api.js         # API client
    │   └── utils/
    │       ├── constants.js
    │       └── storage.js
    └── package.json
```

## 🔑 API Endpoints

### Chat
- `POST /api/chat/message` - Send message and get AI response
- `GET /api/chat/conversations/{user_id}` - Get user's conversations
- `GET /api/chat/messages/{conversation_id}` - Get conversation messages
- `DELETE /api/chat/conversation/{conversation_id}` - Delete conversation

### Tasks
- `POST /api/tasks/create` - Create new task
- `GET /api/tasks/list/{user_id}` - Get user's tasks
- `GET /api/tasks/upcoming/{user_id}` - Get upcoming tasks
- `PUT /api/tasks/complete/{task_id}` - Mark task as completed
- `PUT /api/tasks/update/{task_id}` - Update task
- `DELETE /api/tasks/delete/{task_id}` - Delete task

### Skills
- `GET /api/skills/list` - Get all skills
- `GET /api/skills/enabled` - Get enabled skills
- `PUT /api/skills/enable/{skill_id}` - Enable skill
- `PUT /api/skills/disable/{skill_id}` - Disable skill
- `POST /api/skills/install-defaults` - Install default skills

### Users
- `POST /api/users/create` - Create user
- `GET /api/users/get/{user_id}` - Get user
- `PUT /api/users/update/{user_id}` - Update user
- `GET /api/users/list` - List all users

### Memory
- `POST /api/memory/store` - Store memory
- `GET /api/memory/get/{user_id}` - Get memories
- `GET /api/memory/context/{user_id}` - Get user context

### Notifications
- `GET /api/notifications/list/{user_id}` - Get notifications
- `PUT /api/notifications/read/{notification_id}` - Mark as read

## 🚀 Running the Application

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB
- Expo CLI (for mobile development)

### Backend Setup
```bash
cd /app/backend
pip install -r requirements.txt
python server.py
```

Backend runs on: `http://localhost:8001`

### Frontend Setup
```bash
cd /app/frontend
npm install
npm run web     # For web
npm run android # For Android (requires Android Studio)
npm run ios     # For iOS (requires Xcode on macOS)
```

Frontend runs on: `http://localhost:3000`

### Using Supervisor (Production)
```bash
sudo supervisorctl restart backend frontend
sudo supervisorctl status
```

## 🧪 Testing the Application

### Test Backend Health
```bash
curl http://localhost:8001/api/health
```

### Test Chat API
```bash
curl -X POST http://localhost:8001/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "message": "Hello, Moltbot!",
    "conversation_id": null
  }'
```

### Test Task Creation
```bash
curl -X POST http://localhost:8001/api/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "title": "Buy groceries",
    "priority": "high"
  }'
```

## 🎨 App Screens

1. **Welcome Screen**: User registration and onboarding
2. **Chat Screen**: AI conversation interface with voice output
3. **Tasks Screen**: Task management with filters and priorities
4. **Skills Screen**: Browse and toggle skills by category
5. **Settings Screen**: User profile and app settings

## 🔐 Environment Variables

### Backend (`.env`)
```
MONGO_URL=mongodb://localhost:27017/moltbot
EMERGENT_LLM_KEY=sk-emergent-xxxx
JWT_SECRET=your-secret-key
PORT=8001
```

### Frontend (`.env`)
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 📱 Mobile Testing

### Web (Easiest)
```bash
cd /app/frontend
npm run web
```
Open `http://localhost:3000` in your browser

### Physical Device (Best Experience)
1. Install Expo Go app on your phone
2. Run `npm start` in frontend directory
3. Scan QR code with Expo Go

### Emulator/Simulator
- **Android**: Requires Android Studio + AVD
- **iOS**: Requires macOS + Xcode

## 🌟 Future Enhancements

The following features are architected but can be expanded:

1. **Messaging Integrations**
   - Telegram Bot integration
   - Discord Bot integration
   - WhatsApp integration
   - Slack integration

2. **Advanced Voice Features**
   - Voice input (speech-to-text)
   - Wake word detection
   - Multiple voice personalities

3. **Browser Control & Web Automation**
   - Web scraping
   - Form filling
   - Automated browsing

4. **Calendar Integration**
   - Google Calendar sync
   - Event creation and management
   - Meeting reminders

5. **Email Integration**
   - Gmail API integration
   - Email reading and sending
   - Inbox management

6. **Enhanced Skills**
   - Weather forecasting
   - News aggregation
   - Music control
   - Smart home integration

7. **File Management**
   - Local file access
   - Cloud storage integration
   - Document processing

## 🐛 Troubleshooting

### Backend Issues
```bash
# Check logs
tail -f /var/log/supervisor/backend.err.log

# Restart backend
sudo supervisorctl restart backend

# Test MongoDB connection
mongosh mongodb://localhost:27017/moltbot
```

### Frontend Issues
```bash
# Check logs
tail -f /var/log/supervisor/frontend.err.log

# Clear cache
cd /app/frontend
rm -rf node_modules/.cache

# Restart frontend
sudo supervisorctl restart frontend
```

### Database Issues
```bash
# Check MongoDB status
ps aux | grep mongod

# Restart MongoDB
sudo supervisorctl restart mongodb
```

## 📄 License

This project is for demonstration purposes.

## 🤝 Contributing

This is a complete implementation of Moltbot features. To extend:

1. Add new skills in `/app/backend/skills/`
2. Create new screens in `/app/frontend/src/screens/`
3. Add API endpoints in `/app/backend/routes/`
4. Update services in `/app/backend/services/`

## 📞 Support

For issues or questions about this implementation, check:
- Backend logs: `/var/log/supervisor/backend.err.log`
- Frontend logs: `/var/log/supervisor/frontend.out.log`
- MongoDB logs: `/var/log/mongodb.log`

---

**Built with ❤️ using React Native, FastAPI, and MongoDB**
