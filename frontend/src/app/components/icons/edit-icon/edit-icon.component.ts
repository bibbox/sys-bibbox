import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-edit-icon',
  templateUrl: './edit-icon.component.svg'
})
export class EditIconComponent {
  @Input() width: number = 16;
  @Input() height: number = 16;
}