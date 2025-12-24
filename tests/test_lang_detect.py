import unittest

from lang_detect import analyze_text


class TestLangDetect(unittest.TestCase):
    def test_hindi_devanagari(self):
        text = "\u092e\u0941\u091d\u0947 \u0938\u0930 \u0926\u0930\u094d\u0926 \u0939\u0948"
        result = analyze_text(text)
        self.assertEqual(result["script"], "devanagari")
        self.assertEqual(result["primary_language"], "hi")

    def test_english(self):
        result = analyze_text("I have a headache today.")
        self.assertEqual(result["script"], "latin")
        self.assertEqual(result["primary_language"], "en")

    def test_hinglish(self):
        result = analyze_text("Aaj headache hai yaar.")
        self.assertEqual(result["script"], "latin")
        self.assertEqual(result["primary_language"], "hinglish")

    def test_mixed_scripts(self):
        text = "\u092e\u0941\u091d\u0947 \u092c\u0941\u0916\u093e\u0930 hai"
        result = analyze_text(text)
        self.assertEqual(result["script"], "mixed")
        self.assertEqual(result["primary_language"], "mixed")

    def test_unknown(self):
        text = "12345 !!! \U0001F637"
        result = analyze_text(text)
        self.assertEqual(result["primary_language"], "unknown")
        self.assertEqual(result["script"], "other")

    def test_confidence_range(self):
        result = analyze_text("I am ok.")
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)


if __name__ == "__main__":
    unittest.main()
