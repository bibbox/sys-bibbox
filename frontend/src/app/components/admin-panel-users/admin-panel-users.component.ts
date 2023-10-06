import {Component, OnInit} from '@angular/core';
import {KeycloakAdminBackendService} from '../../store/services/keycloak-admin-backend.service';
import {UserDictionary, UserRepresentation} from '../../store/models/user.model';
import {environment} from '../../../environments/environment';
import * as userSelector from '../../store/selectors/user.selector';
import {MatDialog} from '@angular/material/dialog';
import {CreateUserDialogComponent} from './create-user-dialog/create-user-dialog.component';
import {ConfirmationDialogComponent} from './confirmation-dialog/confirmation-dialog.component';
import {UserService} from '../../store/services/user.service';
import {AppState} from '../../store/models/app-state.model';
import {select, Store} from '@ngrx/store';
import {DeleteUserAction} from '../../store/actions/user.actions';

@Component({
  selector: 'app-admin-panel-users',
  templateUrl: './admin-panel-users.component.html',
  styleUrls: ['./admin-panel-users.component.scss']
})
export class AdminPanelUsersComponent implements OnInit {

  users: UserRepresentation[];

  kcRoles = {
    [environment.KEYCLOAK_CONFIG.roles.admin]: 'Admin',
    [environment.KEYCLOAK_CONFIG.roles.demo_user]: 'Demo User',
    [environment.KEYCLOAK_CONFIG.roles.standard_user]: 'Standard User'
  };

  constructor(
    private kc_admin_service: KeycloakAdminBackendService,
    private user_service: UserService,
    public dialog: MatDialog,
    private store: Store<AppState>,
  ) {
  }

  ngOnInit(): void {
    this.store.pipe(select(userSelector.selectAllUsers)).subscribe((res) => {
      this.users = res;
    });
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(CreateUserDialogComponent, {
      data: {usernames: this.users.map((user) => user.username)}
    });

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

  editUser(user: UserRepresentation): void {
    const dialogRef = this.dialog.open(CreateUserDialogComponent, {
      data: { usernames: this.users.map((user) => user.username), userToEdit: user }
    });
  }

  confirmDelete(user: UserRepresentation): void {
    let current_user_id = this.user_service.getUserID();

    if (user.id === current_user_id) {
      const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
        data: { message: 'You cannot delete your own account.', showCancel: false},
        panelClass: 'slim'
      });
      return;
    }

    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      data: { message: 'Are you sure you want to delete this user: '+ user.username +'?', showCancel: true },
      panelClass: 'slim'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        this.deleteUser(user);
      }
    });
  }

  deleteUser(user: UserRepresentation): void {
    this.store.dispatch(new DeleteUserAction(user.id));
  }
}
