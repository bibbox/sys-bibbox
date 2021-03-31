import {Component, Inject, OnInit} from '@angular/core';
import {ApplicationItem, IVersions} from '../../../store/models/application-group-item.model';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import {FormControl, Validators} from '@angular/forms';

@Component({
  selector: 'app-install-screen-dialog',
  templateUrl: './install-screen-dialog.component.html',
  styleUrls: ['./install-screen-dialog.component.scss']
})
export class InstallScreenDialogComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public applicationItem: ApplicationItem) {

  }

  versionFormControl = new FormControl('', Validators.required);
  selectedVersion: IVersions;

  ngOnInit(): void {
    this.selectedVersion = this.applicationItem.versions[0];
  }
  openInstallScreen(): void {

    // console.warn(this.applicationItem);
    // todo: store call for add Instance
    // todo: open install screen and pass relevant arguments (applicationItem, selectedVersion)
    // todo: where do I get the 'organization' parameter from?
  }
}
