import re
import unicodedata

DEVANAGARI_RANGES = (
    (0x0900, 0x097F),
    (0xA8E0, 0xA8FF),
)

LATIN_RANGES = (
    (0x0041, 0x007A),
    (0x00C0, 0x00FF),
    (0x0100, 0x017F),
    (0x0180, 0x024F),
    (0x1E00, 0x1EFF),
    (0x2C60, 0x2C7F),
    (0xA720, 0xA7FF),
    (0xAB30, 0xAB6F),
)

TOKEN_RE = re.compile(r"[A-Za-z]+|[\u0900-\u097F]+")

MIXED_SCRIPT_MIN_RATIO = 0.15
MIN_ALPHA_RATIO = 0.15

HINDI_ROMANIZED_WORDS = {
    "aaj",
    "aj",
    "kal",
    "parso",
    "abhi",
    "ab",
    "tab",
    "jab",
    "kab",
    "yaha",
    "yahan",
    "waha",
    "wahan",
    "mai",
    "mein",
    "mera",
    "meri",
    "mere",
    "mujhe",
    "mujh",
    "mujhse",
    "mujhko",
    "mereko",
    "hum",
    "ham",
    "hume",
    "humein",
    "tum",
    "tera",
    "teri",
    "tere",
    "aap",
    "aapka",
    "aapki",
    "aapke",
    "ap",
    "apka",
    "apki",
    "apke",
    "ye",
    "yeh",
    "yah",
    "wo",
    "woh",
    "vo",
    "kya",
    "kyu",
    "kyun",
    "kyon",
    "kaise",
    "kahan",
    "kaha",
    "ka",
    "ki",
    "ke",
    "hai",
    "hain",
    "tha",
    "thi",
    "the",
    "ho",
    "hun",
    "hoon",
    "hoga",
    "hogi",
    "honge",
    "raha",
    "rahe",
    "rahi",
    "rha",
    "rhe",
    "rhi",
    "nahi",
    "nahin",
    "nhi",
    "na",
    "haan",
    "han",
    "bahut",
    "bohot",
    "bhot",
    "thoda",
    "thodi",
    "thode",
    "dard",
    "bukhar",
    "bukhaar",
    "sardi",
    "khansi",
    "pet",
    "gala",
    "sar",
    "chakkar",
    "thakan",
    "thakaan",
    "kamjor",
    "kamzori",
    "bimar",
    "beemar",
    "tabiyat",
    "dawa",
    "dawai",
    "davai",
    "theek",
    "thik",
    "acha",
    "accha",
    "aur",
    "par",
    "lekin",
    "kyunki",
    "phir",
    "fir",
    "yaar",
    "bhai",
}

HINDI_ROMANIZED_SUFFIXES = ("wala", "wali", "wale")

ENGLISH_WORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "if",
    "then",
    "so",
    "because",
    "i",
    "you",
    "he",
    "she",
    "it",
    "we",
    "they",
    "me",
    "my",
    "your",
    "his",
    "her",
    "our",
    "their",
    "this",
    "that",
    "these",
    "those",
    "is",
    "am",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "do",
    "does",
    "did",
    "have",
    "has",
    "had",
    "not",
    "no",
    "yes",
    "ok",
    "okay",
    "please",
    "today",
    "yesterday",
    "tomorrow",
    "now",
    "later",
    "morning",
    "night",
    "day",
    "week",
    "feel",
    "feels",
    "feeling",
    "felt",
    "hurt",
    "pain",
    "ache",
    "headache",
    "fever",
    "cough",
    "cold",
    "flu",
    "sore",
    "throat",
    "stomach",
    "back",
    "body",
    "tired",
    "fatigue",
    "nausea",
    "vomit",
    "vomiting",
    "diarrhea",
    "diarrhoea",
    "dizzy",
    "dizziness",
    "weak",
    "weakness",
    "sleep",
    "sleepy",
    "insomnia",
    "stress",
    "anxiety",
    "mood",
    "sad",
    "happy",
    "angry",
    "off",
    "better",
    "worse",
    "medicine",
    "meds",
    "tablet",
    "pill",
    "doctor",
    "clinic",
    "hospital",
    "blood",
    "pressure",
    "sugar",
}


def is_devanagari_code(code):
    for start, end in DEVANAGARI_RANGES:
        if start <= code <= end:
            return True
    return False


def is_latin_code(code):
    for start, end in LATIN_RANGES:
        if start <= code <= end:
            return True
    return False


def count_scripts(text):
    latin = 0
    devanagari = 0
    other = 0
    non_space = 0
    for ch in text:
        if ch.isspace():
            continue
        non_space += 1
        if not ch.isalpha():
            continue
        code = ord(ch)
        if is_devanagari_code(code):
            devanagari += 1
        elif is_latin_code(code):
            latin += 1
        else:
            other += 1
    return latin, devanagari, other, non_space


def detect_script(latin, devanagari, other):
    total = latin + devanagari + other
    if total == 0:
        return "other"
    latin_ratio = latin / total
    devanagari_ratio = devanagari / total
    if (
        latin >= 2
        and devanagari >= 2
        and latin_ratio >= MIXED_SCRIPT_MIN_RATIO
        and devanagari_ratio >= MIXED_SCRIPT_MIN_RATIO
    ):
        return "mixed"
    if devanagari_ratio >= 0.6:
        return "devanagari"
    if latin_ratio >= 0.6:
        return "latin"
    if latin > 0 and devanagari > 0:
        return "mixed"
    if devanagari > 0:
        return "devanagari"
    if latin > 0:
        return "latin"
    return "other"


def is_meaningful_mix(hi_hits, en_hits):
    if hi_hits < 2 or en_hits < 2:
        return False
    ratio = min(hi_hits, en_hits) / max(hi_hits, en_hits)
    return ratio >= 0.6


def compute_confidence(language, metrics):
    token_count = metrics["token_count"]
    latin_ratio = metrics["latin_ratio"]
    devanagari_ratio = metrics["devanagari_ratio"]
    hi_word_hits = metrics["hi_word_hits"]
    hi_roman_hits = metrics["hi_roman_hits"]
    en_word_hits = metrics["en_word_hits"]
    script = metrics["script"]
    total_letters = metrics["total_letters"]

    if language == "unknown":
        conf = 0.2
        if total_letters == 0:
            conf = 0.1
        elif token_count >= 3:
            conf = 0.3
        return max(0.0, min(1.0, conf))

    if language == "hi":
        conf = 0.6 + 0.3 * devanagari_ratio
        if token_count < 3:
            conf -= 0.1
        return max(0.0, min(1.0, conf))

    if language == "en":
        word_ratio = en_word_hits / max(1, token_count)
        conf = 0.55 + 0.35 * min(1.0, word_ratio)
        if latin_ratio < 0.8:
            conf -= 0.1
        return max(0.0, min(1.0, conf))

    if language == "hinglish":
        word_ratio = hi_roman_hits / max(1, token_count)
        conf = 0.55 + 0.3 * min(1.0, word_ratio)
        if en_word_hits > 0:
            conf += 0.05
        return max(0.0, min(1.0, conf))

    if language == "mixed":
        mix_ratio = (hi_word_hits + en_word_hits) / max(1, token_count)
        conf = 0.5 + 0.3 * min(1.0, mix_ratio)
        if script == "mixed":
            conf += 0.1
        return max(0.0, min(1.0, conf))

    return 0.2


def analyze_text(text):
    normalized = unicodedata.normalize("NFKC", text or "")
    latin_count, devanagari_count, other_count, non_space_count = count_scripts(normalized)
    total_letters = latin_count + devanagari_count + other_count
    alpha_ratio = total_letters / max(1, non_space_count)

    hi_roman_hits = 0
    en_word_hits = 0
    devanagari_token_count = 0
    latin_token_count = 0
    token_count = 0
    first_token_len = 0
    hindi_words = HINDI_ROMANIZED_WORDS
    english_words = ENGLISH_WORDS
    hindi_suffixes = HINDI_ROMANIZED_SUFFIXES
    for match in TOKEN_RE.finditer(normalized):
        token = match.group(0)
        if not token:
            continue
        token_count += 1
        if token_count == 1:
            first_token_len = len(token)
        first_code = ord(token[0])
        if is_devanagari_code(first_code):
            devanagari_token_count += 1
            continue
        latin_token_count += 1
        token_lower = token.lower()
        if token_lower in hindi_words or token_lower.endswith(hindi_suffixes):
            hi_roman_hits += 1
        if token_lower in english_words:
            en_word_hits += 1

    hi_word_hits = hi_roman_hits + devanagari_token_count

    script = detect_script(latin_count, devanagari_count, other_count)
    latin_ratio = latin_count / total_letters if total_letters else 0.0
    devanagari_ratio = devanagari_count / total_letters if total_letters else 0.0

    short_token = token_count == 1 and first_token_len <= 2 if token_count else False

    if (
        total_letters == 0
        or token_count == 0
        or alpha_ratio < MIN_ALPHA_RATIO
        or (short_token and hi_roman_hits == 0 and en_word_hits == 0 and devanagari_token_count == 0)
    ):
        language = "unknown"
    elif script == "devanagari":
        language = "hi"
    elif script == "mixed" and (
        latin_ratio >= MIXED_SCRIPT_MIN_RATIO and devanagari_ratio >= MIXED_SCRIPT_MIN_RATIO
    ):
        language = "mixed"
    elif latin_ratio >= 0.6:
        if hi_roman_hits > 0:
            language = "mixed" if is_meaningful_mix(hi_roman_hits, en_word_hits) else "hinglish"
        elif en_word_hits > 0:
            language = "en"
        elif latin_token_count >= 3:
            language = "en"
        else:
            language = "unknown"
    elif devanagari_ratio >= 0.4:
        language = "hi"
    else:
        language = "unknown"

    metrics = {
        "latin_ratio": latin_ratio,
        "devanagari_ratio": devanagari_ratio,
        "hi_word_hits": hi_word_hits,
        "hi_roman_hits": hi_roman_hits,
        "en_word_hits": en_word_hits,
        "token_count": token_count,
        "script": script,
        "total_letters": total_letters,
    }

    confidence = compute_confidence(language, metrics)
    evidence = {
        "latin_ratio": round(latin_ratio, 2),
        "devanagari_ratio": round(devanagari_ratio, 2),
        "hi_word_hits": hi_word_hits,
        "en_word_hits": en_word_hits,
        "token_count": token_count,
    }

    return {
        "primary_language": language,
        "script": script,
        "confidence": round(confidence, 2),
        "evidence": evidence,
    }
