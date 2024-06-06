import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-restart-icon',
  templateUrl: './restart-icon.component.svg'
})
export class RestartIconComponent {
  @Input() width: number = 16;
  @Input() height: number = 16;
}