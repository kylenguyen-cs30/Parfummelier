import { useRouter } from "next/navigation"; // Use Next.js router for redirection
import axios from "axios";

export default function LogoutButton() {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      // Send POST request to Flask backend to logout
      await axios.post(
        "http://localhost:5000/logout",
        {},
        { withCredentials: true }
      );

      // Redirect to login page after successful logout
      router.push("/login"); // or any route
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return <button onClick={handleLogout}>Logout</button>;
}
