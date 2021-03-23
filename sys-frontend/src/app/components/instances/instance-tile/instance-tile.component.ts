import {Component, Input, OnInit} from '@angular/core';
import {InstanceItem} from '../../../../store/models/instance-item.model';

@Component({
  selector: 'app-instance-tile',
  templateUrl: './instance-tile.component.html',
  styleUrls: ['./instance-tile.component.scss']
})
export class InstanceTileComponent implements OnInit {

  constructor() { }

  @Input() instance: InstanceItem;

  ngOnInit(): void {
  }
}
