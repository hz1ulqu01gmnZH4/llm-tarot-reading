# LLM Tarot Reading

Local-only tarot reading app powered by LLM with high-quality RNG shuffling and card animations.

## Features
- 🔮 AI-powered tarot interpretations via OpenAI/OpenRouter/Ollama
- 🎲 Cryptographically secure shuffling (`window.crypto.getRandomValues`)
- ✨ Smooth card flip animations
- 🎯 Smart spread selection based on your question
- 🔒 100% local - your API keys never leave your browser
- 🎨 Complete 78-card AI-generated tarot deck

## Quick Start
1. Open `index.html` in browser
2. Enter API key (OpenAI/OpenRouter) or connect to local Ollama
3. Type your question
4. Watch the mystical unfold

## Usage

```
┌─────────────────────────────────────────────┐
│           🔮 LLM Tarot Reader 🔮            │
├─────────────────────────────────────────────┤
│                                             │
│  [?] What does the future hold for me?     │
│                                             │
│              [ Ask the Cards ]              │
│                                             │
│     ┌───┐    ┌───┐    ┌───┐               │
│     │ ? │    │ ? │    │ ? │               │
│     │   │    │   │    │   │               │
│     └───┘    └───┘    └───┘               │
│      Past   Present   Future               │
│                                             │
│  ─────────────────────────────────          │
│  Hover over cards for individual readings  │
│                                             │
│  Summary: The cards suggest a period of    │
│  transformation ahead...                   │
│                                             │
└─────────────────────────────────────────────┘
```

## Configuration
- **OpenAI**: Enter API key when prompted
- **OpenRouter**: Use any supported model key
- **Ollama**: Ensure Ollama is running locally on default port

## Tech Stack
- Pure HTML/CSS/JS - no frameworks needed
- Tarot deck: AI-generated Rider-Waite style imagery (78 cards)
- RNG: Browser's crypto API for true randomness
- Animations: CSS transitions for smooth flips

## Project Structure
- `images/` - Complete 78-card tarot deck
- `scripts/image_edit/` - Image processing utilities
- `docs/` - Design documentation

## License
WTFPL - Do What The F*ck You Want To Public License

## Notes
- All processing happens in-browser
- API keys stored in localStorage (clear browser data to remove)
- Supports 3-card, Celtic Cross, and custom spreads based on query

---
*"The cards know what the cards know"*