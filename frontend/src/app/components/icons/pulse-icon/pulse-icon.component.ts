import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-pulse-icon',
  templateUrl: './pulse-icon.component.svg'
})
export class PulseIconComponent {
  @Input() width: number = 16;
  @Input() height: number = 16;
}