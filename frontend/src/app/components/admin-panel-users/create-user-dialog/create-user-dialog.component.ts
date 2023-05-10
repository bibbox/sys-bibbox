import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {FormGroup, FormBuilder, Validators, ValidationErrors, AbstractControl} from '@angular/forms';
import {environment} from '../../../../environments/environment';
import {ValidatorService} from '../../../store/services/validator.service';

@Component({
  selector: 'app-create-user-dialog',
  templateUrl: './create-user-dialog.component.html',
})
export class CreateUserDialogComponent {
  userForm: FormGroup;
  hidePassword = true;

  kcRoles = [
    {
      value: environment.KEYCLOAK_CONFIG.roles.admin,
      name: 'Admin'
    },
    {
      value: environment.KEYCLOAK_CONFIG.roles.demo_user,
      name: 'Demo User'
    },
    {
      value: environment.KEYCLOAK_CONFIG.roles.standard_user,
      name: 'Standard User'
    }
  ]

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<CreateUserDialogComponent>,
    private validatorService: ValidatorService,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.userForm = this.fb.group({
      username: ['', [Validators.required, this.validatorService.noWhitespaceValidator, this.usernameExistsValidator]], // add validator s.t. username is unique
      password: ['', Validators.required],
      role: ['', Validators.required],
      email: ['', []],
      firstName: ['', []],
      lastName: ['', []],
    });
  }

  usernameExistsValidator = (control: AbstractControl): ValidationErrors | null => {
    if (this.data.usernames.includes(control.value)) {
      return {usernameExists: true};
    }
    return null;
  }

  onSave() {
    this.dialogRef.close(this.userForm.value);
  }

  onCancel() {
    this.dialogRef.close();
  }


}
