import React, { forwardRef } from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className = "", error, ...props }, ref) => {
    return (
      <div className="w-full">
        <input
          className={`
            w-full
            rounded-md
            border
            border-gray-300
            bg-white
            px-3
            py-2
            text-sm
            placeholder:text-gray-400
            focus:outline-none
            focus:ring-2
            focus:ring-blue-500
            focus:border-transparent
            disabled:cursor-not-allowed
            disabled:opacity-50
            ${error ? "border-red-500" : ""}
            ${className}
          `}
          ref={ref}
          {...props}
        />
        {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
      </div>
    );
  },
);

Input.displayName = "Input";

export default Input;
