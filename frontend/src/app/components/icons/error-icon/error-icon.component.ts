import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-error-icon',
  templateUrl: './error-icon.component.svg'
})
export class ErrorIconComponent {
  @Input() width: number = 16;
  @Input() height: number = 16;
}