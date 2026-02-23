from dataclasses import asdict, dataclass
from typing import Any, Callable, Optional


def _normalize_optional(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def _has_value(value: Any) -> bool:
    return _normalize_optional(value) is not None


@dataclass
class CustomerFeedback:
    feedback: str
    rating: Optional[int]


@dataclass
class CustomerContact:
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None

    @staticmethod
    def from_defaults(defaults: dict) -> "CustomerContact":
        return CustomerContact(
            name=_normalize_optional(defaults.get("name")),
            phone_number=_normalize_optional(defaults.get("phone_number", defaults.get("phone"))),
            email=_normalize_optional(defaults.get("email")),
        )

    def to_defaults(self, defaults: dict) -> dict:
        defaults.update(asdict(self))
        defaults.pop("phone", None)
        return defaults


@dataclass
class CustomerIssue:
    what_happened: Optional[str] = None
    when_happened: Optional[str] = None
    where_happened: Optional[str] = None
    expecting_to_happen: Optional[str] = None
    resolution_request: Optional[str] = None

    @staticmethod
    def from_defaults(defaults: dict) -> "CustomerIssue":
        return CustomerIssue(
            what_happened=_normalize_optional(defaults.get("what_happened")),
            when_happened=_normalize_optional(defaults.get("when_happened")),
            where_happened=_normalize_optional(defaults.get("where_happened")),
            expecting_to_happen=_normalize_optional(defaults.get("expecting_to_happen")),
            resolution_request=_normalize_optional(defaults.get("resolution_request")),
        )

    def to_defaults(self, defaults: dict) -> dict:
        defaults.update(asdict(self))
        return defaults

    def to_dict(self) -> dict:
        return asdict(self)


def prompt_for_rating(input_fn: Callable[[str], str] = input, print_fn: Callable[[str], None] = print) -> Optional[int]:
    while True:
        rating_str = input_fn('On a scale of 1 to 10, how would you rate your experience with us? (Enter 0 for no rating) ')
        try:
            rating = int(rating_str)
            if rating < 0 or rating > 10:
                print_fn('Please enter a rating between 1 and 10, or 0 for no rating.')
                continue
            return rating
        except ValueError:
            print_fn('Please enter a valid integer rating, or 0 for no rating.')


def prompt_yn(
    prompt: str,
    *,
    default: bool,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
) -> bool:
    suffix = " (Y/n) " if default else " (y/N) "
    while True:
        response = input_fn(prompt + suffix).strip().lower()
        if response == "":
            return default
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print_fn("Please answer Y or n.")


def prompt_text(
    prompt: str,
    *,
    allow_skip: bool,
    input_fn: Callable[[str], str] = input,
) -> Optional[str]:
    if allow_skip:
        prompt = f"{prompt} (optional, press Enter to skip)"
    response = input_fn(prompt + ": ").strip()
    return response if response else None


def get_input(
    key: str,
    label: str,
    defaults: Optional[dict] = None,
    *,
    allow_skip: bool = False,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
):
    if defaults is None:
        defaults = {}

    current = defaults.get(key)
    if not _has_value(current):
        defaults[key] = prompt_text(
            f"Please enter your {label}",
            allow_skip=allow_skip,
            input_fn=input_fn,
        )
        return defaults

    is_correct = prompt_yn(
        f"Your {label} is {current}. Is this correct?",
        default=True,
        input_fn=input_fn,
        print_fn=print_fn,
    )
    if not is_correct:
        defaults[key] = prompt_text(
            f"What is your {label}",
            allow_skip=allow_skip,
            input_fn=input_fn,
        )

    return defaults


def get_customer_contact(defaults, *, input_fn: Callable[[str], str] = input, print_fn: Callable[[str], None] = print):
    contact = CustomerContact.from_defaults(defaults)
    contact_defaults = asdict(contact)

    contact_defaults = get_input('name', 'Name', contact_defaults, input_fn=input_fn, print_fn=print_fn)
    if _has_value(contact_defaults.get("name")):
        print_fn(f'Hello, {contact_defaults["name"]}!')

    contact_defaults = get_input('phone_number', 'Phone number', contact_defaults, allow_skip=True, input_fn=input_fn, print_fn=print_fn)
    contact_defaults = get_input('email', 'Email', contact_defaults, allow_skip=True, input_fn=input_fn, print_fn=print_fn)

    updated_contact = CustomerContact(**contact_defaults)
    return updated_contact.to_defaults(defaults)


def get_issue(defaults):
    return CustomerIssue.from_defaults(defaults).to_dict()


def get_customer_feedback(defaults, *, input_fn: Callable[[str], str] = input, print_fn: Callable[[str], None] = print):
    wants_feedback = prompt_yn(
        "Would you like to leave feedback?",
        default=False,
        input_fn=input_fn,
        print_fn=print_fn,
    )

    if not wants_feedback:
        return defaults, False, CustomerIssue().to_dict()

    print_fn('Thanks — please provide a bit more detail. You can skip optional questions.\n')
    issue_defaults = asdict(CustomerIssue.from_defaults(defaults))
    issue_defaults = get_input('what_happened', 'What happened', issue_defaults, input_fn=input_fn, print_fn=print_fn)
    issue_defaults = get_input('when_happened', 'When did it happen', issue_defaults, allow_skip=True, input_fn=input_fn, print_fn=print_fn)
    issue_defaults = get_input('where_happened', 'Where did it happen', issue_defaults, allow_skip=True, input_fn=input_fn, print_fn=print_fn)
    issue_defaults = get_input('expecting_to_happen', 'What were you expecting to happen', issue_defaults, input_fn=input_fn, print_fn=print_fn)
    issue_defaults = get_input('resolution_request', 'What would you like us to do to resolve the issue', issue_defaults, allow_skip=True, input_fn=input_fn, print_fn=print_fn)

    issue_model = CustomerIssue(**issue_defaults)
    defaults = issue_model.to_defaults(defaults)
    return defaults, True, issue_model.to_dict()
