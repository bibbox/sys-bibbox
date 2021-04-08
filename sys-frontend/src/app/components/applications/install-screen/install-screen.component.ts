import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ApplicationItem, EnvironmentParameters, IVersions} from '../../../store/models/application-group-item.model';
import {ApplicationService} from '../../../store/services/application.service';

@Component({
  selector: 'app-install-screen',
  templateUrl: './install-screen.component.html',
  styleUrls: ['./install-screen.component.scss']
})
export class InstallScreenComponent implements OnInit {

  constructor(private activatedRoute: ActivatedRoute,
              private router: Router,
              private appService: ApplicationService) {

    // TODO: Find better Workaround
    if (!(history.state[0])){
      this.router.navigateByUrl('/applications');
    }
  }

  appItem: ApplicationItem;
  selectedVersion: IVersions;
  environmentParameters: EnvironmentParameters[];

  ngOnInit(): void {
    console.log(history.state);
    this.appItem = history.state[0];
    this.selectedVersion = history.state[1];
    this.loadEnvParams();

  }

  async loadEnvParams(): Promise<void> {
    console.warn(this.selectedVersion.environment_parameters);
    await this.appService.getAppEnvParams(this.selectedVersion.environment_parameters).toPromise().then(
      res => this.environmentParameters = res
    );
    console.warn(this.environmentParameters);
  }

  cancel(): void {
    this.router.navigateByUrl('/applications');
  }

  install(): void {

  }
}
