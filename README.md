# Automatic Quiz Generator with Assessment Feature

## Overview

This project is a desktop application developed in Python that automatically generates fill-in-the-blank quizzes from various text sources. It leverages Natural Language Processing (NLP) to intelligently identify key terms and create context-based questions, providing a valuable tool for both educators and students.

## Features

-   **Multi-Source Input:** Generates quizzes from PDF files, DOCX documents, or manually pasted text.
-   **Intelligent Question Generation:** Utilizes the NLTK library to perform Part-of-Speech (POS) tagging, automatically identifying key nouns and verbs to blank out.
-   **Dual-Mode GUI:**
    -   **Generation Mode:** Allows an educator to load a document, specify the number of questions, and instantly generate a quiz with the correct answers displayed.
    -   **Assessment Mode:** Allows a student to take the generated quiz, select answers from multiple-choice options, and receive an immediate score and a question-by-question review upon completion.
-   **User-Friendly Interface:** Built with Tkinter for a clean and intuitive graphical user interface.

## Technologies Used

-   **Language:** Python
-   **GUI:** Tkinter
-   **NLP:** NLTK
-   **File Handling:** pdfplumber, python-docx

## How to Run

1.  Clone the repository:
    ```bash
    git clone https://github.com/harshitpatel0000/Automatic_Quiz_Generator_with_assessment_feature.git
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python main.py
    ```
