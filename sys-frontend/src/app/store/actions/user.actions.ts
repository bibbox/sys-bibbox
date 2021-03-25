import {Action} from '@ngrx/store';
import {User} from '../models/user.model';

export const GET_USER = '[AUTH] Get User';
export const AUTHENTICATED = '[AUTH] Authenticated';
export const NOT_AUTHENTICATED = '[AUTH] Not Authenticated';
export const USER_LOGIN = '[AUTH] User Login';
export const USER_LOGIN_SUCCESS = '[AUTH] User Login Success';
export const USER_LOGIN_FAILURE = '[AUTH] User Login Failure';
export const USER_LOGOUT = '[AUTH] User Logout';

// TODO: Strong type payload for each action

export class GetUser implements Action {
  readonly type = GET_USER;
  constructor(public payload?: any) {}
}

export class Authenticated implements Action {
  readonly type = AUTHENTICATED;
  constructor(public payload?: any) {}
}

export class NotAuthenticated implements Action {
  readonly type = NOT_AUTHENTICATED;
  constructor(public payload?: any) {}
}

export class UserLogin implements Action {
  readonly type = USER_LOGIN;
  constructor(public payload?: any) {}
}

export class UserLoginSuccess implements Action {
  readonly type = USER_LOGIN_SUCCESS;
  constructor(public payload?: any) {}
}

export class UserLoginFailure implements Action {
  readonly type = USER_LOGIN_FAILURE;
  constructor(public payload?: any) {}
}

export class UserLogout implements Action {
  readonly type = USER_LOGOUT;
  constructor(public payload?: any) {}
}

export type UserActions =
  GetUser
  | Authenticated
  | NotAuthenticated
  | UserLogin
  | UserLoginSuccess
  | UserLoginFailure
  | UserLogout;
