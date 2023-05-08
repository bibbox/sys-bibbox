import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import {environment} from '../../../../environments/environment';
import {KeycloakService} from 'keycloak-angular';

@Component({
  selector: 'app-create-user-dialog',
  templateUrl: './create-user-dialog.component.html',
})
export class CreateUserDialogComponent {
  userForm: FormGroup;
  hidePassword = true;

  kcRoles = [
    {
      value: environment.KEYCLOAK_ROLES.admin,
      name: 'Admin'
    },
    {
      value: environment.KEYCLOAK_ROLES.demo_user,
      name: 'Demo User'
    },
    {
      value: environment.KEYCLOAK_ROLES.standard_user,
      name: 'Standard User'
    }
  ]

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<CreateUserDialogComponent>,
    private kcService: KeycloakService,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.userForm = this.fb.group({
      username: ['', Validators.required], // add validator s.t. username is unique
      password: ['', Validators.required],
      role: ['', Validators.required],
      email: ['', []],
      firstName: ['', []],
      lastName: ['', []],
    });
  }

  onSave() {
    this.dialogRef.close(this.userForm.value);
  }

  onCancel() {
    this.dialogRef.close();
  }
}
