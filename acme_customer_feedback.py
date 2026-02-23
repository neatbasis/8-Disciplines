#!/usr/bin/env python3
import os
import sys
import json
import pytz
import argparse
import openai
from dotenv import load_dotenv

load_dotenv()

from rich.console import Console
console = Console()

parser = argparse.ArgumentParser(description='8-Disciplines Problem Solving')
parser.add_argument('--use-defaults', dest='use_defaults', action='store_true')
parser.set_defaults(use_defaults=False)
#parser.add_argument('search', metavar='SEARCH', type=str, help='the phrase to search')

args = parser.parse_args()

try:

    import sys
    from typing import Optional, Dict
    import json
    import os
    from reportgenerator import ReportGenerator
    import json
    from survey_tools import CustomerFeedback, get_input, get_customer_feedback, get_customer_contact, get_issue

    # In case lack of data, invent your own scenarios with LLMs
    class EightDisciplines:
        def __init__(self, issue):
            self.EIGHT_DISCIPLINES = ['plan', 'prerequisites', 'team', 'problem_description', 'interim_containment_plan', 'root_causes', 'permanent_corrections', 'corrective_actions', 'preventive_measures']
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
            # Generate an explanation, the values and the reason behind the implemented change, the value it brings to both internal and external customers
            self.congratulations = ReportGenerator.congrats_template(report)
            return self.congratulations
            
        def inform_scrum(self):
            report = self.generate_machine_readable_report()
            generator = ReportGenerator(report)
            text = f"----------- SCRUM REPORT -------------\n"
            text += f"{generator.scrum_report()}\n"
            text += f"------- END OF SCRUM REPORT-----------\n"
            return text
            
        # Doing many small things right is the way to doing big things
        def generate_work(self):
            self.plan_solving_problem("Investigate and fix website performance issues", "Access to website logs")
            self.use_team(["John", "Mary", "David"])
            self.define_problem("Our website is slow and sometimes unresponsive, causing poor user experience.")
            self.develop_interim_containment_plan("Limit website traffic to reduce load on servers.")
            self.determine_root_causes("High traffic volume and inadequate server resources.")
            print(self.inform_scrum())
            
            self.choose_permanent_corrections("Upgrade server resources and optimize website code.")
            self.implement_corrective_actions("Upgraded server resources and optimized website code.")
            self.take_preventive_measures("Regularly monitor website performance and upgrade resources as needed.")
            #self.congratulate_team()
            
        def generate_machine_readable_report(self) -> Dict[str, str]:
            if self.plan is None:
                plan = None
                prerequisites = None
            else:
                plan = self.plan[0]
                prerequisites = self.plan[1]
                
            report = {
                "issue": self.issue,
                "plan": plan, # Starts with plan zero... interesting, creating new plans could be as easy as adding one to the index with plan and prerequisites 🤔
                "prerequisites": prerequisites,
                "team": self.team,
                "problem_description": self.problem_description,
                "interim_containment_plan": self.interim_containment_plan,
                "root_causes": self.root_causes,
                "permanent_corrections": self.permanent_corrections,
                "corrective_actions": self.corrective_actions,
                "preventive_measures": self.preventive_measures
            }
            return report
      
    DEFAULTS_FILE = "customer_defaults.json"

    def load_defaults():
        if os.path.exists(DEFAULTS_FILE):
            with open(DEFAULTS_FILE, "r") as f:
                defaults = json.load(f)
        else:
            defaults = {
                "name": "",
                "phone_number": "",
                "email": "",
                "feedback": "",
                "what_happened": "",
                "when_happened": "",
                "where_happened": "",
                "expecting_to_happen": "",
                "resolution_request": ""
            }
        return defaults

    def save_defaults(defaults):
        with open(DEFAULTS_FILE, "w") as f:
            json.dump(defaults, f)

    def customer_service_chatbot():
        # Load default values
        defaults = load_defaults()
        feedback = ""
        issue = get_issue(defaults)

        # Personalized interactions
        if args.use_defaults:
            feedback = "yes"
            issue = get_issue(defaults)
        
        if args.use_defaults is not True and sys.stdin.isatty():
            defaults = get_customer_contact(defaults)
        #else:
        #    user_name = defaults.get('name', 'User ')
        #    phone_number = defaults.get('phone_number', 'Phone number ')
        #    email = defaults.get('email', 'Email ')

        # Clear and concise communication
        print('How can we help you today?')

        # Attentiveness to customer feedback
        if args.use_defaults is not True and sys.stdin.isatty():
            defaults, feedback, issue = get_customer_feedback(defaults)

        # Save default values
        save_defaults(defaults)

        # Positive language and notification about feedback usage
        print('Thank you for choosing our services. We are committed to providing you with the best experience possible!')
        if feedback:
            print("Your feedback will be used to improve our services and ensure a better experience for all customers.")
            eight_d = EightDisciplines(issue)
            report = eight_d.generate_machine_readable_report()
            missing = ReportGenerator.check_empty_values(report)
            done = ReportGenerator.check_nonempty_values(report)
            print(eight_d.inform_scrum())
            
            
            if len(done) > 0:
                print(f"Done:")
                for step in done:
                    print(f"- {step}")
                
            if len(missing) > 0:
                print(f"\nDoing: {missing[0]}")
                
                print(f"\nTodo:")
                for next_step in missing:
                    print(f"- {next_step}")
            else:
                congratulations = eight_d.congratulate_team()
                print(congratulations)
            
            #eight_d.generate_work()
            #print(eight_d.inform_scrum())
            # Received customer feedback
            # Investigated the root cause of the feedback
            # Identified solutions to the feedback")
            # Implemented changes to improve the customer experience
            


    def log_feedback(feedback: CustomerFeedback):
        # Implement logging logic using Lean Six-Sigma principles
        # ...
        pass

    if __name__ == "__main__":
        customer_service_chatbot()
except Exception:
    console.print_exception(show_locals=True)
