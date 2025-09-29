import re
import nltk
from nltk.tokenize import regexp_tokenize
from nltk import pos_tag
import random
import pdfplumber
from docx import Document
import tkinter as tk
from tkinter import filedialog, scrolledtext


# nltk.download('averaged_perceptron_tagger_eng') run this line when running the code for first time after that no need to rerun this line

# Text Extraction Functions
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def custom_sent_tokenize(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# Quiz Generation
def generate_quiz(text, num_questions=5):
    sentences = custom_sent_tokenize(text)
    words = regexp_tokenize(text, r'\w+|[^\w\s]')
    tagged_words = pos_tag(words)
    distractors = [word for word, pos in tagged_words if pos.startswith('NN') or pos.startswith('VB')]
    distractors = list(set(distractors))

    questions = []
    for _ in range(num_questions):
        if not sentences:
            break
        sentence = random.choice(sentences)
        words = regexp_tokenize(sentence, r'\w+|[^\w\s]')
        tagged_words = pos_tag(words)
        candidates = [word for word, pos in tagged_words if pos.startswith('NN') or pos.startswith('VB')]
        if not candidates:
            continue
        word_to_remove = random.choice(candidates)
        question = sentence.replace(word_to_remove, "______", 1)

        correct_answer = word_to_remove
        options = [correct_answer]
        while len(options) < 4:
            distractor = random.choice(distractors)
            if distractor != correct_answer and distractor not in options:
                options.append(distractor)
        random.shuffle(options)

        questions.append((question, correct_answer, options))
        sentences.remove(sentence)

    return questions

# GUI Setup
root = tk.Tk()
root.title("Automatic Quiz System")
root.geometry("800x600")
root.resizable(False, False)

# Global state
quiz_data = []
current_question_index = 0
user_answers = []
correct_answers = []

# Navigation functions
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def main_menu():
    clear_window()
    tk.Label(root, text="Select Mode", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Quiz Generation", command=quiz_generation_interface, width=30).pack(pady=10)
    tk.Button(root, text="Quiz Assessment", command=quiz_assessment_interface, width=30).pack(pady=10)

def back_to_main_menu():
    main_menu()

# Quiz Generation Interface
def quiz_generation_interface():
    clear_window()

    def select_file():
        file_path = filedialog.askopenfilename()
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

    def generate_callback():
        try:
            file_path = entry_file_path.get()
            num_questions = int(entry_num_questions.get())
            method = radio_selection.get()

            if method == "pdf":
                text = extract_text_from_pdf(file_path)
            elif method == "docx":
                text = extract_text_from_docx(file_path)
            elif method == "manual":
                text = text_box.get(1.0, tk.END).strip()
            else:
                output_box.insert(tk.END, "Invalid input method selected!\n")
                return

            quiz = generate_quiz(text, num_questions)
            output_box.delete(1.0, tk.END)
            for idx, (question, answer, options) in enumerate(quiz, 1):
                output_box.insert(tk.END, f"Q{idx}: {question}\n")
                for i, option in enumerate(options, 1):
                    output_box.insert(tk.END, f"  {i}. {option}\n")
                output_box.insert(tk.END, f"Answer: {answer}\n\n")
        except Exception as e:
            output_box.delete(1.0, tk.END)
            output_box.insert(tk.END, f"Error: {str(e)}")

    tk.Button(root, text="Back to Main Menu", command=back_to_main_menu).pack(anchor='ne')

    tk.Label(root, text="Select input method:").pack(anchor='w')
    radio_selection = tk.StringVar(value="pdf")
    tk.Radiobutton(root, text="PDF", variable=radio_selection, value="pdf").pack(anchor='w')
    tk.Radiobutton(root, text="DOCX", variable=radio_selection, value="docx").pack(anchor='w')
    tk.Radiobutton(root, text="Manual Text", variable=radio_selection, value="manual").pack(anchor='w')

    tk.Label(root, text="File path:").pack(anchor='w')
    entry_file_path = tk.Entry(root, width=60)
    entry_file_path.pack()
    tk.Button(root, text="Browse", command=select_file).pack()

    tk.Label(root, text="Number of questions:").pack(anchor='w')
    entry_num_questions = tk.Entry(root, width=10)
    entry_num_questions.insert(0, "5")
    entry_num_questions.pack()

    #text_box = scrolledtext.ScrolledText(root, height=5)
    #text_box.pack(pady=10)

    output_box = scrolledtext.ScrolledText(root, height=15)
    output_box.pack(pady=10)

    tk.Button(root, text="Generate Quiz", command=generate_callback).pack(pady=5)
    
# Quiz Assessment Interface
def quiz_assessment_interface():
    clear_window()

    def select_file():
        file_path = filedialog.askopenfilename()
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

    def start_assessment():
        global quiz_data, current_question_index, user_answers, correct_answers
        file_path = entry_file_path.get()
        num_questions = int(entry_num_questions.get())
        if file_path.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            text = extract_text_from_docx(file_path)
        else:
            output_box.insert(tk.END, "Unsupported file format\n")
            return

        quiz_data = generate_quiz(text, num_questions)
        current_question_index = 0
        user_answers = []
        correct_answers = [q[1] for q in quiz_data]
        show_question()

    def show_question():
        clear_window()
        global current_question_index
        if current_question_index < len(quiz_data):
            question, correct, options = quiz_data[current_question_index]
            tk.Label(root, text=f"Question {current_question_index + 1}").pack()
            tk.Label(root, text=question, wraplength=700).pack()
            selected_option = tk.StringVar()
            selected_option.set(None)
            for option in options:
                tk.Radiobutton(root, text=option, variable=selected_option, value=option).pack(anchor='w')
            def submit():
                user_answers.append(selected_option.get())
                global current_question_index
                current_question_index += 1
                show_question()
            tk.Button(root, text="Submit", command=submit).pack(pady=10)
        else:
            show_result()

    def show_result():
        clear_window()
        score = sum(1 for u, c in zip(user_answers, correct_answers) if u == c)
        tk.Label(root, text=f"Assessment Completed!", font=("Arial", 14)).pack(pady=10)
        tk.Label(root, text=f"Score: {score}/{len(correct_answers)}").pack()
        tk.Label(root, text="\nReview:").pack()

        review_box = scrolledtext.ScrolledText(root, height=20)
        review_box.pack()

        for i, (question, correct, options) in enumerate(quiz_data):
            review_box.insert(tk.END, f"Q{i+1}: {question}\n")
            review_box.insert(tk.END, f"Your Answer: {user_answers[i]}\n")
            review_box.insert(tk.END, f"Correct Answer: {correct}\n\n")

        tk.Button(root, text="Back to Main Menu", command=back_to_main_menu).pack(pady=10)

    tk.Button(root, text="Back to Main Menu", command=back_to_main_menu).pack(anchor='ne')
    tk.Label(root, text="Select file for assessment:").pack(anchor='w')
    entry_file_path = tk.Entry(root, width=60)
    entry_file_path.pack()
    tk.Button(root, text="Browse", command=select_file).pack()

    tk.Label(root, text="Number of questions:").pack(anchor='w')
    entry_num_questions = tk.Entry(root, width=10)
    entry_num_questions.insert(0, "5")
    entry_num_questions.pack()

    output_box = scrolledtext.ScrolledText(root, height=10)
    output_box.pack(pady=10)

    tk.Button(root, text="Start Assessment", command=start_assessment).pack(pady=5)

main_menu()
root.mainloop()
