import {Injectable} from '@angular/core';
import {SOCKET_IO_URL} from '../../commons';
import {io, Socket} from 'socket.io-client';
import {DeleteInstanceSuccessAction} from '../actions/instance.actions';
import {Store} from '@ngrx/store';
import {AppState} from '../models/app-state.model';
import {InstanceService} from './instance.service';
import {ActivityService} from './activity.service';
import {KeyValueService} from './keyvalue.service';
import {KeycloakAdminBackendService} from './keycloak-admin-backend.service';
import {KeycloakService} from 'keycloak-angular';
import {DeleteUserSuccessAction} from '../actions/user.actions';

@Injectable({
  providedIn: 'root'
})
export class SocketioService {

  private socket: Socket;
  constructor(
    private instanceService: InstanceService,
    private activityService: ActivityService,
    private kcAdminService: KeycloakAdminBackendService,
    private store: Store<AppState>
  ) {
    this.connect();
    this.checkConnected();
  }

  connect(): void {
    this.socket = io(
      SOCKET_IO_URL,
      {
      // reconnectionDelayMax: 10000,
      transports: ['polling', 'websocket'] // , 'websocket'] // currently only polling works
      }
      );
    // console.log('socket connected: ', this.socket.connected);
  }

  addInstanceUpdatesListener(): void {
    this.socket.on('new_instance_data', () => {
      // console.log('new instance data');
      this.instanceService.refreshStoreInstances();
    });
    this.socket.on('instance_deleted', (response) => {
      // console.log('deleted instance ' + response.id);
      this.store.dispatch(new DeleteInstanceSuccessAction(response.id));
    });
  }

  addActivityUpdatesListener(): void {
    this.socket.on('new_activity_status', () => {
      // console.log('new_activity_status');
      this.activityService.refreshStoreActivities();
    });
  }

  addUserUpdatesListener(): void {
    console.log('adding user updates listener');
    this.socket.on('new_user_data', () => {
      this.kcAdminService.refreshStoreUsers();
    });

    this.socket.on('user_deleted', (response) => {
      // this.store.dispatch(new DeleteUserSuccessAction(response.id));
    });
  }

  checkConnected(): void {
    this.socket.on('connected', (data) => {
      console.log('new ws connection: ', data.data);
      // console.log(this.socket.id);
    });
  }
}
