from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class CustomerFeedback:
    feedback: str
    rating: Optional[int]


@dataclass
class CustomerContact:
    name: str = ""
    phone_number: str = ""
    email: str = ""

    @staticmethod
    def from_defaults(defaults: dict) -> "CustomerContact":
        return CustomerContact(
            name=defaults.get("name", ""),
            phone_number=defaults.get("phone_number", defaults.get("phone", "")),
            email=defaults.get("email", ""),
        )

    def to_defaults(self, defaults: dict) -> dict:
        defaults.update(asdict(self))
        defaults.pop("phone", None)
        return defaults


@dataclass
class CustomerIssue:
    what_happened: str = ""
    when_happened: str = ""
    where_happened: str = ""
    expecting_to_happen: str = ""
    resolution_request: str = ""

    @staticmethod
    def from_defaults(defaults: dict) -> "CustomerIssue":
        return CustomerIssue(
            what_happened=defaults.get("what_happened", ""),
            when_happened=defaults.get("when_happened", ""),
            where_happened=defaults.get("where_happened", ""),
            expecting_to_happen=defaults.get("expecting_to_happen", ""),
            resolution_request=defaults.get("resolution_request", ""),
        )

    def to_defaults(self, defaults: dict) -> dict:
        defaults.update(asdict(self))
        return defaults

    def to_dict(self) -> dict:
        return asdict(self)


def prompt_for_rating() -> Optional[int]:
    while True:
        rating_str = input('On a scale of 1 to 10, how would you rate your experience with us? (Enter 0 for no rating) ')
        try:
            rating = int(rating_str)
            if rating < 0 or rating > 10:
                print('Please enter a rating between 1 and 10, or 0 for no rating.')
                continue
            else:
                return rating
        except ValueError:
            print('Please enter a valid integer rating, or 0 for no rating.')


def get_input(key, label, defaults=None):
    if defaults is None:
        defaults = {}

    if key in defaults:
        response = input(f'Your {label} is {defaults[key]}. Is this correct? (Y/n) ')
        if response.strip().lower() in ('no', 'n'):
            value = input(f'What is your {key}? ')
            defaults[key] = value
    else:
        value = input(f'Please enter your {key}: ')
        defaults[key] = value
    return defaults


def get_customer_contact(defaults):
    contact = CustomerContact.from_defaults(defaults)
    contact_defaults = asdict(contact)

    contact_defaults = get_input('name', 'Name', contact_defaults)
    print(f'Hello, {contact_defaults["name"]}!')
    contact_defaults = get_input('phone_number', 'Phone number', contact_defaults)
    contact_defaults = get_input('email', 'Email', contact_defaults)

    updated_contact = CustomerContact(**contact_defaults)
    return updated_contact.to_defaults(defaults)


def get_issue(defaults):
    return CustomerIssue.from_defaults(defaults).to_dict()


def get_customer_feedback(defaults):
    feedback = input('Do you have any feedback for us? ')
    if feedback:
        print('Thank you for your feedback! Can you please provide us with more details about the issue?')
        print('Some questions that may help you give us more detail:')
        issue_defaults = asdict(CustomerIssue.from_defaults(defaults))
        issue_defaults = get_input('what_happened', 'What happened?', issue_defaults)
        issue_defaults = get_input('when_happened', 'When did it happen?', issue_defaults)
        issue_defaults = get_input('where_happened', 'Where did it happen?', issue_defaults)
        issue_defaults = get_input('expecting_to_happen', 'What were you expecting to happen?', issue_defaults)
        issue_defaults = get_input('resolution_request', 'What would you like us to do to resolve the issue?', issue_defaults)

        issue_model = CustomerIssue(**issue_defaults)
        defaults = issue_model.to_defaults(defaults)
        issue = issue_model.to_dict()
    else:
        issue = CustomerIssue(
            what_happened='Our website is sometimes unresponsive.',
            when_happened='Over the past week.',
            where_happened='On feedback requests on our website',
            expecting_to_happen='We expect the website to work well at all times.',
            resolution_request='Please investigate and fix the performance issues on our website.',
        ).to_dict()
        print('Sorry to hear that. Can you please provide us with more details about what went wrong?')

    return defaults, feedback, issue
