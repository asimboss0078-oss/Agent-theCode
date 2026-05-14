# Agent-theCode Advanced Chat Agent

## Features
- Chat UI with mini-browser
- Automatic web lookup (no commands needed)
- Multi-Supabase/multi-API backend
- Teach agent new knowledge via Training Page
- All config via `.env`, never committing secrets

## Usage

1. Set up `.env` based on `.env.sample`
2. Run Python backend: `python3 backend/app.py`
3. Open `web_ui/index.html` for chat, or deploy frontend with Vercel

### Train the agent
- Go to `/train.html`, upload text or file, assign a label (Supabase project), and teach.

### Web browsing
- Just ask about current events/websites; if needed, agent fetches and previews the web page.
- Mini-browser panel displays content seen by agent.

---

## Security
- API and Supabase credentials are read **only from your environment!**
- Never push real keys to this repo.

---
