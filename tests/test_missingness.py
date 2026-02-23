import unittest

from reportgenerator import ReportGenerator, is_issue_complete
from survey_tools import CustomerIssue


class TestMissingness(unittest.TestCase):
    def test_issue_defaults_to_none(self):
        issue = CustomerIssue().to_dict()
        self.assertTrue(all(value is None for value in issue.values()))

    def test_issue_complete_requires_what_when_where_expectation(self):
        issue = {
            'what_happened': 'x',
            'when_happened': None,
            'where_happened': 'y',
            'expecting_to_happen': 'z',
            'resolution_request': None,
        }
        self.assertFalse(is_issue_complete(issue))

        issue['when_happened'] = 'now'
        self.assertTrue(is_issue_complete(issue))

    def test_reportgenerator_issue_step_uses_issue_completeness(self):
        report_incomplete = {
            'issue': {
                'what_happened': 'x',
                'when_happened': None,
                'where_happened': 'y',
                'expecting_to_happen': 'z',
                'resolution_request': None,
            },
            'plan': None,
            'prerequisites': None,
            'team': None,
            'problem_description': None,
            'interim_containment_plan': None,
            'root_causes': None,
            'permanent_corrections': None,
            'corrective_actions': None,
            'preventive_measures': None,
        }
        missing = ReportGenerator.check_empty_values(report_incomplete)
        done = ReportGenerator.check_nonempty_values(report_incomplete)
        self.assertIn('issue', missing)
        self.assertNotIn('issue', done)

        report_complete = dict(report_incomplete)
        report_complete['issue'] = {
            'what_happened': 'x',
            'when_happened': 'now',
            'where_happened': 'y',
            'expecting_to_happen': 'z',
            'resolution_request': None,
        }
        missing2 = ReportGenerator.check_empty_values(report_complete)
        done2 = ReportGenerator.check_nonempty_values(report_complete)
        self.assertNotIn('issue', missing2)
        self.assertIn('issue', done2)

    def test_scrum_report_empty_progress_replaces_placeholder_with_guidance(self):
        report = {
            'issue': CustomerIssue().to_dict(),
            'plan': None,
            'prerequisites': None,
            'team': None,
            'problem_description': None,
            'interim_containment_plan': None,
            'root_causes': None,
            'permanent_corrections': None,
            'corrective_actions': None,
            'preventive_measures': None,
        }

        scrum_report = ReportGenerator(report).scrum_report()

        self.assertIn("We haven't completed any steps yet. Let's get started with these first steps:", scrum_report)
        self.assertNotIn("[insert instructions here]", scrum_report)
        self.assertIn(
            "We need to address the issue gifted to us by our dear customer.",
            scrum_report,
        )
        self.assertIn(
            "Definition of complete: The issue has been acknowledged",
            scrum_report,
        )


if __name__ == '__main__':
    unittest.main()
