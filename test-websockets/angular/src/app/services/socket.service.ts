import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import {io, Socket} from 'socket.io-client';
import {environment} from '../../environments/environment';

export interface SocketData {
  message: string;
  type: string;
  counter: number;
}


@Injectable({
  providedIn: 'root'
})
export class SocketService {

  private socket;

  clientMessages: SocketData[] = [];
  broadcastMessages: SocketData[] = [];

  constructor() {}

  setupSocketConnection(): void {
    this.socket = io(environment.SOCKET_ENDPOINT);
  }

  sendMessage(msg: string): void {
    this.socket.emit('custom event', msg);
  }

  sendBroadcastMessage(msg: string): void {
    this.socket.emit('custom broadcast event', msg);
  }

  getMessage(): Observable<SocketData> {
    return this.socket.on('response', (data) => {
      console.log('Server response: ', data);
      this.clientMessages.push(data);
    });
  }

  getBroadcastMessage(): Observable<SocketData> {
    return this.socket.on('response broadcast', (data) => {
      console.log('Server broadcast response:', data);
      this.broadcastMessages.push(data);
    });
  }
}
