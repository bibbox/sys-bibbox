import { Injectable } from '@angular/core';
import {User} from '../models/user.model';
import {HttpClient, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Store} from '@ngrx/store';
import {Observable} from 'rxjs';
import {API_AUTH_URL} from '../../commons';

@Injectable({
  providedIn: 'root'
})
export class AuthService implements HttpInterceptor {

  user: User;

  constructor(
    private http: HttpClient,
    private store: Store<{AppState}>) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    request = request.clone({
      setHeaders: {
        Authorization: 'X-API-KEY value'
      }
    });
    return next.handle(request);
  }


  login(): Observable<User> {
    return this.http.get<User>(API_AUTH_URL + 'token');
    // TODO
  }



  tokenSetter(): void {
    localStorage.setItem('access_token', 'value');
  }

  tokenGetter(): string {
    return localStorage.getItem('access_token');
  }
}
