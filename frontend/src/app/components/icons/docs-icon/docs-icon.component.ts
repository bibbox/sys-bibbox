import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-docs-icon',
  templateUrl: './docs-icon.component.svg'
})
export class DocsIconComponent {
  @Input() width: number = 18;
  @Input() height: number = 18;
}