import {Component, Inject, OnInit} from '@angular/core';
import {AppInfo, ApplicationItem, IVersions} from '../../../store/models/application-group-item.model';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import {FormControl, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {ApplicationService} from '../../../store/services/application.service';
@Component({
  selector: 'app-install-screen-dialog',
  templateUrl: './install-screen-dialog.component.html',
  styleUrls: ['./install-screen-dialog.component.scss']
})
export class InstallScreenDialogComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public applicationItem: ApplicationItem,
              private router: Router,
              private appService: ApplicationService) {
    this.selectedVersion = this.applicationItem.versions[0];
    this.loadAppInfo();
  }

  versionFormControl = new FormControl('', Validators.required);
  selectedVersion: IVersions;
  appInfo: AppInfo | null;

  ngOnInit(): void {
  }

  async loadAppInfo(): Promise<void> {
    await this.appService.getAppInfo(this.selectedVersion.appinfo).toPromise().then(
      res => this.appInfo = res
    );
  }

  openInstallScreen(): void {
    this.router.navigateByUrl('install/' + this.applicationItem.app_name + '/' + this.selectedVersion.version,
      {state: [{...this.applicationItem}, this.selectedVersion]}
    );

    // todo: store call for add Instance
  }
}
