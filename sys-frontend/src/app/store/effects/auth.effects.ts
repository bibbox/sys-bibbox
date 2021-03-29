import {Injectable} from '@angular/core';
import {Actions, createEffect, ofType} from '@ngrx/effects';
import {GetUser, UserLogin, UserLoginSuccess, UserLoginFailure, UserLogout, Authenticated, NotAuthenticated} from '../actions/auth.actions';
import {catchError, map, mergeMap} from 'rxjs/operators';
import {AuthService} from '../services/auth.service';
import {of} from 'rxjs';


@Injectable()
export class InstanceEffects {

  // TODO

  constructor(private actions$: Actions, private authService: AuthService) {
  }
}
