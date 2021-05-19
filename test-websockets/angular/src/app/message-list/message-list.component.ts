import {ChangeDetectorRef, Component, Input, OnInit} from '@angular/core';
import {SocketData} from '../services/socket.service';
import {Subject} from 'rxjs';

@Component({
  selector: 'app-message-list',
  templateUrl: './message-list.component.html',
  styleUrls: ['./message-list.component.scss']
})
export class MessageListComponent implements OnInit {

  @Input() data: Subject<SocketData[]>;
  @Input() title: string;

  constructor(private cd: ChangeDetectorRef) { }

  ngOnInit(): void {
  }

}
