import {Component, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {FormControl} from '@angular/forms';
import {SocketData, SocketService} from './services/socket.service';
import {Subject} from 'rxjs';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'socket demo';

  client = new FormControl('', []);
  broadcast = new FormControl('', []);

  clientMessages: Subject<SocketData[]>;
  broadcastMessages: Subject<SocketData[]>;


  constructor(private socketService: SocketService) {
  }

  ngOnInit(): void {
    this.socketService.setupSocketConnection();
    this.socketService.getMessage();
    this.socketService.getBroadcastMessage();
  }

  sendMessage(): void {
    console.log('pressed send. message: ' + this.client.value.toString());
    this.socketService.sendMessage(this.client.value);
  }

  sendBroadcastMessage(): void {
    console.log('pressed send broadcast message: ' + this.broadcast.value.toString());
    this.socketService.sendBroadcastMessage(this.broadcast.value);
  }
}
