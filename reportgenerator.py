import textwrap

def _is_missing(value):
    if value is None:
        return True
    if isinstance(value, dict):
        return all(_is_missing(v) for v in value.values())
    return False


class ReportGenerator:
    def __init__(self, report):
        self.report = report
        self.phrases = {
        "issue": {
            "todo": "address the issue gifted to us by our dear customer",
            "done": "received the issue from our dear customer",
            "definition_complete": "The issue has been acknowledged"
        },
        "plan": {
            "todo": "create a plan to address the issue",
            "done": "created a plan to address the issue",
            "definition_complete": "A plan has been created and approved to address the issue."
        },
        "prerequisites": {
            "todo": "identify the prerequisites needed to carry out the plan",
            "done": "identified the prerequisites needed to carry out the plan",
            "definition_complete": "All necessary prerequisites have been identified and are available to carry out the plan."
        },
        "team": {
            "todo": "assemble the team of people with product/process knowledge to carry out the plan",
            "done": "assembled the team of people with product/process knowledge to carry out the plan",
            "definition_complete": "A team with the appropriate knowledge and skills has been assembled to carry out the plan."
        },
        "problem_description": {
            "todo": "specify the problem by identifying in quantifiable terms the who, what, where, when, why, how, and how many (5W2H) for the problem",
            "done": "specified the problem by identifying in quantifiable terms the who, what, where, when, why, how, and how many (5W2H) for the problem.",
            "definition_complete": "The problem has been described in detail identifying in quantifiable terms the who, what, where, when, why, how, and how many (5W2H) for the problem."
        },
        "interim_containment_plan": {
            "todo": "define and implement containment actions to isolate the problem from any customer",
            "done": "defined and implemented containment actions to isolate the problem from any customer",
            "definition_complete": "An interim containment plan has been put in place to isolate the problem from any customers."
        },
        "root_causes": {
            "todo": "determine, identify and verify all applicable causes that could explain why the problem occurred",
            "done": "determined, identified and verified all applicable causes that could explain why the problem occurred",
            "definition_complete": "All applicable causes of the problem have been identified and verified, and a clear understanding of why the problem was not noticed at the time it occurred has been determined."
        },
        "permanent_corrections": {
            "todo": "develop a set of permanent corrections to address the root causes",
            "done": "developed a set of permanent corrections to address the root causes",
            "definition_complete": "A set of permanent corrections has been developed and implemented to address the root causes of the problem."
        },
        "corrective_actions": {
            "todo": "carry out corrective actions to address the immediate symptoms",
            "done": "carried out corrective actions to address the immediate symptoms",
            "definition_complete": "Corrective actions have been taken to address the immediate symptoms of the problem."
        },
        "preventive_measures": {
            "todo": "put in place preventive measures to ensure the problem doesn't recur",
            "done": "put in place preventive measures to ensure the problem doesn't recur",
            "definition_complete": "Completed modifications of the management systems, operation systems, practices, and procedures to prevent recurrence of this and all similar problems"
        }
    }
    @staticmethod
    def congrats_template(report: dict) -> str:
        """
        Generates a congratulatory email template for the team based on the details provided in the report.
    
        Args:
            report (dict): A dictionary containing the details of the team's accomplishment.
    
        Returns:
            str: A string containing the congratulatory email template with the relevant details from the report.
        """
        congratulatory_message = f"Dear {ReportGenerator.join_names(report['team'])},\n\n"
        congratulatory_message += f"Congratulations on successfully resolving the issue {report['issue']['what_happened']} {report['issue']['where_happened']}! "
        congratulatory_message += f"Your hard work and dedication to developing a solution is truly commendable.\n\n"
        congratulatory_message += f"The plan you developed to address the issue with {report['plan']} and the following prerequisites: {report['prerequisites']} was effective in solving the problem. Your problem description: {report['problem_description']} and interim containment plan: {report['interim_containment_plan']} helped to prevent the issue from recurring. "
        congratulatory_message += f"The root causes: {report['root_causes']}, permanent corrections: {report['permanent_corrections']}, corrective actions: {report['corrective_actions']} and preventive measures: {report['preventive_measures']} were well thought out and implemented.\n\n"
        congratulatory_message += f"Again, congratulations on this achievement! Your hard work and dedication to continuous improvement is appreciated by both internal and external customers.\n\n"
        congratulatory_message += "Sincerely,\n[Your Name]"

        return congratulatory_message
    @staticmethod
    def check_empty_values(report):
        return [key for key, value in report.items() if _is_missing(value)]

    @staticmethod
    def check_nonempty_values(report):
        return {key for key, value in report.items() if not _is_missing(value)}
        
    @staticmethod
    def get_issue_text(issue):
        what_happened = issue.get('what_happened', 'Unknown')
        when_happened = issue.get('when_happened', 'Unknown')
        where_happened = issue.get('where_happened', 'Unknown')
        expecting_to_happen = issue.get('expecting_to_happen', 'Unknown')
        resolution_request = issue.get('resolution_request', 'Unknown')
        
        text = f"- {what_happened}\n"
        text += f"  - When: {when_happened}\n"
        text += f"  - Where: {where_happened}\n"
        text += f"  - Expecting to happen: {expecting_to_happen}\n"
        text += f"  - Resolution request: {resolution_request}\n"
        return text

    @staticmethod
    def join_names(names):
        if names is not None and len(names) >= 1:
            return ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
        else:
            return "Unknown"
        
    def _check_empty_values(self, report):
        return set(self.check_empty_values(report))

    def _check_nonempty_values(self, report):
        all_steps = set(self.phrases.keys())
        nonempty = set(self.check_nonempty_values(report))
        return all_steps.intersection(nonempty)
        
    def scrum_report(self):
        #with Progress() as progress:
        #    task = progress.add_task("Working", total=100)
        #    progress.update(task, advance=22)
        missing = self._check_empty_values(self.report)
        done = self._check_nonempty_values(self.report)
        issue_text = self.get_issue_text(self.report['issue'])
        what_happened = self.report['issue'].get('what_happened', 'Unknown')
        when_happened = self.report['issue'].get('when_happened', 'Unknown')
        where_happened = self.report['issue'].get('where_happened', 'Unknown')
        expecting_to_happen = self.report['issue'].get('expecting_to_happen', 'Unknown')
        resolution_request = self.report['issue'].get('resolution_request', 'Unknown')
        report_string = f"A customer has an issue:\n{textwrap.indent(issue_text, ' ' * 4)}\n"
        report_string += f"A quick update on our progress.\n"
        done_descriptions = []
        missing_descriptions = []
        for key in self.phrases:
            if key in done:
                done_descriptions.append(key)
            elif key in missing:
                missing_descriptions.append(key)
        if done_descriptions:
            report_string += f"\nHere's what we've accomplished so far:\n\n"
            for d in done_descriptions:
                did = self.phrases[d]['done']
                detail = self.report[d]
                report_string += f"    - We {did}.\n"
                if d == 'issue':
                    report_string += f"       - Expectation: {expecting_to_happen}\n"
                    report_string += f"       - Reality: {what_happened}\n"
                    report_string += f"       - When: {when_happened}\n"
                    report_string += f"       - Where: {where_happened}\n"
                    report_string += f"       - Request: {resolution_request}\n"
                    expecting_to_happen
                elif d == 'team':
                    report_string += f"       - {self.join_names(detail)}\n"
                else:
                    report_string += f"       - {detail}\n"
        else:
            report_string += f"\nWe haven't completed any steps yet. [insert instructions here]\n"
        if missing_descriptions:
            report_string += f"\nLet's focus on completing the missing steps. Here's a quick reminder of what we need to do:\n\n"
            for d in missing_descriptions:
                definition_complete = self.phrases[d]['definition_complete']
                todo = self.phrases[d]['todo']
                report_string += f"    - We need to {todo}.\n"
                report_string += f"       - Definition of complete: {definition_complete}\n"
                if d == 'issue':
                    report_string += f"Find out why the issue is missing\n"
        else:
            report_string += f"\nWe've completed all the steps!"
        return report_string



                
