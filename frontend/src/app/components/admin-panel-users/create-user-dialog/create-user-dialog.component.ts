import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {FormGroup, FormBuilder, Validators, ValidationErrors, AbstractControl} from '@angular/forms';
import {environment} from '../../../../environments/environment';
import {ValidatorService} from '../../../store/services/validator.service';
import { UserCreateDialogProps } from '../../../store/models/user.model';

@Component({
  selector: 'app-create-user-dialog',
  templateUrl: './create-user-dialog.component.html',
  styleUrls: ['create-user-dialog.component.scss']
})
export class CreateUserDialogComponent {
  userForm: FormGroup;
  hidePassword = true;
  isEditMode = false;

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
  ];

  usernameMaxLength = 20;
  usernameMinLength = 3;
  passwordMaxLength = 32;
  passwordMinLength = 8;

  constructor(
    @Inject(MAT_DIALOG_DATA) public props: UserCreateDialogProps,
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<CreateUserDialogComponent>,
    private validatorService: ValidatorService
  ) {
  }

  ngOnInit(): void {
    this.isEditMode = !!this.props.userToEdit;

    this.userForm = this.fb.group({
      username: [this.props.userToEdit?.username || '', [
        Validators.required,
        this.validatorService.noWhitespaceValidator,
        this.validatorService.isAlphanumericValidator,
        this.usernameExistsValidator,
        Validators.maxLength(this.usernameMaxLength),
        Validators.minLength(this.usernameMinLength)
      ]], // add validator s.t. username is unique
      password: ['', [
        Validators.maxLength(this.passwordMaxLength),
        Validators.minLength(this.passwordMinLength)
      ]],
      role: [this.props.userToEdit?.roles[0] || environment.KEYCLOAK_CONFIG.roles.standard_user, [
        Validators.required,
        this.isRoleInKcRolesValidator
      ]],
      email: [this.props.userToEdit?.email || '',
        [Validators.email]
      ],
      firstName: [this.props.userToEdit?.firstName || '', []],
      lastName: [this.props.userToEdit?.lastName || '', []],
    });

    if(!this.isEditMode) {
      console.log('add constraint');
      this.userForm.controls.password.addValidators(Validators.required);
    }
  }

  usernameExistsValidator = (control: AbstractControl): ValidationErrors | null => {
    if (this.props.usernames.includes(control.value.toLowerCase()) && control.value.toLowerCase() !== this.props.userToEdit.username.toLowerCase()) {
      return {usernameExists: true};
    }
    return null;
  }

  isRoleInKcRolesValidator = (control: AbstractControl): ValidationErrors | null => {
    if (!this.checkIfRoleInKcRoles(control.value)) {
      return {roleNotInKcRoles: true};
    }
    return null;
  }

  checkIfRoleInKcRoles(role: string) {
    return this.kcRoles.find(kcRole => kcRole.value === role);
  }

  onSave() {
    this.dialogRef.close(this.userForm.value);
  }

  onCancel() {
    this.dialogRef.close();
  }
}
