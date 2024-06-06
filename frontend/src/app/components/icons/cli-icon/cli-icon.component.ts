import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-cli-icon',
  templateUrl: './cli-icon.component.svg'
})
export class CliIconComponent {
  @Input() width: number = 16;
  @Input() height: number = 16;
}