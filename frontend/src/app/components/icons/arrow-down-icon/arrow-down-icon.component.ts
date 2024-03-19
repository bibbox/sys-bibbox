import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-arrow-down-icon',
  templateUrl: './arrow-down-icon.component.svg'
})
export class ArrowDownIconComponent {
  @Input() width: number = 10;
  @Input() height: number = 10;
}