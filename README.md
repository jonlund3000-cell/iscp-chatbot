# ISCP Virtual Assistant — Demo

A chatbot for www.iscp.ac.uk that answers common trainee and trainer queries,
and escalates difficult ones to the human helpdesk.

## Setup (one time)

### 1. Open Terminal and go to this folder
```
cd ~/Downloads/iscp-chatbot
```

### 2. Create a Python virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Add your Anthropic API key
Edit the `.env` file and replace the placeholder:
```
ANTHROPIC_API_KEY=sk-ant-your-real-key-here
```

## Run the demo

```
source venv/bin/activate   # if not already active
python app.py
```

Then open your browser at: **http://localhost:5050**

## How it works

- `app.py` — Flask server, receives chat messages, calls Claude API
- `knowledge_base.py` — System prompt with ISCP-specific knowledge
- `templates/index.html` — The chat widget UI (styled to feel like ISCP)

## Escalation logic

The bot automatically escalates to the helpdesk when it detects keywords like:
"complaint", "appeal", "urgent", "locked out", "safeguarding", "speak to a person", etc.

When escalated, it shows the helpdesk banner with phone and email.

## Helpdesk contact (built into the bot)
- Email: helpdesk@iscp.ac.uk
- Phone: 020 7869 6299
- Hours: Monday–Friday, 9am–5pm

## Patching into the real ISCP site (later)

The chat widget in `templates/index.html` can be extracted into a standalone
`<script>` tag or iframe and embedded into any page on iscp.ac.uk by the web team.
The Flask backend would need to be hosted (e.g. on Azure, AWS, or a JCST server).
