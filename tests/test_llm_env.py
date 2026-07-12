import os
import sys
import unittest
from unittest.mock import patch


class TestLlmEnv(unittest.TestCase):
    def test_uses_environment_api_key(self):
        os.environ["GROQ_API_KEY"] = "env-key"
        sys.modules.pop("backend.llm", None)

        with patch("groq.Groq") as mock_groq:
            import backend.llm as llm

        self.assertEqual(mock_groq.call_args.kwargs["api_key"], "env-key")
        self.assertIsNotNone(llm.client)


if __name__ == "__main__":
    unittest.main()
