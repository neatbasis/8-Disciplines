import unittest

from acme_customer_feedback import compute_workflow_status, step_prereqs


class TestWorkflowGating(unittest.TestCase):
    def test_doing_is_first_available_missing_step_in_order(self):
        # Only issue is complete; everything else missing.
        report = {
            'issue': {
                'what_happened': 'x',
                'when_happened': 'now',
                'where_happened': 'here',
                'expecting_to_happen': 'should work',
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

        order = [
            'issue',
            'plan',
            'prerequisites',
            'team',
            'problem_description',
            'interim_containment_plan',
            'root_causes',
            'permanent_corrections',
            'corrective_actions',
            'preventive_measures',
        ]

        status = compute_workflow_status(report, order, step_prereqs())

        # plan is gated only on issue in our prereq map, so it should be first available.
        self.assertEqual(status['doing'], 'plan')
        self.assertIn('plan', status['available'])

    def test_blocked_steps_are_reported_when_prereqs_missing(self):
        # Issue incomplete -> almost everything should be blocked.
        report = {
            'issue': {
                'what_happened': 'x',
                'when_happened': None,
                'where_happened': 'here',
                'expecting_to_happen': 'should work',
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

        order = [
            'issue',
            'plan',
            'prerequisites',
            'team',
            'problem_description',
            'interim_containment_plan',
            'root_causes',
            'permanent_corrections',
            'corrective_actions',
            'preventive_measures',
        ]

        status = compute_workflow_status(report, order, step_prereqs())

        # With incomplete issue, nothing should be available (because issue isn't done).
        self.assertIsNone(status['doing'])
        self.assertEqual(status['available'], [])
        self.assertTrue(len(status['blocked']) > 0)


if __name__ == '__main__':
    unittest.main()
