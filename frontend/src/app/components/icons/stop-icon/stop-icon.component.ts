import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-stop-icon',
  templateUrl: './stop-icon.component.svg'
})
export class StopIconComponent {
  @Input() width: number = 16;
  @Input() height: number = 16;
}