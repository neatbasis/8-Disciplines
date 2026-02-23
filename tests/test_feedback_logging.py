import io
import json
import os
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout

from acme_customer_feedback import customer_service_chatbot, log_feedback
from survey_tools import CustomerFeedback


class TestFeedbackLogging(unittest.TestCase):
    def test_log_feedback_writes_jsonl_record(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, 'feedback.jsonl')
            os.environ['ACME_FEEDBACK_LOG'] = log_file

            log_feedback(CustomerFeedback(feedback='Service was delayed.', rating=8))

            with open(log_file, 'r', encoding='utf-8') as fh:
                lines = fh.readlines()

            self.assertEqual(len(lines), 1)
            record = json.loads(lines[0])
            self.assertEqual(record['event'], 'customer_feedback_submitted')
            self.assertEqual(record['feedback'], {'feedback': 'Service was delayed.', 'rating': 8})
            self.assertIn('timestamp', record)

    def test_chatbot_feedback_submission_triggers_logging(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            defaults_file = os.path.join(tmpdir, 'defaults.json')
            log_file = os.path.join(tmpdir, 'feedback.jsonl')
            defaults = {
                'name': 'Sam',
                'phone_number': '555-5555',
                'email': 'sam@example.com',
                'feedback': None,
                'what_happened': 'Package arrived damaged',
                'when_happened': '2025-01-10',
                'where_happened': 'Front porch',
                'expecting_to_happen': 'Package should be intact',
                'resolution_request': 'Replacement item',
            }
            with open(defaults_file, 'w', encoding='utf-8') as fh:
                json.dump(defaults, fh)

            os.environ['ACME_FEEDBACK_LOG'] = log_file
            args = Namespace(
                use_defaults=False,
                non_interactive=True,
                format='json',
                defaults_file=defaults_file,
            )

            with redirect_stdout(io.StringIO()):
                customer_service_chatbot(args)

            with open(log_file, 'r', encoding='utf-8') as fh:
                lines = fh.readlines()

            self.assertEqual(len(lines), 1)
            record = json.loads(lines[0])
            self.assertEqual(record['event'], 'customer_feedback_submitted')
            feedback_payload = json.loads(record['feedback']['feedback'])
            self.assertEqual(feedback_payload['what_happened'], defaults['what_happened'])
            self.assertEqual(feedback_payload['expecting_to_happen'], defaults['expecting_to_happen'])
            self.assertIsNone(record['feedback']['rating'])


if __name__ == '__main__':
    unittest.main()
