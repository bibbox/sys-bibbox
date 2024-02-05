import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-burger-icon',
  templateUrl: './burger-icon.component.svg'
})
export class BurgerIconComponent {
  @Input() width: number = 22;
  @Input() height: number = 22;
}