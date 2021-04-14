import {Component, Input, OnInit} from '@angular/core';
import {InstanceItem} from '../../../store/models/instance-item.model';
import {LOCAL_TLD} from '../../../commons';

@Component({
  selector: 'app-instance-tile',
  templateUrl: './instance-tile.component.html',
  styleUrls: ['./instance-tile.component.scss']
})
export class InstanceTileComponent implements OnInit {

  constructor() { }

  @Input() instance: InstanceItem;
  instanceUrl: string;

  ngOnInit(): void {
    this.getInstanceUrl();
  }

  getInstanceUrl(): void {
    for (const proxy of this.instance.proxy) {
      if (proxy.TYPE === 'PRIMARY') {
        this.instanceUrl = 'http://' + proxy.CONTAINER.replace(/:[0-9]+/, '') + LOCAL_TLD;
      }
    }
  }
}
