/*
    The QuizModal component is a React modal used to display a quiz or survey to users.
    Log to console an array/list of answers in variable updatedAnswers
*/
"use client";
import React, { useState } from "react";
import ReactDOM from "react-dom";

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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-lg w-full">
        <h2 className="text-2xl font-bold mb-4">
          Question {currentQuestionIndex + 1}
        </h2>
        <p className="font-bold mb-4">{currentQuestion.question}</p>

        <div className="space-y-4">
          {currentQuestion.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleOptionClick(option)} // Pass the string value of the option
              className={`block w-full text-left p-2 rounded-md ${
                selectedOption === option
                  ? "bg-blue-200"
                  : "bg-gray-100 hover:bg-gray-200"
              }`}
            >
              {option}
            </button>
          ))}
        </div>

        <div className="mt-6 text-right">
          <button
            onClick={handleNextQuestion}
            disabled={selectedOption === null}
            className={`${
              selectedOption === null
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-500"
            } text-white py-2 px-4 rounded-md`}
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
