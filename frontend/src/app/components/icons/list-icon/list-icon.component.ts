import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-list-icon',
  templateUrl: './list-icon.component.svg'
})
export class ListIconComponent {
  @Input() width: number = 16;
  @Input() height: number = 16;
}