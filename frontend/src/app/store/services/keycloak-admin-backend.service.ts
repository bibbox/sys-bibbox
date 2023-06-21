import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {API_KEYCLOAK_URL} from '../../commons';

// import user model ts
import {
  UserRepresentation,
  UserDictionary,
  UserRoleMapping,
  UserRoles,
  RoleRepresentation,
  UpdateRoleMappingSuccessResponse, CreateUserSuccessResponse, DeleteUserSuccessResponse
} from '../models/user.model';
import {Observable} from 'rxjs';

import {Store} from '@ngrx/store';
import {AppState} from '../models/app-state.model';
import {LoadUsersAction} from '../actions/user.actions';

@Injectable({
  providedIn: 'root'
})
export class KeycloakAdminBackendService {

  constructor(
    private http: HttpClient,
    private store: Store<AppState>) { }

  getUsers(): Observable<UserRepresentation[]> {
    return this.http.get<UserRepresentation[]>(API_KEYCLOAK_URL + 'users');
  }

  createUser(UserDict: UserDictionary): Observable<CreateUserSuccessResponse> {
    const header = new HttpHeaders();
    header.set('Content-Type', 'application/json'); // ; charset=utf-8
    return this.http.post<CreateUserSuccessResponse>(API_KEYCLOAK_URL + 'users', UserDict, {headers: header});
  }

  deleteUser(userID: string): Observable<DeleteUserSuccessResponse> {
    return this.http.delete<DeleteUserSuccessResponse>(API_KEYCLOAK_URL + 'users/' + userID);
  }

  setRolesForMultipleUsers(userRoleMappings: UserRoleMapping): Observable<UpdateRoleMappingSuccessResponse> {
    const header = new HttpHeaders();
    header.set('Content-Type', 'application/json'); // ; charset=utf-8
    return this.http.post<UpdateRoleMappingSuccessResponse>(API_KEYCLOAK_URL + 'roles/update_role_mapping', userRoleMappings, {headers: header});
  }

  refreshStoreUsers(): void {
    this.store.dispatch(new LoadUsersAction());
  }

  getUserNames(): Observable<string[]> {
    return this.http.get<string[]>(API_KEYCLOAK_URL + 'users/names');
  }

  checkIfUsernameExists(username: string): Observable<boolean> {
    return this.http.get<boolean>(API_KEYCLOAK_URL + 'users/names/' + username);
  }


  // getUser(userID: string): Observable<UserRepresentation> {
  //   return this.http.get<UserRepresentation>(API_KEYCLOAK_URL + 'users/' + userID);
  // }

  // updateUser(userID: string, UserDict: UserDictionary): Observable<Object> {
  //   const header = new HttpHeaders();
  //   header.set('Content-Type', 'application/json'); // ; charset=utf-8
  //   return this.http.put(API_KEYCLOAK_URL + 'users/' + userID, UserDict, {headers: header});
  // }



  // addUserRoles(userID: string, roles: string[]): Observable<string[]> {
  //   return this.http.post<string[]>(API_KEYCLOAK_URL + 'users/' + userID + '/roles', roles);
  // }



  // getRoles(): Observable<RoleRepresentation[]> {
  //   return this.http.get<RoleRepresentation[]>(API_KEYCLOAK_URL + 'roles');
  // }
}
