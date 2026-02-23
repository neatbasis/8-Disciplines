import unittest

from eight_disciplines.survey_tools import get_input, prompt_yn


class TestPrompts(unittest.TestCase):
    def test_prompt_yn_reprompts_invalid(self):
        answers = iter(["maybe", "y"])
        printed = []

        def input_fn(_):
            return next(answers)

        def print_fn(msg):
            printed.append(msg)

        result = prompt_yn("Continue?", default=False, input_fn=input_fn, print_fn=print_fn)
        self.assertTrue(result)
        self.assertIn("Please answer Y or n.", printed)

    def test_get_input_does_not_confirm_blank_value(self):
        answers = iter(["Alice"])
        prompts = []

        def input_fn(prompt):
            prompts.append(prompt)
            return next(answers)

        defaults = {"name": None}
        updated = get_input("name", "Name", defaults, input_fn=input_fn)

        self.assertEqual(updated["name"], "Alice")
        self.assertTrue(any("Please enter your Name" in p for p in prompts))
        self.assertFalse(any("Is this correct" in p for p in prompts))


if __name__ == "__main__":
    unittest.main()
