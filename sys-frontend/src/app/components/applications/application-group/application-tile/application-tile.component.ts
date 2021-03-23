import {Component, Input, OnInit} from '@angular/core';
import {ApplicationItem} from '../../../../../store/models/application-group-item.model';

@Component({
  selector: 'app-application-tile',
  templateUrl: './application-tile.component.html',
  styleUrls: ['./application-tile.component.scss']
})
export class ApplicationTileComponent implements OnInit {

  constructor() { }

  @Input() application: ApplicationItem;

  ngOnInit(): void {
  }

}
