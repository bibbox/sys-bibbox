import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-github-icon',
  templateUrl: './github-icon.component.svg'
})
export class GithubIconComponent {
  @Input() width: number = 18;
  @Input() height: number = 18;
}