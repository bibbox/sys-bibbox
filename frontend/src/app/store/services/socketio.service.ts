import { Injectable } from '@angular/core';
import {SOCKET_IO_URL} from '../../commons';
import {io} from 'socket.io-client';
import {Observable} from 'rxjs';
import {BASEURL} from '../../../app.config';
import {LoadInstancesAction} from '../actions/instance.actions';
import {Store} from '@ngrx/store';
import {AppState} from '../models/app-state.model';

@Injectable({
  providedIn: 'root'
})
export class SocketioService {

  private socket;

  constructor(private store: Store<AppState>) {}

  setupSocketConnection(): void {
    this.socket = io(SOCKET_IO_URL, {
      // transports: ['websocket']
    });
  }

  getInstanceUpdates(): Observable<string> {
    return this.socket.on('new instance data', (data) => {
      console.log('new instance data');
      this.store.dispatch(new LoadInstancesAction());
    });
  }
}
