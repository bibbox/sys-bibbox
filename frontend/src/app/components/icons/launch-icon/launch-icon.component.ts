import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-launch-icon',
  templateUrl: './launch-icon.component.svg'
})
export class LaunchIconComponent {
  @Input() width: number = 16;
  @Input() height: number = 16;
}