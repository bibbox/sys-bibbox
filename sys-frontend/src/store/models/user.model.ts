export interface User {
  id?: string;
  username?: string;
  email?: string;
  password_hash?: string;
  token?: string;
  loading?: boolean;
  error?: string;
}
