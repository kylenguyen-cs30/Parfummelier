"use client";
import React from "react";
import Link from "next/link";

interface QuizPromptSectionProps {
  isNewUser: boolean;
}

const QuizPromptSection: React.FC<QuizPromptSectionProps> = ({ isNewUser }) => {
  return (
    <section className="bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-3xl mx-auto text-center">
          {isNewUser ? (
            <div className="bg-white p-8 rounded-lg shadow-md">
              <h2 className="text-2xl font-semibold mb-4">First time here?</h2>
              <p className="text-gray-600 mb-6">
                Please take our quiz to find out your ScentBank
              </p>
              <Link
                href="/quiz"
                className="inline-block bg-blue-500 text-white px-6 py-3 rounded-md hover:bg-blue-600 transition-colors"
              >
                Take the Quiz
              </Link>
            </div>
          ) : (
            <div className="bg-white p-8 rounded-lg shadow-md">
              <h2 className="text-2xl font-semibold mb-4">
                Want to update your preferences?
              </h2>
              <p className="text-gray-600 mb-6">
                Retake the quiz to refine your ScentBank
              </p>
              <Link
                href="/quiz"
                className="inline-block bg-blue-500 text-white px-6 py-3 rounded-md hover:bg-blue-600 transition-colors"
              >
                Retake Quiz
              </Link>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default QuizPromptSection;
