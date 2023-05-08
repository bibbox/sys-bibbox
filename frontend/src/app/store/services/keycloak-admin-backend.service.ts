import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {API_KEYCLOAK_URL} from '../../commons';

// import user model ts
import {UserRepresentation, UserDictionary, UserRoleMapping, UserRoles, RoleRepresentation} from '../models/user.model';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class KeycloakAdminBackendService {

  constructor(private http: HttpClient) { }

  getUsers(): Observable<UserRepresentation[]> {
    return this.http.get<UserRepresentation[]>(API_KEYCLOAK_URL + 'users');
  }

  createUser(UserDict: UserDictionary): Observable<JSON> {
    const header = new HttpHeaders();
    header.set('Content-Type', 'application/json'); // ; charset=utf-8
    return this.http.post<JSON>(API_KEYCLOAK_URL + 'users', UserDict, {headers: header});
  }

  deleteUser(userID: string): Observable<JSON> {
    return this.http.delete<JSON>(API_KEYCLOAK_URL + 'users/' + userID);
  }

  setRolesForMultipleUsers(userRoleMappings: UserRoleMapping): Observable<JSON> {
    const header = new HttpHeaders();
    header.set('Content-Type', 'application/json'); // ; charset=utf-8
    return this.http.post<JSON>(API_KEYCLOAK_URL + 'roles/update_role_mapping', userRoleMappings, {headers: header});
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
