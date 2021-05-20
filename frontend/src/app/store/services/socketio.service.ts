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

  constructor(private store: Store<AppState>) {
    this.socket = io(
      // SOCKET_IO_URL,
      'http://localhost:4200',
      {
        transports: ['websocket']
      }
    );
  }

  setupSocketConnection(): void {
    this.socket = io(
      // SOCKET_IO_URL,
      'http://localhost:4200',
      {
        transports: ['websocket']
      }
      );
  }

  getInstanceUpdates(): Observable<any> {
    return this.socket.on('new_instance_data', (data) => {
      console.log('new_instance_data', data);
      this.store.dispatch(new LoadInstancesAction());
    });
  }
  testSockets(): Observable<any> {
    return this.socket.on('connected', (data) => {
      console.log('from ws event: ', data);
    });
  }
}
