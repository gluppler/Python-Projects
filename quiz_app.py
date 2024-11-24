import json
from typing import List

# -------------------------------------------------------------------
# Core Question Classes
# -------------------------------------------------------------------

class Question:
    """
    Base class for all types of questions.
    Handles the basic functionality for questions like storing text,
    checking correctness, and serializing/deserializing.
    """
    def __init__(self, question_text, correct_answer):
        self.question_text = question_text
        self.correct_answer = correct_answer

    def is_correct(self, answer):
        """
        Check if the given answer is correct.
        Compares the user's answer with the correct answer, ignoring case.
        """
        return answer.strip().lower() == self.correct_answer.strip().lower()

    def display(self):
        """
        Display the question text.
        Intended to be overridden by subclasses for additional functionality.
        """
        print(self.question_text)

    def to_dict(self):
        """
        Convert the question to a dictionary for saving to a file.
        This method enables serialization.
        """
        return {
            "type": "Question",
            "question_text": self.question_text,
            "correct_answer": self.correct_answer
        }

    @staticmethod
    def from_dict(data):
        """
        Reconstruct a Question object from its dictionary representation.
        Used when loading questions from a file.
        """
        return Question(data["question_text"], data["correct_answer"])


class MultipleChoiceQuestion(Question):
    """
    Specialized class for multiple-choice questions.
    Extends the base Question class by adding choices functionality.
    """
    def __init__(self, question_text, choices, correct_answer):
        super().__init__(question_text, correct_answer)
        self.choices = choices

    def display(self):
        """
        Display the question along with multiple-choice options.
        """
        super().display()
        for idx, choice in enumerate(self.choices, 1):
            print(f"{idx}. {choice}")

    def is_correct(self, answer):
        """
        Check if the selected choice matches the correct answer.
        Converts user input (number) into the corresponding choice text.
        """
        try:
            selected_index = int(answer) - 1
            return self.choices[selected_index].strip().lower() == self.correct_answer.strip().lower()
        except (ValueError, IndexError):
            return False

    def to_dict(self):
        """
        Serialize the question into a dictionary including choices.
        """
        return {
            "type": "MultipleChoice",
            "question_text": self.question_text,
            "choices": self.choices,
            "correct_answer": self.correct_answer
        }

    @staticmethod
    def from_dict(data):
        """
        Reconstruct a MultipleChoiceQuestion from a dictionary.
        """
        return MultipleChoiceQuestion(data["question_text"], data["choices"], data["correct_answer"])


class TrueFalseQuestion(Question):
    """
    Specialized class for true/false questions.
    Extends the base Question class by limiting answers to True/False.
    """
    def __init__(self, question_text, correct_answer):
        super().__init__(question_text, correct_answer)

    def display(self):
        """
        Display the question along with True/False options.
        """
        super().display()
        print("1. True")
        print("2. False")

    def to_dict(self):
        """
        Serialize the question into a dictionary.
        """
        return {
            "type": "TrueFalse",
            "question_text": self.question_text,
            "correct_answer": self.correct_answer
        }

    @staticmethod
    def from_dict(data):
        """
        Reconstruct a TrueFalseQuestion from a dictionary.
        """
        return TrueFalseQuestion(data["question_text"], data["correct_answer"])


# -------------------------------------------------------------------
# Quiz Management
# -------------------------------------------------------------------

class QuizManager:
    """
    Handles the creation, editing, saving, and loading of quizzes.
    Responsible for persistence and organization of multiple quizzes.
    """
    def __init__(self, filename="quizzes.json"):
        self.filename = filename  # File where quizzes are stored
        self.quizzes = self.load_quizzes()  # Load quizzes on startup

    def load_quizzes(self):
        """
        Load quizzes from a JSON file.
        Returns a dictionary where keys are quiz names and values are lists of questions.
        """
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                # Convert dictionary data into Question objects
                return {name: [self.create_question(q) for q in questions] for name, questions in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_quizzes(self):
        """
        Save quizzes to a JSON file.
        Converts Question objects into dictionaries for serialization.
        """
        with open(self.filename, "w") as file:
            json.dump({name: [q.to_dict() for q in questions] for name, questions in self.quizzes.items()}, file, indent=4)

    @staticmethod
    def create_question(data):
        """
        Dynamically create a Question object based on its type.
        Supports multiple question types like 'MultipleChoice' and 'TrueFalse'.
        """
        question_type = data["type"]
        if question_type == "MultipleChoice":
            return MultipleChoiceQuestion.from_dict(data)
        elif question_type == "TrueFalse":
            return TrueFalseQuestion.from_dict(data)
        else:
            return Question.from_dict(data)

    def display_quizzes(self):
        """
        Print the list of available quizzes.
        """
        print("\nAvailable Quizzes:")
        for idx, quiz_name in enumerate(self.quizzes.keys(), 1):
            print(f"{idx}. {quiz_name}")
        print()

    def add_quiz(self, quiz_name):
        """
        Add a new quiz to the manager.
        """
        if quiz_name in self.quizzes:
            print("Quiz already exists!")
        else:
            self.quizzes[quiz_name] = []
            print(f"Quiz '{quiz_name}' created.")

    def edit_quiz(self, quiz_name):
        """
        Edit an existing quiz by adding/removing questions or viewing them.
        """
        if quiz_name not in self.quizzes:
            print("Quiz not found!")
            return

        while True:
            print(f"\nEditing Quiz: {quiz_name}")
            print("1. Add Question")
            print("2. Remove Question")
            print("3. View Questions")
            print("4. Done")
            choice = input("Select an option: ")

            if choice == "1":
                self.add_question_to_quiz(quiz_name)
            elif choice == "2":
                self.remove_question_from_quiz(quiz_name)
            elif choice == "3":
                self.view_questions(quiz_name)
            elif choice == "4":
                break
            else:
                print("Invalid option!")

    def add_question_to_quiz(self, quiz_name):
        """
        Add a new question to the specified quiz.
        Supports multiple question types.
        """
        print("\nAdding a Question:")
        print("1. Multiple Choice")
        print("2. True/False")
        print("3. Basic Question")
        choice = input("Select question type: ")

        if choice == "1":
            question_text = input("Enter question text: ")
            choices = input("Enter choices (comma-separated): ").split(",")
            correct_answer = input("Enter the correct answer: ")
            question = MultipleChoiceQuestion(question_text, choices, correct_answer)
        elif choice == "2":
            question_text = input("Enter question text: ")
            correct_answer = input("Enter correct answer (True/False): ")
            question = TrueFalseQuestion(question_text, correct_answer)
        elif choice == "3":
            question_text = input("Enter question text: ")
            correct_answer = input("Enter correct answer: ")
            question = Question(question_text, correct_answer)
        else:
            print("Invalid option!")
            return

        self.quizzes[quiz_name].append(question)
        print("Question added!")

    def remove_question_from_quiz(self, quiz_name):
        """
        Remove a question from the specified quiz.
        Lists all questions for selection.
        """
        questions = self.quizzes[quiz_name]
        if not questions:
            print("No questions to remove!")
            return

        for idx, question in enumerate(questions, 1):
            print(f"{idx}. {question.question_text}")

        try:
            choice = int(input("Enter question number to remove: "))
            if 1 <= choice <= len(questions):
                removed_question = questions.pop(choice - 1)
                print(f"Removed question: {removed_question.question_text}")
            else:
                print("Invalid question number!")
        except ValueError:
            print("Invalid input!")

    def view_questions(self, quiz_name):
        """
        View all questions in the specified quiz.
        """
        print(f"\nQuestions in Quiz '{quiz_name}':")
        for idx, question in enumerate(self.quizzes[quiz_name], 1):
            print(f"{idx}. {question.question_text}")
        print()


# -------------------------------------------------------------------
# Quiz Execution
# -------------------------------------------------------------------

class Quiz:
    """
    Runs a quiz for the user and evaluates their answers.
    """
    def __init__(self, questions: List[Question]):
        self.questions = questions
        self.score = 0

    def start(self):
        """
        Start the quiz by displaying questions and recording answers.
        Provides feedback for each answer and calculates the final score.
        """
        print("Starting the Quiz!")
        print("-" * 30)

        for idx, question in enumerate(self.questions, 1):
            print(f"\nQuestion {idx}:")
            question.display()
            answer = input("Your answer: ")
            if question.is_correct(answer):
                print("Correct!")
                self.score += 1
            else:
                print(f"Wrong! The correct answer was: {question.correct_answer}")

        print("-" * 30)
        print(f"Quiz Finished! Your score: {self.score}/{len(self.questions)}")


# -------------------------------------------------------------------
# Main Program Loop
# -------------------------------------------------------------------

def main():
    """
    Main entry point for the application.
    Displays the menu and handles user input for quiz management.
    """
    manager = QuizManager()

    while True:
        print("\nQuiz Manager")
        print("1. View Quizzes")
        print("2. Add Quiz")
        print("3. Edit Quiz")
        print("4. Take Quiz")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            manager.display_quizzes()
        elif choice == "2":
            quiz_name = input("Enter new quiz name: ")
            manager.add_quiz(quiz_name)
        elif choice == "3":
            quiz_name = input("Enter quiz name to edit: ")
            manager.edit_quiz(quiz_name)
        elif choice == "4":
            quiz_name = input("Enter quiz name to take: ")
            if quiz_name in manager.quizzes:
                quiz = Quiz(manager.quizzes[quiz_name])
                quiz.start()
            else:
                print("Quiz not found!")
        elif choice == "5":
            manager.save_quizzes()
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()

