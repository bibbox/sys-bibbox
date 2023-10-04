import {Component, Input} from '@angular/core';
import {ApplicationGroupItem} from '../../../store/models/application-group-item.model';

@Component({
  selector: 'app-application-group',
  templateUrl: './application-group.component.html',
  styleUrls: ['./application-group.component.scss']
})
export class ApplicationGroupComponent {

  constructor() { }

  @Input() applicationGroup: ApplicationGroupItem;
  @Input() searchByTag: (tag: string) => void;
}
