import {Component, Inject, OnInit} from '@angular/core';
import {AppInfo, AppInstallDialogProps, ApplicationItem, IVersions} from '../../../store/models/application-group-item.model';
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

  applicationItem: ApplicationItem;
  searchByTag: (tag: string) => void;
  versionFormControl = new FormControl(null, Validators.required);
  appInfo: AppInfo | null;
  disableInstallButton: boolean = true;
  maxInstancesTooltip: string = 'Cannot install instance. You have reached the maximum number of instances installable as a demo user. ('+ environment.KEYCLOAK_CONFIG.max_instances_per_demo_user +')';

  constructor(
    @Inject(MAT_DIALOG_DATA) public props: AppInstallDialogProps,
    private router: Router,
    private appService: ApplicationService,
    private userService: UserService,
    private instanceService: InstanceService,
  ) {
    this.applicationItem = props.application;
    this.searchByTag = props.searchByTag;

    this.appInfo = {
      name: '',
      short_name: '',
      version: '',
      description: '',
      short_description: '',
      catalog_url: '',
      application_url: '',
      tags: [],
      application_documentation_url: '',
      icon_url: this.applicationItem.icon_url,
      versionOptions: structuredClone(this.applicationItem.versions).map(item => ({ ...item, selectLabel: item.app_version })),
      install_guide_url: '',
      instance_information: ''
    };
  }

  async ngOnInit(): Promise<void> {
    await this.loadAppInfo().then(() => {
      this.appInfo.versionOptions[0].app_version = this.appInfo.version;
      this.appInfo.versionOptions[0].selectLabel = `${this.appInfo.version} (latest)`;
      this.versionFormControl.setValue(this.appInfo.versionOptions[0]);
    });

    this.maxInstancesReached();
  }

  async loadAppInfo(): Promise<void> {
    await this.appService.getAppInfo((this.versionFormControl.value || this.applicationItem.versions[0])?.appinfo)
      .toPromise()
      .then(res => this.appInfo = {
        ...this.appInfo,
        ...res,
        install_guide_url: this.getInstallGuideUrl(this.applicationItem.app_name, res.version),
        instance_information: res.instance_information || ''
      });
  }

  openInstallScreen(): void {
    this.router.navigateByUrl(
      'install/' + this.applicationItem.app_name + '/' + this.versionFormControl.value.app_version,
      {state: [
        {...this.applicationItem},
        this.versionFormControl.value,
        this.appInfo.install_guide_url,
        this.appInfo.application_documentation_url,
        this.appInfo.instance_information
      ]}
    ).then();
  }

  maxInstancesReached(): void {
    const isDemoUser = this.userService.isRole(environment.KEYCLOAK_CONFIG.roles.demo_user);

    if (isDemoUser) {
      const userID = this.userService.getUserID();
      this.instanceService.getInstancesPerInstallerID(userID).subscribe(
        (res: InstanceItem[]) => {
          this.disableInstallButton = (res.length >= environment.KEYCLOAK_CONFIG.max_instances_per_demo_user);
        }
      );
    }
    else {
      this.disableInstallButton = false;
    }
  }

  getInstallGuideUrl(appName: string, version: string) {
    return `https://github.com/bibbox/${appName}/tree/${version}/INSTALL-APP.md`
  }
}
