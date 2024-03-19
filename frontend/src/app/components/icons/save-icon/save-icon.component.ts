import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-save-icon',
  templateUrl: './save-icon.component.svg'
})
export class SaveIconComponent {
  @Input() width: number = 22;
  @Input() height: number = 22;
}