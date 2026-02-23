#!/usr/bin/env python3
import argparse
from dataclasses import asdict
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Optional

from reportgenerator import ReportGenerator, is_issue_complete
from survey_tools import CustomerFeedback, get_customer_contact, get_customer_feedback, get_issue


class EightDisciplines:
    def __init__(self, issue):
        self.EIGHT_DISCIPLINES = [
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
        self.issue = issue
        self.feedback = []
        self.team = None
        self.plan = None
        self.problem_description = None
        self.interim_containment_plan = None
        self.root_causes = None
        self.permanent_corrections = None
        self.corrective_actions = None
        self.preventive_measures = None
        self.congratulations = None

    def plan_solving_problem(self, plan, prerequisites):
        self.plan = (plan, prerequisites)

    def use_team(self, team):
        self.team = team

    def define_problem(self, problem_description):
        self.problem_description = problem_description

    def develop_interim_containment_plan(self, interim_containment_plan):
        self.interim_containment_plan = interim_containment_plan

    def determine_root_causes(self, root_causes):
        self.root_causes = root_causes

    def choose_permanent_corrections(self, permanent_corrections):
        self.permanent_corrections = permanent_corrections

    def implement_corrective_actions(self, corrective_actions):
        self.corrective_actions = corrective_actions

    def take_preventive_measures(self, preventive_measures):
        self.preventive_measures = preventive_measures

    def congratulate_team(self):
        report = self.generate_machine_readable_report()
        self.congratulations = ReportGenerator.congrats_template(report)
        return self.congratulations

    def inform_scrum(self):
        report = self.generate_machine_readable_report()
        generator = ReportGenerator(report)
        text = '----------- SCRUM REPORT -------------\n'
        text += f"{generator.scrum_report()}\n"
        text += '------- END OF SCRUM REPORT-----------\n'
        return text

    def generate_machine_readable_report(self) -> Dict[str, Optional[str]]:
        if self.plan is None:
            plan = None
            prerequisites = None
        else:
            plan = self.plan[0]
            prerequisites = self.plan[1]

        return {
            'issue': self.issue,
            'plan': plan,
            'prerequisites': prerequisites,
            'team': self.team,
            'problem_description': self.problem_description,
            'interim_containment_plan': self.interim_containment_plan,
            'root_causes': self.root_causes,
            'permanent_corrections': self.permanent_corrections,
            'corrective_actions': self.corrective_actions,
            'preventive_measures': self.preventive_measures,
        }


def parse_args():
    parser = argparse.ArgumentParser(description='8-Disciplines Problem Solving')
    parser.add_argument('--use-defaults', dest='use_defaults', action='store_true')
    parser.add_argument('--non-interactive', action='store_true', help='Skip prompts and run using stored defaults only.')
    parser.add_argument('--format', choices=['scrum', 'plain', 'json'], default=os.getenv('ACME_OUTPUT_FORMAT', 'scrum'))
    parser.add_argument('--defaults-file', default=os.getenv('ACME_DEFAULTS_FILE', 'customer_defaults.json'))
    return parser.parse_args()


def load_defaults(defaults_file):
    if os.path.exists(defaults_file):
        with open(defaults_file, 'r', encoding='utf-8') as file:
            defaults = json.load(file)
    else:
        defaults = {
            'name': None,
            'phone_number': None,
            'email': None,
            'feedback': None,
            'what_happened': None,
            'when_happened': None,
            'where_happened': None,
            'expecting_to_happen': None,
            'resolution_request': None,
        }
    return defaults


def save_defaults(defaults, defaults_file):
    with open(defaults_file, 'w', encoding='utf-8') as file:
        json.dump(defaults, file)


def _has_issue_details(issue: Dict[str, Optional[str]]) -> bool:
    # Strict: issue is "submitted" only if it satisfies required completeness.
    return is_issue_complete(issue)


def step_order(eight_d: EightDisciplines) -> list[str]:
    return ['issue'] + list(eight_d.EIGHT_DISCIPLINES)


def step_prereqs() -> Dict[str, list[str]]:
    # Minimal, sensible gating. Adjust as you evolve your definition-of-ready.
    return {
        'issue': ['issue'],
        'team': ['issue'],
        'problem_description': ['issue', 'team'],
        'interim_containment_plan': ['problem_description'],
        'root_causes': ['problem_description', 'interim_containment_plan'],
        'permanent_corrections': ['root_causes'],
        'corrective_actions': ['permanent_corrections'],
        'preventive_measures': ['corrective_actions'],
        'plan': ['issue'],
        'prerequisites': ['plan'],
    }


def ordered(steps: list[str], order: list[str]) -> list[str]:
    idx = {k: i for i, k in enumerate(order)}
    return sorted(steps, key=lambda s: idx.get(s, 10**9))


def compute_workflow_status(report: Dict[str, object], order: list[str], prereqs: Dict[str, list[str]]):
    missing = ReportGenerator.check_empty_values(report)
    done = ReportGenerator.check_nonempty_values(report)

    missing_ord = ordered(missing, order)
    done_ord = ordered(list(done), order)

    available = []
    blocked = []
    for step in missing_ord:
        reqs = prereqs.get(step, [])
        if all(r in done for r in reqs):
            available.append(step)
        else:
            blocked.append(step)

    doing = available[0] if available else None
    return {
        'done': done_ord,
        'missing': missing_ord,
        'available': available,
        'blocked': blocked,
        'doing': doing,
    }


def customer_service_chatbot(args):
    defaults = load_defaults(args.defaults_file)
    issue = get_issue(defaults)
    feedback_submitted = False

    env_non_interactive = os.getenv('NON_INTERACTIVE', '0') == '1'
    interactive_mode = not (args.non_interactive or env_non_interactive) and sys.stdin.isatty()

    if interactive_mode and not args.use_defaults:
        defaults = get_customer_contact(defaults)
        print('How can we help you today?')
        defaults, feedback_submitted, issue = get_customer_feedback(defaults)
    else:
        # Non-interactive OR explicitly using defaults: never prompt.
        # "feedback_submitted" is derived strictly from stored issue completeness.
        feedback_submitted = _has_issue_details(issue)

    if feedback_submitted:
        issue_blob = json.dumps(issue, sort_keys=True)
        log_feedback(CustomerFeedback(feedback=issue_blob, rating=None))

    save_defaults(defaults, args.defaults_file)

    eight_d = EightDisciplines(issue)
    report = eight_d.generate_machine_readable_report()

    order = step_order(eight_d)
    prereqs = step_prereqs()
    status = compute_workflow_status(report, order, prereqs)

    if args.format == 'json':
        print(json.dumps({
            'feedback_submitted': feedback_submitted,
            'report': report,
            'done_steps': status['done'],
            'missing_steps': status['missing'],
            'available_steps': status['available'],
            'blocked_steps': status['blocked'],
            'doing_step': status['doing'],
        }))
        return

    print('Thank you for choosing our services. We are committed to providing you with the best experience possible!')
    if not feedback_submitted:
        print('No complete issue submitted (requires what/when/where/expectation).')
        return

    print('Your feedback will be used to improve our services and ensure a better experience for all customers.')
    if args.format == 'scrum':
        print(eight_d.inform_scrum())
    else:
        print(ReportGenerator(report).scrum_report())

    if status['done']:
        print('Done:')
        for step in status['done']:
            print(f'- {step}')

    if status['missing']:
        if status['doing'] is not None:
            print(f"\nDoing: {status['doing']}")
        else:
            print('\nDoing: (none available — prerequisites missing)')

        print('\nTodo (available next):')
        for step in status['available']:
            print(f'- {step}')

        if status['blocked']:
            print('\nBlocked (missing prerequisites):')
            done_set = set(status['done'])
            for step in status['blocked']:
                reqs = prereqs.get(step, [])
                missing_reqs = [r for r in reqs if r not in done_set]
                print(f"- {step} (needs: {', '.join(missing_reqs)})")
    else:
        print(eight_d.congratulate_team())


def log_feedback(feedback: CustomerFeedback):
    log_path = os.getenv('ACME_FEEDBACK_LOG', 'feedback_events.jsonl')
    payload = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'event': 'customer_feedback_submitted',
        'feedback': asdict(feedback),
    }
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(json.dumps(payload, sort_keys=True) + '\n')


def main():
    args = parse_args()
    try:
        customer_service_chatbot(args)
    except KeyboardInterrupt:
        print('\nAborted by user.')
        raise SystemExit(130)


if __name__ == '__main__':
    main()
