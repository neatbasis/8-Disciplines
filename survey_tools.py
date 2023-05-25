from typing import Optional
class CustomerFeedback:
    def __init__(self, feedback: str, rating: Optional[int]):
        self.feedback = feedback
        self.rating = rating
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

def get_input(key, label, defaults=[]):
    # Ask for input
    if key in defaults:
        response = input(f'Your {label} is {defaults[key]}. Is this correct? (Y/n) ')
        if response.strip().lower() in ('no', 'n'):
            value = input(f'What is your {key}? ')
            defaults[key] = value
        else:
            value = defaults[key]
    else:
        value = input(f'Please enter your {key}: ')
        defaults[key] = value
    return defaults

def get_customer_contact(defaults):
    # Ask for user name
    defaults = get_input('name', 'Name', defaults)
    print(f'Hello, {defaults["name"]}!')
    # Ask for phone number
    defaults = get_input('phone_number', 'Phone number', defaults)
    # Ask for email
    defaults = get_input('email', 'Email', defaults)
    return defaults
    
def get_issue(defaults):
    issue = {
        "what_happened": defaults['what_happened'],
        "when_happened": defaults['when_happened'],
        "where_happened": defaults['where_happened'],
        "expecting_to_happen": defaults['expecting_to_happen'],
        "resolution_request": defaults['resolution_request']
    }
    return issue
        
def get_customer_feedback(defaults):
    feedback = input('Do you have any feedback for us? ')
    if feedback:
        print('Thank you for your feedback! Can you please provide us with more details about the issue?')
        print('Some questions that may help you give us more detail:')
        defaults = get_input('what_happened', 'What happened?', defaults)
        defaults = get_input('when_happened', 'When did it happen?', defaults)
        defaults = get_input('where_happened', 'Where did it happen?', defaults)
        defaults = get_input('expecting_to_happen', 'What were you expecting to happen?', defaults)
        defaults = get_input('resolution_request', 'What would you like us to do to resolve the issue?', defaults)

        issue = get_issue(defaults)

    else:
        issue = {
            "what_happened": "Our website is sometimes unresponsive.",
            "when_happened": "Over the past week.",
            "where_happened": "On feedback requests on our website",
            "expecting_to_happen": "We expect the website to work well at all times.",
            "resolution_request": "Please investigate and fix the performance issues on our website."
        }
        print("Sorry to hear that. Can you please provide us with more details about what went wrong?")
        
    return defaults, feedback, issue
