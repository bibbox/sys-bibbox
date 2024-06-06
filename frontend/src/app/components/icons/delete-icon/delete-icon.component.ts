import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-delete-icon',
  templateUrl: './delete-icon.component.svg'
})
export class DeleteIconComponent {
  @Input() width: number = 16;
  @Input() height: number = 16;
}