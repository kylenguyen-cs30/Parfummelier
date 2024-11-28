import React from "react";
import { Search, ClipboardCheck, Sparkles, Plus } from "lucide-react";

const HowitWorkHero = () => {
  const steps = [
    {
      icon: <Search className="w-12 h-12 text-orange-400" />,
      title: "BROWSE OUR FRAGRANCES",
      description:
        "Explore our extensive collection of unique and captivating scents.",
    },

    {
      icon: <ClipboardCheck className="w-12 h-12 text-orange-400" />,
      title: "TAKE OUR PERSONALIZED QUIZ",
      description:
        "Find your perfect match through through our carefully curated questionaire",
    },
    {
      icon: <Sparkles className="w-12 h-12 text-orange-400" />,
      title: "GET MATCHED",
      description: "Discover fragrances tailored to your prefernces and style.",
    },
    {
      icon: <Plus className="w-12 h-12 text-orange-400" />,
      title: "ADD TO YOUR SCENT BANK",
      description: "Build your personal collection of favorite fragrances.",
    },
  ];

  return (
    <div className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* NOTE: Title of the section */}
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            HERE'S HOW IT WORKS
          </h2>
        </div>

        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((step, index) => (
            <div key={index} className="text-center">
              <div className="flex justify-center mb-4">{step.icon}</div>
              <h3 className="text-lg font-semibold mb-2">{step.title}</h3>
              <p className="text-sm text-gray-600">{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HowitWorkHero;
