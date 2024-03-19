import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-guide-icon',
  templateUrl: './guide-icon.component.svg'
})
export class GuideIconComponent {
  @Input() width: number = 20;
  @Input() height: number = 20;
}