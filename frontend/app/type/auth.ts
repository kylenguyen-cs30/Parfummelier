export interface User {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  userName: string;
  favorite_accords: string[];
  favorite_products: string[];
}

export interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}
