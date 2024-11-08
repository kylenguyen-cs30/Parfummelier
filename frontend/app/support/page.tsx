import React from "react";

const Support: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Support</h1>

        {/* Support Description */}
        <p className="mb-6">
          Welcome to the Parfummelier Support Page! We are here to assist you
          with any questions or issues you may have regarding our app. Browse
          our frequently asked questions (FAQ), or feel free to reach out to our
          support team for help.
        </p>

        {/* FAQ Section */}
        <div className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">
            Frequently Asked Questions
          </h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold">How do I reset my password?</h3>
              <p>
                If you have forgotten your password, you can reset it by
                clicking on the Forgot Password link on the login page and
                following the instructions.
              </p>
            </div>

            <div>
              <h3 className="font-semibold">
                How can I update my profile information?
              </h3>
              <p>
                Go to the My Account section of the app and click on Edit
                Profile to update your personal information and preferences.
              </p>
            </div>

            <div>
              <h3 className="font-semibold">
                Where can I track my fragrance ratings?
              </h3>
              <p>
                You can find all your fragrance ratings in the Scent Bank
                section of your profile. It stores your ratings and reviews for
                easy reference.
              </p>
            </div>
          </div>
        </div>

        {/* Contact Support Section */}
        <div className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Contact Support</h2>
          <p className="mb-4">
            Still need help? Reach out to our support team and we will get back
            to you as soon as possible.
          </p>
          <form>
            <div className="mb-4">
              <label htmlFor="name" className="block text-sm font-medium">
                Your Name
              </label>
              <input
                type="text"
                id="name"
                name="name"
                className="w-full p-2 rounded-md text-gray-900 border border-gray-300"
                required
              />
            </div>

            <div className="mb-4">
              <label htmlFor="email" className="block text-sm font-medium">
                Your Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                className="w-full p-2 rounded-md text-gray-900 border border-gray-300"
                required
              />
            </div>

            <div className="mb-4">
              <label htmlFor="message" className="block text-sm font-medium">
                Your Message
              </label>
              <textarea
                id="message"
                name="message"
                rows={5}
                className="w-full p-2 rounded-md text-gray-900 border border-gray-300"
                required
              />
            </div>

            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-500"
            >
              Send Message
            </button>
          </form>
        </div>

        {/* Additional Resources */}
        <div className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Additional Resources</h2>
          <ul className="list-disc ml-6 space-y-2">
            <li>
              <a href="#" className="text-blue-400 hover:underline">
                User Guide
              </a>
            </li>
            <li>
              <a href="#" className="text-blue-400 hover:underline">
                Troubleshooting Tips
              </a>
            </li>
            <li>
              <a href="#" className="text-blue-400 hover:underline">
                Community Forum
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Support;
