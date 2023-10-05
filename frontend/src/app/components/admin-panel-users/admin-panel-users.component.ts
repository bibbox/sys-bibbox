import {Component, OnInit} from '@angular/core';
import {KeycloakAdminBackendService} from '../../store/services/keycloak-admin-backend.service';
import {UserDictionary, UserRepresentation} from '../../store/models/user.model';
import {environment} from '../../../environments/environment';
import {AbstractControl, FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {UserRoles, UserRoleMapping} from '../../store/models/user.model';
import * as userSelector from '../../store/selectors/user.selector';
import {MatDialog} from '@angular/material/dialog';
import {CreateUserDialogComponent} from './create-user-dialog/create-user-dialog.component';
import {ConfirmationDialogComponent} from './confirmation-dialog/confirmation-dialog.component';
import {UserService} from '../../store/services/user.service';
import {AppState} from '../../store/models/app-state.model';
import {select, Store} from '@ngrx/store';
import {SocketioService} from '../../store/services/socketio.service';
import {CreateUserAction, DeleteUserAction, UpdateUserRoleMappingsAction} from '../../store/actions/user.actions';

@Component({
  selector: 'app-admin-panel-users',
  templateUrl: './admin-panel-users.component.html',
  styleUrls: ['./admin-panel-users.component.scss']
})
export class AdminPanelUsersComponent implements OnInit {

  users: UserRepresentation[];
  userForms: FormGroup[];
  updatedUsers: UserRepresentation[] = [];

  kcRoles = {
    [environment.KEYCLOAK_CONFIG.roles.admin]: 'Admin',
    [environment.KEYCLOAK_CONFIG.roles.demo_user]: 'Demo User',
    [environment.KEYCLOAK_CONFIG.roles.standard_user]: 'Standard User'
  };

  constructor(
    private kc_admin_service: KeycloakAdminBackendService,
    private user_service: UserService,
    private fb: FormBuilder,
    public dialog: MatDialog,
    private store: Store<AppState>,
  ) {
  }

  ngOnInit(): void {
    // this.kc_admin_service.getUsers().subscribe((users) => {
    //   this.users = users;
    //   this.createForms();
    // });


    this.store.pipe(select(userSelector.selectAllUsers)).subscribe((res) => {
      this.users = res;
      this.createForms();
    });

    // each time the state changes, we need to update the forms
    this.store.select(state => state.users).subscribe((res) => {
      this.createForms();
    });


  }

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
      user = Object.assign({}, user, {
        username: userForm.value.username,
        roles: [userForm.value.role]
      });
      //
      // user.username = userForm.value.username;
      // user.roles = [userForm.value.role];
      this.updatedUsers.push(user);
    });

    const current_user_id = this.user_service.getUserID();
    const current_user = this.updatedUsers.find((user) => user.id === current_user_id);

    if (current_user.roles[0] !== environment.KEYCLOAK_CONFIG.roles.admin) {
      const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
        width: '250px',
        data: { message: 'You cannot revoke your own admin privileges.', showCancel: false}
      });

      dialogRef.afterClosed().subscribe(result => {
        this.store.pipe(select(userSelector.selectAllUsers)).subscribe((res) => {
          this.users = res;
          this.createForms();
        });
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

    this.store.dispatch(new UpdateUserRoleMappingsAction(userRoleMapping));
  }


  openDialog(): void {
    const dialogRef = this.dialog.open(CreateUserDialogComponent, {
      width: '300px',
      maxWidth: '90vw',
      maxHeight: '90vh',
      panelClass: 'custom-dialog-container',
      data: {usernames: this.users.map((user) => user.username)}
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

        // this.store.dispatch(new CreateUserAction(userDictionary));

        this.kc_admin_service.createUser(userDictionary).subscribe();

        // update the table
      }
    })
  }

  confirmDelete(user: UserRepresentation): void {
    let current_user_id = this.user_service.getUserID();
    if (user.id === current_user_id) {
      const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
        width: '250px',
        data: { message: 'You cannot delete your own account.', showCancel: false}
      });
      return;
    }

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

  edit(user: UserRepresentation): void {
    // this.store.dispatch(new DeleteUserAction(user.id));
  }

  deleteUser(user: UserRepresentation): void {
    this.store.dispatch(new DeleteUserAction(user.id));
  }
}
