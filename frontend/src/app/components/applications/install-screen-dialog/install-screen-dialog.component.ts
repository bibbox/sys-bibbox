import {Component, Inject, OnInit} from '@angular/core';
import {AppInfo, ApplicationItem, IVersions} from '../../../store/models/application-group-item.model';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import {FormControl, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {ApplicationService} from '../../../store/services/application.service';
import {InstanceItem} from '../../../store/models/instance-item.model';
import {UserService} from '../../../store/services/user.service';
import {InstanceService} from '../../../store/services/instance.service';
import {environment} from '../../../../environments/environment';


@Component({
  selector: 'app-install-screen-dialog',
  templateUrl: './install-screen-dialog.component.html',
  styleUrls: ['./install-screen-dialog.component.scss']
})
export class InstallScreenDialogComponent implements OnInit {

  versionFormControl = new FormControl('', Validators.required);
  selectedVersion: IVersions;
  appInfo: AppInfo | null;
  disableInstallButton: boolean;
  maxInstancesTooltip: string = 'Cannot install instance. You have reached the maximum number of instances installable as a demo user.';


  constructor(
    @Inject(MAT_DIALOG_DATA) public applicationItem: ApplicationItem,
    private router: Router,
    private appService: ApplicationService,
    private userService: UserService,
    private instanceService: InstanceService,
  ) {
    this.selectedVersion = this.applicationItem.versions[0];
    this.appInfo = {
      name: '',
      short_name: '',
      version: '',
      description: '',
      short_description: '',
      catalog_url: '',
      application_url: '',
      tags: [],
      application_documentation_url: ''
    };
    this.loadAppInfo().then();
    this.maxInstancesReached();
  }

  ngOnInit(): void {
  }

  async loadAppInfo(): Promise<void> {
    await this.appService.getAppInfo(this.selectedVersion.appinfo)
      .toPromise()
      .then(
        res => this.appInfo = res
      );
  }

  openInstallScreen(): void {
    this.router.navigateByUrl(
      'install/' + this.applicationItem.app_name + '/' + this.selectedVersion.app_version,
      {state: [{...this.applicationItem}, this.selectedVersion]}
    ).then();
  }

  maxInstancesReached(): void {
    const isDemoUser = this.userService.isRole(environment.KEYCLOAK_ROLES.demo_user);

    if (isDemoUser) {
      const userID = this.userService.getUserID();
      this.instanceService.getInstancesPerInstallerID(userID).subscribe(
        (res: InstanceItem[]) => {
          this.disableInstallButton = (res.length >= environment.KEYCLOAK_CONFIG.max_instances_per_demo_user);
        }
      );
    }
  }
}
