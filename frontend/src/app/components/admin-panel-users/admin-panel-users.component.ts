import {Component, ENVIRONMENT_INITIALIZER, OnInit} from '@angular/core';
import {KeycloakAdminBackendService} from '../../store/services/keycloak-admin-backend.service';
import {UserDictionary, UserRepresentation} from '../../store/models/user.model';
import {Observable} from 'rxjs';
import {environment} from '../../../environments/environment';
import {AbstractControl, FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {UserRoles, UserRoleMapping} from '../../store/models/user.model';
import {InstanceItem} from '../../store/models/instance-item.model';
import {MatDialog} from '@angular/material/dialog';
import {CreateUserDialogComponent} from './create-user-dialog/create-user-dialog.component';
import {ConfirmationDialogComponent} from './confirmation-dialog/confirmation-dialog.component';
import {UserService} from '../../store/services/user.service';

@Component({
  selector: 'app-admin-panel-users',
  templateUrl: './admin-panel-users.component.html',
  styleUrls: ['./admin-panel-users.component.scss']
})
export class AdminPanelUsersComponent implements OnInit {

  users: UserRepresentation[];
  userForms: FormGroup[];
  updatedUsers: UserRepresentation[] = [];


  toObject = Object.keys;
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
    private kc_admin_service: KeycloakAdminBackendService,
    private user_service: UserService,
    private fb: FormBuilder,
    public dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.kc_admin_service.getUsers().subscribe((users) => {
      this.users = users;
      this.createForms();
    });

  }

  // TODO: disable editing the role of the super admin user


  createForms(): void {
    this.userForms = this.users.map(user => {
      return this.fb.group({
        id: [user.id],
        username: [user.username, Validators.required],
        role: [user.roles[0], Validators.required],
        email: [user.email, []],
        firstName: [user.firstName, []],
        lastName: [user.lastName, []],
      });
    });
  }

  confirmUpdateUsers(): void {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '250px',
      data: {title: 'Update Users', message: 'Are you sure you want to update all users?', showCancel: true}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.updateUsers();
      }
    });
  }


  updateUsers(): void {
    this.updatedUsers = [];

    this.userForms.forEach((userForm) => {
      let user = this.users.find((user) => user.id === userForm.value.id);
      user.username = userForm.value.username;
      user.roles = [userForm.value.role];
      this.updatedUsers.push(user);
    });

    const current_user_id = this.user_service.getUserID();
    const current_user = this.updatedUsers.find((user) => user.id === current_user_id);

    if (current_user.roles[0] !== environment.KEYCLOAK_ROLES.admin) {
      const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
        width: '250px',
        data: { message: 'You cannot revoke your own admin privileges.', showCancel: false}
      });

      dialogRef.afterClosed().subscribe(result => {
        // refresh table
      });
      return;
    }


    let userRoleMapping: UserRoleMapping = {
      user_role_mappings: []
    };
    userRoleMapping.user_role_mappings = [];
    this.updatedUsers.forEach((user) => {

      let userRoleObj: UserRoles = {
        user_id: user.id,
        roles: user.roles
      }
      userRoleMapping.user_role_mappings.push(userRoleObj);
    });

    // alert(JSON.stringify(userRoleMapping, null, 4));
    console.log(userRoleMapping);
    this.kc_admin_service.setRolesForMultipleUsers(userRoleMapping).subscribe((res) => {
      console.log(res);
    });
  }


  // updateUsers(): void {
  //
  //   let userRoleObj = {
  //     user_id: '',
  //     roles: []
  //   }
  //
  //   let userRoleMapping = {
  //     user_role_mappings: []
  //   }
  //
  //   this.kc_admin_service.getUsers().subscribe((res) => {
  //     this.users = res;
  //   });
  // }

  openDialog(): void {
    const dialogRef = this.dialog.open(CreateUserDialogComponent, {
      width: '300px',
      maxWidth: '90vw',
      maxHeight: '90vh',
      panelClass: 'custom-dialog-container',
    })

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {

        let userDictionary: UserDictionary = {
          'username': result.username,
          'password': result.password,
          'email': result.email,
          'firstName': result.firstName,
          'lastName': result.lastName,
          'roles': [result.role]
        }

        this.kc_admin_service.createUser(userDictionary).subscribe((res) => {
          // alert(JSON.stringify(res, null, 4));
          // console.log(res);
          // this.kc_admin_service.getUsers().subscribe((users) => {this.updatedUsers = users});
        });

        // update the table
      }
    })
  }

  confirmDelete(user: UserRepresentation): void {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '250px',
      data: { message: 'Are you sure you want to delete this user: '+ user.username +'?', showCancel: true }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      if (result === true) {
        this.deleteUser(user);
      }
    });
  }

  deleteUser(user: UserRepresentation): void {
    // Send delete request to API

    let idToDelete = user.id;

    this.kc_admin_service.deleteUser(idToDelete).subscribe((res) => {

    });

    // update the table

  }

}
