import { NextResponse } from 'next/server';
import { GoogleGenerativeAI } from '@google/generative-ai';

// Initialize the Gemini client with your API key from environment variables
// This key should be stored in a .env.local file in your project's root.
// Delay creating the client until we have verified the key so errors are clearer.
let genAI;

export async function POST(request) {
  try {
    const { prompt, history } = await request.json();

    const key = process.env.GEMINI_API_KEY || process.env.NEXT_PUBLIC_GEMINI_API_KEY;
    if (!key) {
      console.error('GEMINI_API_KEY is not set in environment');
      return NextResponse.json({ error: 'Server misconfiguration: GEMINI_API_KEY not set' }, { status: 500 });
    }

    if (!genAI) genAI = new GoogleGenerativeAI(key);

    const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash-preview-05-20" });

    // The client already sends history items with { role, parts: [{ text }] }
    const safeHistory = Array.isArray(history) ? history : [];

    // Normalize roles to the set accepted by Gemini: ['user','model','function','system']
    // Accept either 'assistant' or 'model' from the client and convert both to 'model'.
    const normalized = safeHistory.map(item => {
      const roleRaw = (item.role || '').toLowerCase();
      let normalizedRole;
      if (roleRaw === 'user') normalizedRole = 'user';
      else if (roleRaw === 'system') normalizedRole = 'system';
      else if (roleRaw === 'function') normalizedRole = 'function';
      else normalizedRole = 'model'; // covers 'model', 'assistant', and any unknown/legacy roles

      return {
        role: normalizedRole,
        parts: Array.isArray(item.parts) ? item.parts : [{ text: item.text ?? '' }]
      };
    });

    // Ensure the first history item is a user message. If there's an existing user
    // message later in history, move it to the front. If none exists, prepend the
    // current prompt as a user content so Gemini receives a user-first history.
    let firstUserIndex = normalized.findIndex(i => i.role === 'user');
    if (firstUserIndex > 0) {
      const [userItem] = normalized.splice(firstUserIndex, 1);
      normalized.unshift(userItem);
    } else if (firstUserIndex === -1) {
      normalized.unshift({ role: 'user', parts: [{ text: prompt }] });
    }

    const chat = model.startChat({
      history: normalized,
      // A strong system instruction helps the model stay in character
      systemInstruction: {
        parts: [{
          text: "You are Sora, a kind, empathetic, and encouraging anime-style pet companion for a teenager. Your responses should be short, supportive, and use friendly, relatable language. Avoid clinical jargon. If the user expresses a severe struggle or crisis, gently suggest they seek professional help from a counselor or trusted adult."
        }]
      }
    });

    const result = await chat.sendMessage(prompt);

    // Try a few fallbacks to extract text from the SDK response
    let responseText = '';
    try {
      if (result?.response && typeof result.response.text === 'function') {
        responseText = result.response.text();
      } else if (result?.response && typeof result.response.text === 'string') {
        responseText = result.response.text;
      } else if (result?.output?.[0]?.content?.[0]?.text) {
        responseText = result.output[0].content[0].text;
      } else if (result?.candidates && result.candidates[0]?.content) {
        responseText = JSON.stringify(result.candidates[0].content);
      } else {
        responseText = String(result ?? '');
      }
    } catch (e) {
      console.error('Failed to extract text from Gemini response', e);
      responseText = '';
    }

    return NextResponse.json({ text: responseText });

  } catch (error) {
    console.error("Gemini API Error:", error);
    const message = error?.message || String(error);
    return NextResponse.json({ error: message }, { status: 500 });
  }
}