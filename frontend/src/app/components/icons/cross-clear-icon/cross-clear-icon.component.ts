import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-cross-clear-icon',
  templateUrl: './cross-clear-icon.component.svg'
})
export class CrossClearIconComponent {
  @Input() width: number = 10;
  @Input() height: number = 10;
}