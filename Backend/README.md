# Mental Wellness API - Groq-Powered Empathy Agent

## Overview

This FastAPI backend provides a mental wellness support system powered by Groq's high-performance LLM API. The system has been completely migrated from local MT5 model training to cloud-based Groq API with advanced prompt engineering for empathetic responses.

## Key Features

### 🤖 Groq-Powered Empathy Agent
- **Advanced Prompt Engineering**: Sophisticated empathy framework with cultural sensitivity
- **Bilingual Support**: Natural code-switching between English and Hindi
- **Context-Aware Responses**: Maintains conversation history for better continuity
- **Crisis Detection**: Automatic identification and escalation of crisis situations
- **Emotion Analysis**: Real-time emotional state detection and response adaptation

### 🔒 Security & Privacy
- **End-to-End Encryption**: All messages encrypted using Fernet encryption
- **JWT Authentication**: Secure user authentication with token-based access
- **Anonymous Support**: Users can interact without creating accounts
- **Data Protection**: Encrypted storage of sensitive conversation data

### 📊 Admin Dashboard
- **Real-time Analytics**: Emotional trends and user engagement metrics
- **Crisis Monitoring**: Automated flagging and review of concerning content
- **Conversation Analysis**: AI-powered insights into user conversation patterns
- **Wellness Reports**: Periodic analysis of emotional health trends

### 🌟 Enhanced Features
- **Personalized Wellness Plans**: AI-generated suggestions based on emotional state
- **Cultural Context**: Tailored for Indian youth with culturally appropriate responses
- **WebSocket Support**: Real-time chat capabilities
- **Scalable Architecture**: Docker-ready with Redis/Celery for background tasks

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI        │    │   Groq API      │
│   (React/Vue)   │◄──►│   Backend        │◄──►│   (LLM Engine)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   MongoDB        │
                       │   (Encrypted     │
                       │    Messages)     │
                       └──────────────────┘
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- MongoDB
- Redis (for background tasks)
- Groq API Key

### 1. Environment Setup

Create a `.env` file in the `Backend/app/` directory:

```env
# FastAPI Configuration
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Database
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=mental_wellness

# Redis/Celery
REDIS_URL=redis://localhost:6379/0

# Encryption
FERNET_KEY=your_32_byte_url_safe_base64_encoded_key

# Groq API (REQUIRED)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
```

### 2. Generate Encryption Key

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3. Install Dependencies

```bash
cd Backend
pip install -r requirements.txt
```

### 4. Start Services

```bash
# Start MongoDB
mongod

# Start Redis
redis-server

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Docker Setup (Recommended)

```bash
# From project root
docker-compose up --build
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user (anonymous or with credentials)
- `POST /api/auth/token` - Login and get JWT token

### Chat
- `POST /api/chat/message` - Send message and get empathetic response
- `GET /api/chat/history` - Retrieve conversation history
- `GET /api/chat/wellness-suggestions` - Get personalized wellness suggestions
- `GET /api/chat/emotion-analysis` - Analyze emotion of text
- `WebSocket /api/chat/ws` - Real-time chat interface

### Admin
- `GET /api/admin/dashboard` - Admin overview and metrics
- `GET /api/admin/messages` - List messages with filtering
- `GET /api/admin/flagged` - List crisis/flagged messages
- `POST /api/admin/flag/{message_id}` - Flag message for review
- `POST /api/admin/analyze-conversation/{user_id}` - Analyze user patterns
- `GET /api/admin/emotions-report` - Generate emotion trends report
- `POST /api/admin/wellness-insights` - Generate wellness recommendations

## Groq Integration

### Model Configuration

The system uses Groq's high-performance LLM API with optimized parameters:

- **Model**: `mixtral-8x7b-32768` (configurable)
- **Temperature**: 0.7 (balanced creativity)
- **Max Tokens**: 150-200 (concise responses)
- **Top-p**: 0.9 (diverse but relevant responses)

### Prompt Engineering

The empathy agent uses a sophisticated prompt framework:

1. **System Prompt**: Defines empathy principles and cultural context
2. **Context Integration**: Includes recent conversation history
3. **Cultural Sensitivity**: Supports English-Hindi code-switching
4. **Crisis Awareness**: Trained to recognize and handle crisis situations
5. **Response Validation**: Post-processing for safety and quality

### Example Empathy Framework

```python
empathy_framework = {
    "core_principles": [
        "Listen with genuine care and presence",
        "Validate emotions without judgment", 
        "Offer hope and practical support",
        "Respect cultural and linguistic diversity",
        "Encourage connection with support systems"
    ],
    "response_styles": {
        "validation": ["Tumhari feelings bilkul valid hain", "I hear you..."],
        "empathy": ["That sounds really challenging", "Main feel kar sakta hoon..."],
        "support": ["You don't have to go through this alone", "Tum akele nahi ho..."],
        "encouragement": ["You're stronger than you know", "Tumne ye share kiya..."]
    }
}
```

## Migration from MT5 Training

### What Changed

1. **Removed Local Training**: No more MT5 model training or fine-tuning
2. **Cloud-Based AI**: Leverages Groq's optimized inference infrastructure
3. **Enhanced Prompting**: Advanced prompt engineering replaces model training
4. **Faster Responses**: Groq's optimized hardware provides sub-second responses
5. **Better Multilingual**: Native support for English-Hindi code-switching
6. **Reduced Infrastructure**: No GPU requirements or model storage needed

### Benefits

- **Scalability**: Handle thousands of concurrent users
- **Cost Efficiency**: No GPU infrastructure costs
- **Maintenance**: No model retraining or version management
- **Performance**: Consistent, fast response times
- **Quality**: Access to state-of-the-art language models
- **Reliability**: Enterprise-grade API with high availability

## Development

### Project Structure

```
Backend/
├── app/
│   ├── api/           # API endpoints
│   │   ├── auth.py    # Authentication
│   │   ├── chat.py    # Chat functionality  
│   │   ├── admin.py   # Admin dashboard
│   │   └── deps.py    # Dependencies
│   ├── core/          # Core configuration
│   │   ├── config.py  # Settings
│   │   └── security.py # JWT handling
│   ├── db/            # Database models
│   │   ├── models.py  # Beanie models
│   │   └── base.py    # DB initialization
│   ├── services/      # Business logic
│   │   ├── ai_service.py        # Groq integration
│   │   ├── finetune_mt5.py      # Enhanced Groq service
│   │   └── escalation.py        # Crisis detection
│   ├── utils/         # Utilities
│   │   └── encryption.py # Message encryption
│   ├── tasks/         # Background tasks
│   │   └── workers.py # Celery workers
│   └── main.py        # FastAPI app
├── requirements.txt   # Python dependencies
├── Dockerfile        # Container setup
└── README.md         # This file
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Test specific endpoint
pytest tests/test_chat.py -v

# Test with coverage
pytest --cov=app tests/
```

### Monitoring

The system includes comprehensive logging and monitoring:

- **Request Logging**: All API calls logged with response times
- **Error Tracking**: Detailed error logs with stack traces
- **Emotion Analytics**: Real-time tracking of emotional trends
- **Crisis Alerts**: Immediate notifications for concerning content
- **Performance Metrics**: Response times and throughput monitoring

## Deployment

### Production Considerations

1. **Environment Variables**: Secure storage of API keys and secrets
2. **Database Scaling**: MongoDB replica sets or Atlas for production
3. **Redis Clustering**: For high-availability background tasks
4. **Load Balancing**: Multiple FastAPI instances behind load balancer
5. **SSL/TLS**: HTTPS termination for secure communications
6. **Rate Limiting**: Protect against API abuse
7. **Monitoring**: APM tools like New Relic or DataDog

### Docker Production

```yaml
# docker-compose.prod.yml
version: "3.9"
services:
  backend:
    build: ./backend
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - MONGODB_URL=${MONGODB_URL}
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
```

## Security

### Data Protection
- All messages encrypted at rest using Fernet encryption
- JWT tokens for secure authentication
- CORS protection for cross-origin requests
- Input validation and sanitization
- Rate limiting to prevent abuse

### Privacy Considerations
- Anonymous chat support
- No personal data collection required
- Conversation data encrypted and isolated by user
- Admin access controls and audit logging
- GDPR-compliant data handling practices

## Support

### Crisis Response
The system includes built-in crisis detection and response:

1. **Keyword Detection**: Identifies concerning language patterns
2. **Automatic Escalation**: Flags crisis messages for immediate review
3. **Resource Provision**: Provides crisis helpline numbers and resources
4. **Professional Referral**: Encourages professional mental health support

### Resources
- **iCall**: 9152987821 (India)
- **KIRAN**: 1800-599-0019 (India)
- **Emergency**: Local emergency services

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit pull request
5. Ensure all checks pass

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v2.0.0 - Groq Migration
- Migrated from local MT5 training to Groq API
- Enhanced prompt engineering framework
- Improved cultural sensitivity and bilingual support
- Added comprehensive admin dashboard
- Implemented real-time emotion analysis
- Enhanced crisis detection and response

### v1.0.0 - Initial Release
- Basic MT5 model training and inference
- Simple chat functionality
- MongoDB integration
- Basic authentication