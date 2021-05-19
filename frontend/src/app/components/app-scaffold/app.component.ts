import {Component, OnDestroy, OnInit} from '@angular/core';
import {SocketioService} from '../../store/services/socketio.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{

  constructor(private socketService: SocketioService) { }

  ngOnInit(): void {
    try {
      this.socketService.setupSocketConnection();
      this.socketService.getInstanceUpdates();
    }
    catch (e: any) {
      console.log(e);
    }
  }

}
