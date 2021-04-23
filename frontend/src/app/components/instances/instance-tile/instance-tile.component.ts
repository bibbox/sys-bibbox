import {Component, Input, OnInit} from '@angular/core';
import {InstanceItem} from '../../../store/models/instance-item.model';
import {BASEURL} from '../../../../app.config';

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
        this.instanceUrl = 'http://' + this.instance.instancename + '.' + BASEURL;
      }
    }
  }
}
