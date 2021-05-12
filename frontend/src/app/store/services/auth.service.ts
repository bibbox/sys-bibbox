import { Injectable } from '@angular/core';
import {User} from '../models/user.model';
import {HttpClient} from '@angular/common/http';
import {Store} from '@ngrx/store';
import {Observable} from 'rxjs';
import {API_AUTH_URL} from '../../commons';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  user: User;

  constructor(
    private http: HttpClient,
    private store: Store<{AppState}>) { }

  login(): Observable<User> {
    return this.http.get<User>(API_AUTH_URL + 'token');
    // TODO
  }
}
