import {User} from '../models/user.model';
import {AuthAction, AuthActionTypes} from '../actions/auth.actions';
export interface AuthState {
  user: User;
  isAuthenticated: boolean;
  loading: false;
  error: undefined;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  loading: false,
  error: undefined
};


export function AuthReducer(
  state: AuthState = initialState,
  action: AuthAction
): any {
  switch (action.type) {
    case AuthActionTypes.GET_USER:
      return {...state};
    case AuthActionTypes.USER_LOGIN:
      return {
        ...state,
        loading: true
      };
    case AuthActionTypes.USER_LOGIN_SUCCESS:
      return {
        ...state,
        user: action.payload,
        loading: false,
        isAuthenticated: true,
        error: undefined
      };
    case AuthActionTypes.USER_LOGIN_FAILURE:
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        loading: false,
        error: action.payload
      };
    case AuthActionTypes.USER_LOGOUT:
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        loading: false,
        error: undefined,
      };

    default:
      return {...state};
  }
}
