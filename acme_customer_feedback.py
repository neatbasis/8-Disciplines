#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Dict, Optional

from reportgenerator import ReportGenerator
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


def _has_issue_details(issue):
    return any(value is not None for value in issue.values())


def customer_service_chatbot(args):
    defaults = load_defaults(args.defaults_file)
    issue = get_issue(defaults)
    feedback_submitted = False

    env_non_interactive = os.getenv('NON_INTERACTIVE', '0') == '1'
    interactive_mode = not (args.non_interactive or env_non_interactive) and sys.stdin.isatty()

    if args.use_defaults:
        feedback_submitted = _has_issue_details(issue)
    elif interactive_mode:
        defaults = get_customer_contact(defaults)
        print('How can we help you today?')
        defaults, feedback_submitted, issue = get_customer_feedback(defaults)
    else:
        print('Running in non-interactive mode without --use-defaults; no new feedback was collected.')

    save_defaults(defaults, args.defaults_file)

    eight_d = EightDisciplines(issue)
    report = eight_d.generate_machine_readable_report()
    missing = ReportGenerator.check_empty_values(report)
    done = ReportGenerator.check_nonempty_values(report)

    if args.format == 'json':
        print(json.dumps({
            'feedback_submitted': feedback_submitted,
            'report': report,
            'done_steps': sorted(done),
            'missing_steps': sorted(missing),
        }))
        return

    print('Thank you for choosing our services. We are committed to providing you with the best experience possible!')
    if not feedback_submitted:
        print('No feedback submitted.')
        return

    print('Your feedback will be used to improve our services and ensure a better experience for all customers.')
    if args.format == 'scrum':
        print(eight_d.inform_scrum())
    else:
        print(ReportGenerator(report).scrum_report())

    if done:
        print('Done:')
        for step in sorted(done):
            print(f'- {step}')

    if missing:
        print(f'\nDoing: {sorted(missing)[0]}')
        print('\nTodo:')
        for next_step in sorted(missing):
            print(f'- {next_step}')
    else:
        print(eight_d.congratulate_team())


def log_feedback(feedback: CustomerFeedback):
    pass


def main():
    args = parse_args()
    try:
        customer_service_chatbot(args)
    except KeyboardInterrupt:
        print('\nAborted by user.')
        raise SystemExit(130)


if __name__ == '__main__':
    main()
