import {Component, OnDestroy, OnInit} from '@angular/core';
import {SocketioService} from '../../store/services/socketio.service';
import {Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import * as applicationGroupActions from '../../store/actions/applications.actions';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{

  constructor(private socketService: SocketioService,
              private store: Store<AppState>) { }

  ngOnInit(): void {
    this.store.dispatch(new applicationGroupActions.LoadApplicationGroupsAction());
    try {
      this.socketService.setupSocketConnection();
      this.socketService.getInstanceUpdates();
      this.socketService.testSockets();
    }
    catch (e: any) {
      console.log(e);
    }
  }

}
