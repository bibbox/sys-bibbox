import {Injectable} from '@angular/core';
import {Actions, createEffect, ofType} from '@ngrx/effects';
import {
  UserActionTypes,
  LoadUsersAction, LoadUsersSuccessAction, LoadUsersFailureAction,
  CreateUserAction, CreateUserSuccessAction, CreateUserFailureAction,
  DeleteUserAction, DeleteUserSuccessAction, DeleteUserFailureAction,
  UpdateUserRoleMappingsAction, UpdateUserRoleMappingsSuccessAction, UpdateUserRoleMappingsFailureAction
} from '../actions/user.actions';
import {catchError, map, mergeMap} from 'rxjs/operators';
import {KeycloakAdminBackendService} from '../services/keycloak-admin-backend.service';
import {of} from 'rxjs';

@Injectable()
export class UserEffects {

  loadUsers$ =  createEffect(() =>
    this.actions$.pipe(
      ofType<LoadUsersAction>(UserActionTypes.LOAD_USERS),
      mergeMap(
        () => this.kcService.getUsers()
          .pipe(
            map(users => new LoadUsersSuccessAction(users)),
            catchError(error => of(new LoadUsersFailureAction(error)))
          )
      )
    )
  );

  createUser$ = createEffect(() =>
    this.actions$.pipe(
      ofType<CreateUserAction>(UserActionTypes.CREATE_USER),
      mergeMap(
        (action) => this.kcService.createUser(action.payload)
          .pipe(
            map(info => new CreateUserSuccessAction(info)),
            catchError(error => of(new CreateUserFailureAction(error)))
          )
      )
    )
  );

  deleteUser$ = createEffect(() =>
    this.actions$.pipe(
      ofType<DeleteUserAction>(UserActionTypes.DELETE_USER),
      mergeMap(
        (action) => this.kcService.deleteUser(action.userId)
          .pipe(
            map(info => new DeleteUserSuccessAction(info)),
            catchError(error => of(new DeleteUserFailureAction(error)))
          )
      )
    )
  );

  updateUserRoleMappings$ = createEffect(() =>
    this.actions$.pipe(
      ofType<UpdateUserRoleMappingsAction>(UserActionTypes.UPDATE_USER_ROLE_MAPPINGS),
      mergeMap(
        (action) => this.kcService.setRolesForMultipleUsers(action.payload)
          .pipe(
            // map(json => new UpdateUserRoleMappingsSuccessAction(json)), // something is buggy here, so we just reload the users
            map(json => new LoadUsersAction()),
            catchError(error => of(new UpdateUserRoleMappingsFailureAction(error)))
          )
      )
    )
  );

  constructor(private actions$: Actions, private kcService: KeycloakAdminBackendService) {

  }
}
