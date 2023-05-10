import {Action} from '@ngrx/store';
import {
  UserRepresentation,
  UserDictionary,
  UserRoleMapping,
  UserRoles,
  CreateUserSuccessResponse,
  UpdateRoleMappingSuccessResponse, DeleteUserSuccessResponse
} from '../models/user.model';

export enum UserActionTypes {
  LOAD_USERS = '[USER] Load Users',
  LOAD_USERS_SUCCESS = '[USER] Load Users Success',
  LOAD_USERS_FAILURE = '[USER] Load Users Failure',
  UPDATE_USER_ROLE_MAPPINGS = '[USER] Update User Role Mappings',
  UPDATE_USER_ROLE_MAPPINGS_SUCCESS = '[USER] Update User Role Mappings Success',
  UPDATE_USER_ROLE_MAPPINGS_FAILURE = '[USER] Update User Role Mappings Failure',
  DELETE_USER = '[USER] Delete User',
  DELETE_USER_SUCCESS = '[USER] Delete User Success',
  DELETE_USER_FAILURE = '[USER] Delete User Failure',
  CREATE_USER = '[USER] Create User',
  CREATE_USER_SUCCESS = '[USER] Create User Success',
  CREATE_USER_FAILURE = '[USER] Create User Failure',
}

export class LoadUsersAction implements Action {
  readonly type = UserActionTypes.LOAD_USERS;
}

export class LoadUsersSuccessAction implements Action {
  readonly type = UserActionTypes.LOAD_USERS_SUCCESS;
  constructor(public payload: UserRepresentation[]) {}
}

export class LoadUsersFailureAction implements Action {
  readonly type = UserActionTypes.LOAD_USERS_FAILURE;
  constructor(public payload: Error) {}
}

export class UpdateUserRoleMappingsAction implements Action {
  readonly type = UserActionTypes.UPDATE_USER_ROLE_MAPPINGS;
  constructor(public payload: UserRoleMapping) {}
}

export class UpdateUserRoleMappingsSuccessAction implements Action {
  readonly type = UserActionTypes.UPDATE_USER_ROLE_MAPPINGS_SUCCESS;
  constructor(public payload: UpdateRoleMappingSuccessResponse) {}
}

export class UpdateUserRoleMappingsFailureAction implements Action {
  readonly type = UserActionTypes.UPDATE_USER_ROLE_MAPPINGS_FAILURE;
  constructor(public payload: Error) {}
}

export class DeleteUserAction implements Action {
  readonly type = UserActionTypes.DELETE_USER;
  constructor(public userId: string) {}
}

export class DeleteUserSuccessAction implements Action {
  readonly type = UserActionTypes.DELETE_USER_SUCCESS;
  constructor(public payload: DeleteUserSuccessResponse) {}
}

export class DeleteUserFailureAction implements Action {
  readonly type = UserActionTypes.DELETE_USER_FAILURE;
  constructor(public payload: Error) {}
}

export class CreateUserAction implements Action {
  readonly type = UserActionTypes.CREATE_USER;
  constructor(public payload: UserDictionary) {}
}

export class CreateUserSuccessAction implements Action {
  readonly type = UserActionTypes.CREATE_USER_SUCCESS;
  constructor(public payload: CreateUserSuccessResponse) {}  // TODO: fix this
}

export class CreateUserFailureAction implements Action {
  readonly type = UserActionTypes.CREATE_USER_FAILURE;
  constructor(public payload: Error) {}
}


export type UserAction =
  LoadUsersAction |
  LoadUsersSuccessAction |
  LoadUsersFailureAction |
  UpdateUserRoleMappingsAction |
  UpdateUserRoleMappingsSuccessAction |
  UpdateUserRoleMappingsFailureAction |
  DeleteUserAction |
  DeleteUserSuccessAction |
  DeleteUserFailureAction |
  CreateUserAction |
  CreateUserSuccessAction |
  CreateUserFailureAction;
