/*
    The QuizModal component is a React modal used to display a quiz or survey to users.
    Log to console an array/list of answers in variable updatedAnswers
*/
"use client";
import React, { useState } from "react";
import ReactDOM from "react-dom";
import "../components/quiz-modal.css"; // Import vanilla CSS

interface QuizModalProps {
  isOpen: boolean; //Controls whether the modal is open or closed. When true, the modal is visible; when false, it is hidden.

  onClose: () => void; //A function to close the modal. This is called when the quiz is completed or if the user needs to exit the modal.

  questions: { question: string; options: string[] }[];
}

const QuizModal: React.FC<QuizModalProps> = ({
  isOpen,
  onClose,
  questions,
}) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<(string | null)[]>(
    Array(questions.length).fill(null)
  ); // Store strings
  const [selectedOption, setSelectedOption] = useState<string | null>(null); // Store string value

  const currentQuestion = questions[currentQuestionIndex];

  // Store the selected option (string value)
  const handleOptionClick = (optionValue: string) => {
    setSelectedOption(optionValue);
  };

  const handleNextQuestion = () => {
    if (selectedOption !== null) {
      const updatedAnswers = [...answers];
      updatedAnswers[currentQuestionIndex] = selectedOption; // Store the string value
      setAnswers(updatedAnswers);

      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
      } else {
        // Quiz completed
        setCurrentQuestionIndex(0); // Reset to the first question
        console.log("Survey answers:", updatedAnswers); // Log the string answers
        onClose(); // Close the modal when the survey is completed
      }
      setSelectedOption(null); // Reset selection for the next question
    }
  };

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="modal-overlay">
      <div className="modal-container">
        <h2 className="modal-header">Quiz {currentQuestionIndex + 1}</h2>
        <p className="modal-question">{currentQuestion.question}</p>

        <div className="options-container">
          {currentQuestion.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleOptionClick(option)}
              className={`option-button ${
                selectedOption === option ? "selected" : ""
              }`}
            >
              {option}
            </button>
          ))}
        </div>

        <div className="text-right">
          <button
            onClick={handleNextQuestion}
            disabled={selectedOption === null}
            className="next-button"
          >
            {currentQuestionIndex < questions.length - 1
              ? "Next Question"
              : "Submit Survey"}
          </button>
        </div>
      </div>
    </div>,
    document.getElementById("portal")!
  );
};

export default QuizModal;
