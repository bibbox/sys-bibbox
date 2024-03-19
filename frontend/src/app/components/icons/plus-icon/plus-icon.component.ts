import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-plus-icon',
  templateUrl: './plus-icon.component.svg'
})
export class PlusIconComponent {
  @Input() width: number = 20;
  @Input() height: number = 20;
}