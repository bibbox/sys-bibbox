import {Component, Inject, OnInit} from '@angular/core';
import {ApplicationItem, IVersions} from '../../../store/models/application-group-item.model';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import {FormControl, Validators} from '@angular/forms';
import {Router} from '@angular/router';

@Component({
  selector: 'app-install-screen-dialog',
  templateUrl: './install-screen-dialog.component.html',
  styleUrls: ['./install-screen-dialog.component.scss']
})
export class InstallScreenDialogComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public applicationItem: ApplicationItem,
              private router: Router) {
  }

  versionFormControl = new FormControl('', Validators.required);
  selectedVersion: IVersions;

  public appObj;
  public appVersion;


  ngOnInit(): void {
    this.selectedVersion = this.applicationItem.versions[0];
  }
  openInstallScreen(): void {
    this.appObj = {...this.applicationItem};
    this.appObj.versions = this.selectedVersion;
    console.warn(this.applicationItem);

    this.router.navigateByUrl('install/' + this.applicationItem.app_name + '/' + this.selectedVersion.version, {state: this.appObj});

    // todo: store call for add Instance
  }
}
