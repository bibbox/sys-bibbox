import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-install-icon',
  templateUrl: './install-icon.component.svg'
})
export class InstallIconComponent {
  @Input() width: number;
  @Input() height: number;
}