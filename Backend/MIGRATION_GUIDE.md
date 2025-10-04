# Migration Guide: From MT5 Training to Groq API

## Overview

This guide explains the migration from local MT5 model training to Groq API integration for the Mental Wellness empathy agent.

## What Changed

### ❌ Removed (Old MT5 Approach)
- Local model training with `train_mt5_empathy.py`
- HuggingFace Transformers dependencies
- GPU/CPU intensive inference
- Model storage and versioning
- Dataset preprocessing for training
- Fine-tuning infrastructure

### ✅ Added (New Groq Approach)
- Groq API integration with `groq` Python client
- Advanced prompt engineering framework
- Cloud-based inference (sub-second responses)
- Enhanced conversation context management
- Real-time emotion analysis
- Personalized wellness suggestions
- Crisis detection with escalation

## Key Benefits

| Aspect | MT5 Training | Groq API |
|--------|-------------|-----------|
| **Setup Time** | Hours (training) | Minutes (API key) |
| **Response Time** | 2-5 seconds | <1 second |
| **Hardware Needs** | GPU recommended | None |
| **Scalability** | Limited by hardware | Enterprise-scale |
| **Model Updates** | Manual retraining | Automatic improvements |
| **Multilingual** | Limited training data | Native support |
| **Maintenance** | High (model management) | Low (API calls) |

## Migration Steps

### 1. Environment Setup

Replace training dependencies with Groq:

```bash
# Old requirements (removed)
transformers==4.56.2
datasets
evaluate
accelerate
torch
sentencepiece

# New requirements (added)
groq
```

### 2. Configuration Changes

Update your `.env` file:

```env
# Add Groq configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
```

### 3. Service Architecture Changes

#### Old MT5 Service (`ai_service.py`)
```python
# Old approach - local model loading
self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
self.generator = pipeline("text2text-generation", ...)

# Simple generation
outputs = self.generator(text, max_new_tokens=80)
```

#### New Groq Service (`ai_service.py`)
```python
# New approach - cloud API
self.client = Groq(api_key=settings.groq_api_key)

# Advanced prompt engineering
response = self.client.chat.completions.create(
    model=self.model,
    messages=[
        {"role": "system", "content": self.system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    max_tokens=150,
    temperature=0.7
)
```

### 4. Data Migration

No data migration needed! Your existing conversation data remains unchanged:
- MongoDB schema stays the same
- Encryption continues to work
- User authentication unchanged
- Message history preserved

### 5. API Compatibility

All existing API endpoints remain functional:
- `POST /api/chat/message` - Enhanced with better responses
- `GET /api/chat/history` - Same functionality
- WebSocket `/api/chat/ws` - Improved real-time responses

### 6. Enhanced Features

New capabilities available immediately:

#### Advanced Emotion Analysis
```python
# Before: Basic emotion detection
emotion = ai_service.analyze_emotion(text)

# After: Detailed emotional insights
analysis = ai_service.analyze_emotion(text)
# Returns: label, score, intensity, cultural_context
```

#### Conversation Context
```python
# Before: Stateless responses
reply = await ai_service.generate_empathic_reply(text)

# After: Context-aware responses
reply = await ai_service.generate_empathic_reply(text, user_id=user_id)
# Considers conversation history for better continuity
```

#### Wellness Suggestions
```python
# New feature: Personalized recommendations
suggestions = await ai_service.get_wellness_suggestions(emotion, user_id)
# Returns culturally appropriate, actionable suggestions
```

## Testing the Migration

### 1. Quick Validation
```bash
# Test Groq connection
python setup.py

# Test full integration
python test_groq_integration.py
```

### 2. Compare Responses

Test the same input with both systems to see quality improvements:

**Input**: "Mujhe bahut tension hai exams ke baare mein"

**Old MT5 Output**: 
> "Main samajh raha hoon tum kya feel kar rahe ho."

**New Groq Output**:
> "Exam tension bilkul normal hai, main samajh sakta hoon ye kitna overwhelming feel hota hai. Kya tumne koi specific subject ke baare mein baat karni hai? Thoda step-by-step approach try kar sakte hain."

### 3. Performance Testing

Monitor response times:

```python
import time

start = time.time()
response = await ai_service.generate_empathic_reply("I feel anxious")
end = time.time()

print(f"Response time: {end - start:.2f} seconds")
# Expected: <1 second with Groq vs 2-5 seconds with MT5
```

## Troubleshooting

### Common Issues

#### 1. Groq API Key Issues
```bash
# Verify API key
export GROQ_API_KEY="your_key_here"
python -c "from groq import Groq; print(Groq(api_key='$GROQ_API_KEY').models.list())"
```

#### 2. Import Errors
```bash
# Ensure groq is installed
pip install groq

# Check version
python -c "import groq; print(groq.__version__)"
```

#### 3. Model Selection
Available Groq models:
- `mixtral-8x7b-32768` (recommended for empathy)
- `llama2-70b-4096` (alternative)
- `gemma-7b-it` (lightweight option)

### 4. Rate Limiting
Handle API rate limits gracefully:

```python
try:
    response = self.client.chat.completions.create(...)
except groq.RateLimitError:
    # Fall back to cached responses or retry with backoff
    return self._get_fallback_response(text)
```

## Rollback Plan

If you need to rollback to MT5:

1. **Keep old code**: The old MT5 service is preserved in git history
2. **Restore dependencies**: Reinstall transformers and related packages
3. **Model files**: Restore from backup or retrain if needed
4. **Configuration**: Remove Groq settings from `.env`

```bash
# Rollback steps
git checkout previous_commit  # Before Groq migration
pip install transformers datasets torch
# Update .env to remove GROQ_* settings
```

## Performance Optimization

### Groq API Best Practices

1. **Caching**: Cache frequent responses
2. **Batching**: Group requests when possible
3. **Error Handling**: Implement retry logic
4. **Monitoring**: Track response times and errors

### Example Implementation
```python
from functools import lru_cache
import asyncio

class GroqService:
    @lru_cache(maxsize=100)
    def _cached_emotion_analysis(self, text_hash):
        # Cache emotion analysis for similar texts
        pass
    
    async def generate_with_retry(self, text, max_retries=3):
        for attempt in range(max_retries):
            try:
                return await self.generate_empathic_reply(text)
            except Exception as e:
                if attempt == max_retries - 1:
                    return self._get_fallback_response(text)
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Monitoring & Analytics

### New Metrics to Track

1. **Response Quality**: Empathy score, cultural sensitivity
2. **API Performance**: Latency, error rates, rate limits
3. **User Engagement**: Conversation length, emotional trends
4. **Cost Management**: API usage, token consumption

### Dashboard Enhancements

The new admin dashboard provides:
- Real-time emotion analysis trends
- Conversation quality metrics
- Crisis detection alerts
- Wellness suggestion effectiveness

## Cost Considerations

### Groq API Pricing
- Significantly lower than GPU infrastructure costs
- Pay-per-use model scales with actual usage
- No upfront hardware investment
- Reduced operational overhead

### Cost Optimization Tips
1. **Prompt Engineering**: Optimize for shorter, effective prompts
2. **Response Caching**: Cache common response patterns
3. **Smart Routing**: Use different models based on complexity
4. **Usage Monitoring**: Track and optimize API calls

## Conclusion

The migration from MT5 training to Groq API represents a significant upgrade in:

- **Performance**: Faster, more reliable responses
- **Quality**: Better empathy and cultural sensitivity
- **Scalability**: Handle enterprise-level traffic
- **Maintenance**: Reduced operational complexity
- **Features**: Enhanced emotion analysis and wellness suggestions

The new system is ready for production deployment with minimal infrastructure requirements and maximum user experience quality.

For questions or issues, refer to:
- [Groq API Documentation](https://console.groq.com/docs)
- [Project GitHub Issues](your_repo_issues_url)
- [Mental Wellness API Docs](http://localhost:8000/docs)