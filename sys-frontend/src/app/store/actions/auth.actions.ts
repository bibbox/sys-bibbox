import {Action} from '@ngrx/store';
import {User} from '../models/user.model';


export enum AuthActionTypes {
  GET_USER            = '[AUTH] Get User',
  AUTHENTICATED       = '[AUTH] Authenticated',
  NOT_AUTHENTICATED   = '[AUTH] Not Authenticated',
  USER_LOGIN          = '[AUTH] User Login',
  USER_LOGIN_SUCCESS  = '[AUTH] User Login Success',
  USER_LOGIN_FAILURE  = '[AUTH] User Login Failure',
  USER_LOGOUT         = '[AUTH] User Logout',
}


// TODO: Strong type payload for each action

export class GetUser implements Action {
  readonly type = AuthActionTypes.GET_USER;
  constructor(public payload?: any) {}
}

export class Authenticated implements Action {
  readonly type = AuthActionTypes.AUTHENTICATED;
  constructor(public payload?: any) {}
}

export class NotAuthenticated implements Action {
  readonly type = AuthActionTypes.NOT_AUTHENTICATED;
  constructor(public payload?: any) {}
}

export class UserLogin implements Action {
  readonly type = AuthActionTypes.USER_LOGIN;
  constructor(public payload?: any) {}
}

export class UserLoginSuccess implements Action {
  readonly type = AuthActionTypes.USER_LOGIN_SUCCESS;
  constructor(public payload?: any) {}
}

export class UserLoginFailure implements Action {
  readonly type = AuthActionTypes.USER_LOGIN_FAILURE;
  constructor(public payload: Error) {}
}

export class UserLogout implements Action {
  readonly type = AuthActionTypes.USER_LOGOUT;
  constructor(public payload?: any) {}
}

export type AuthAction =
  GetUser
  | Authenticated
  | NotAuthenticated
  | UserLogin
  | UserLoginSuccess
  | UserLoginFailure
  | UserLogout;
