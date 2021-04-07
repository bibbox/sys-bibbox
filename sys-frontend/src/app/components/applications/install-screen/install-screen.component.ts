import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ApplicationItem} from '../../../store/models/application-group-item.model';

@Component({
  selector: 'app-install-screen',
  templateUrl: './install-screen.component.html',
  styleUrls: ['./install-screen.component.scss']
})
export class InstallScreenComponent implements OnInit {

  constructor(private activatedRoute: ActivatedRoute,
              private router: Router) {
  }
  application: ApplicationItem;

  ngOnInit(): void {
    this.application = history.state;
  }


  cancel(): void {
    this.router.navigateByUrl('/applications');
  }

  install(): void {

  }
}
