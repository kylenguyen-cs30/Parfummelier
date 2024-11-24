export interface User {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  userName: string;
}

export interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}
