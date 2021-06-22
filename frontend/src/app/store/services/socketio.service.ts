import {Injectable} from '@angular/core';
import {SOCKET_IO_URL} from '../../commons';
import {io, Socket} from 'socket.io-client';
import {Observable} from 'rxjs';
import {BASEURL} from '../../../app.config';
import {
  DeleteAllInstancesAction,
  DeleteInstanceAction,
  DeleteInstanceSuccessAction,
  LoadInstancesAction
} from '../actions/instance.actions';
import {Store} from '@ngrx/store';
import {AppState} from '../models/app-state.model';
import {timeout} from 'rxjs/operators';
import {InstanceService} from './instance.service';

@Injectable({
  providedIn: 'root'
})
export class SocketioService {

  private socket: Socket;
  constructor(private iservice: InstanceService, private store: Store<AppState>) {
    this.connect();
    // this.checkConnected();
    this.addInstanceUpdatesListener();
  }

  connect(): void {
    this.socket = io(
      SOCKET_IO_URL,
      // 'http://localhost:4200/socket.io',
      {
      //  reconnectionDelayMax: 10000,
      //   transports: ['websocket']
      }
      );
  }

  addInstanceUpdatesListener(): void {
    this.socket.on('new_instance_data', (data) => {
      console.log('new instance data');
      this.iservice.refreshStoreInstances();
    });
    this.socket.on('instance_deleted', (response) => {
      console.log('deleted instance ' + response.id);
      this.store.dispatch(new DeleteInstanceSuccessAction(response.id));
    });
  }

  checkConnected(): void {
    this.socket.on('connected', (data) => {
      console.log('new ws connection: ', data.data);
      console.log(this.socket.id);
    });
  }
}
