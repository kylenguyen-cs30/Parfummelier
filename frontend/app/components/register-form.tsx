"use client";

export const RegisterForm = ({ children }: { children: React.ReactNode }) => {
  return (
    <form /*onSubmit={handleSubmit}*/>
      <div>
        <label htmlFor="username">Username</label>
        <input
          type="text"
          id="username"
          name="username"
          //value={formData.username}
          //onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          name="email"
          //value={formData.email}
          //onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          name="password"
          //value={formData.password}
          //onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input
          type="password"
          id="confirmPassword"
          name="confirmPassword"
          //value={formData.confirmPassword}
          //onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Register</button>
      {children} {/* Render any child components passed to RegisterForm */}
    </form>
  );
};
