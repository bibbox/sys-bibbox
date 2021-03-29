import {Component, Inject, OnInit} from '@angular/core';
import {ApplicationItem} from '../../../store/models/application-group-item.model';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

@Component({
  selector: 'app-install-screen-dialog',
  templateUrl: './install-screen-dialog.component.html',
  styleUrls: ['./install-screen-dialog.component.scss']
})
export class InstallScreenDialogComponent implements OnInit {

  constructor(public dialogRef: MatDialogRef<InstallScreenDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public applicationItem: ApplicationItem) { }

  ngOnInit(): void {
  }

  installApp(): void {
    // todo: store call for add Instance
  }
}
