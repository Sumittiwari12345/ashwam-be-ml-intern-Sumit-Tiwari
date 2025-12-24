# Language Detection Logic

Deterministic, rule-based language and script detection for short, noisy health journal text.

## Approach
- Normalize text with NFKC.
- Count letter scripts using Unicode ranges to compute Latin vs Devanagari ratios.
- Tokenize into Latin and Devanagari word sequences.
- Count English word hits (small curated list) and Hindi romanized hits (curated list plus a suffix pattern).
- Apply fixed rules to decide `primary_language` and `script`.
- Use `unknown` for very short, numeric-only, emoji-only, or noisy inputs.

## Hinglish vs English
- If the text is Latin script and contains Hindi romanized words, it is labeled `hinglish` by default.
- If Hindi and English word hits are both present and relatively balanced (at least 2 each, within a 40% margin), the label becomes `mixed`.
- If only English word hits appear, the label is `en`.

## Confidence
Confidence is a 0-1 score derived from:
- script dominance (Latin/Devanagari ratios),
- coverage of word hits relative to token count,
- penalties for short or noisy inputs.

## CLI
```bash
lang_detect --in texts.jsonl --out lang.jsonl
```

On Windows (or if the script is not executable):
```bash
python lang_detect.py --in texts.jsonl --out lang.jsonl
```

## Flask server
Install dependencies:
```bash
pip install -r requirements.txt
```

Run the server:
```bash
python app.py --host 127.0.0.1 --port 5000
```

Example request:
```bash
curl -X POST http://127.0.0.1:5000/detect -H "Content-Type: application/json" -d "{\"id\":\"t_001\",\"text\":\"Aaj headache hai\"}"
```

Batch request:
```bash
curl -X POST http://127.0.0.1:5000/detect_batch -H "Content-Type: application/json" -d "{\"items\":[{\"id\":\"t_001\",\"text\":\"Aaj headache hai\"},{\"id\":\"t_002\",\"text\":\"I feel better\"}]}"
```

## Production WSGI server
```bash
pip install -r requirements.txt
python -m waitress --listen=127.0.0.1:5000 wsgi:app
```

## Tests
```bash
python -m unittest discover -s tests
```

## Known limitations
- Word lists are intentionally small and may miss rare romanizations or slang.
- Mixed language in Latin script is only labeled `mixed` when Hindi/English hits are balanced; English-heavy code-switching may remain `hinglish`.
- Other scripts are labeled as `other` with `unknown` language.

## Intentional tradeoff
I prioritize labeling `hinglish` when any Hindi romanized tokens appear to avoid classifying code-switched Hindi as plain English. This can over-label hinglish in English-heavy sentences.
"# Backend--Ashwam" 
