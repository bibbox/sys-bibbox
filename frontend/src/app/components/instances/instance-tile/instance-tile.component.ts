import { Component, Injectable, Input, OnInit } from '@angular/core';
import { InstanceItem } from '../../../store/models/instance-item.model';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-instance-tile',
  templateUrl: './instance-tile.component.html',
  styleUrls: ['./instance-tile.component.scss']
})

@Injectable({
  providedIn: 'root'
})
export class InstanceTileComponent implements OnInit {

  constructor() { }

  @Input() instance: InstanceItem;
  instanceUrl: string;

  ngOnInit(): void {
    this.getInstanceUrl();
  }

  getInstanceUrl(): void {
    if (this.instance.proxy !== undefined) {
      for (const proxy of this.instance.proxy) {
        if (proxy.TYPE === 'PRIMARY') {
          this.instanceUrl = 'http://' + this.instance.instancename + '.' + environment.BASEURL;
        }
      }
    }
  }

}
