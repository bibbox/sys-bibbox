import {Component, Input} from '@angular/core';
import {InstanceGroupItem} from '../../../store/models/instance-item.model';

@Component({
  selector: 'app-instance-group',
  templateUrl: './instance-group.component.html',
  styleUrls: ['./instance-group.component.scss']
})
export class InstanceGroupComponent {

  constructor() { }

  @Input() group: InstanceGroupItem;
}
