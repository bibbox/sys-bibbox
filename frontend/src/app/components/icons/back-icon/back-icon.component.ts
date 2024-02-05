import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-back-icon',
  templateUrl: './back-icon.component.svg'
})
export class BackIconComponent {
  @Input() width: number = 16;
  @Input() height: number = 16;
}