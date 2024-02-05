import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-arrow-up-icon',
  templateUrl: './arrow-up-icon.component.svg'
})
export class ArrowUpIconComponent {
  @Input() width: number = 10;
  @Input() height: number = 10;
}