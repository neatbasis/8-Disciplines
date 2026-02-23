import unittest

from reportgenerator import ReportGenerator
from survey_tools import CustomerIssue


class TestMissingness(unittest.TestCase):
    def test_issue_defaults_to_none(self):
        issue = CustomerIssue().to_dict()
        self.assertTrue(all(value is None for value in issue.values()))

    def test_reportgenerator_uses_none_semantics(self):
        report = {
            "issue": {"what_happened": None},
            "plan": None,
            "prerequisites": None,
            "team": None,
            "problem_description": None,
            "interim_containment_plan": None,
            "root_causes": None,
            "permanent_corrections": None,
            "corrective_actions": None,
            "preventive_measures": None,
        }
        missing = ReportGenerator.check_empty_values(report)
        done = ReportGenerator.check_nonempty_values(report)

        self.assertIn("plan", missing)
        self.assertIn("issue", missing)
        self.assertNotIn("issue", done)


if __name__ == "__main__":
    unittest.main()
