import { Injectable } from '@angular/core';
import {SOCKET_IO_URL} from '../../commons';
import {io, Socket} from 'socket.io-client';
import {Observable} from 'rxjs';
import {BASEURL} from '../../../app.config';
import {LoadInstancesAction} from '../actions/instance.actions';
import {Store} from '@ngrx/store';
import {AppState} from '../models/app-state.model';
import {timeout} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SocketioService {

  private socket: any;

  constructor(private store: Store<AppState>) {
    this.socket = io(
      // SOCKET_IO_URL,
      'http://localhost:4200',
      {
        transports: ['websocket']
      }
    );
    // this.socket = io();
    this.getInstanceUpdates();
    this.testSockets();
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
      console.log(data);
      this.store.dispatch(new LoadInstancesAction());
    });
  }
  testSockets(): Observable<any> {
    return this.socket.on('event from loop', (data) => {
      console.log('from ws event: ', data);
    });
  }
}
