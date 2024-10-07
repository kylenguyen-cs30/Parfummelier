const ManageUserProfile = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-center mb-8">
          Manage Your Profile
        </h1>

        <form
          //   onSubmit={handleSubmit}
          className="max-w-lg mx-auto bg-white p-6 rounded-lg shadow-md"
        >
          {/* Name */}
          <div className="mb-4">
            <label
              htmlFor="name"
              className="block text-sm font-medium text-gray-700"
            >
              Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              //   value={user.name}
              //   onChange={handleChange}
              className="mt-1 p-2 border border-gray-300 w-full rounded-md"
              required
            />
          </div>

          {/* Email */}
          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              //   value={user.email}
              //   onChange={handleChange}
              className="mt-1 p-2 border border-gray-300 w-full rounded-md"
              required
            />
          </div>

          {/* Password */}
          <div className="mb-4">
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              //   value={user.password}
              //   onChange={handleChange}
              className="mt-1 p-2 border border-gray-300 w-full rounded-md"
              required
            />
          </div>

          {/* Bio (Optional) */}
          <div className="mb-4">
            <label
              htmlFor="bio"
              className="block text-sm font-medium text-gray-700"
            >
              Bio
            </label>
            <textarea
              id="bio"
              name="bio"
              //   value={user.bio}
              //   onChange={handleChange}
              className="mt-1 p-2 border border-gray-300 w-full rounded-md"
              rows={3}
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white p-2 rounded-md hover:bg-blue-500"
          >
            Update Profile
          </button>
        </form>
      </div>
    </div>
  );
};

export default ManageUserProfile;
