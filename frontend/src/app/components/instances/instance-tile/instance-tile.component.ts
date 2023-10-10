import {Component, Input, OnInit, ViewEncapsulation} from '@angular/core';
import {InstanceItem} from '../../../store/models/instance-item.model';
import {environment} from '../../../../environments/environment';
import { UserService } from '../../../store/services/user.service';
import { InstanceService } from '../../../store/services/instance.service';
import { Store } from '@ngrx/store';
import { AppState } from '../../../store/models/app-state.model';
import { MatDialog } from '@angular/material/dialog';
import { InstanceDeleteDialogComponent } from '../instance-delete-dialog/instance-delete-dialog.component';

@Component({
  selector: 'app-instance-tile',
  templateUrl: './instance-tile.component.html',
  styleUrls: ['./instance-tile.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class InstanceTileComponent implements OnInit {

  constructor(private store: Store<AppState>, private instanceService: InstanceService, private userService: UserService, public dialog: MatDialog) { }

  @Input() instance: InstanceItem;
  instanceUrl: string;
  isOpen = false;

  ngOnInit(): void {
    this.getInstanceUrl();
  }

  getInstanceUrl(): void {
    if (this.instance.proxy !== undefined) {
      for (const proxy of this.instance.proxy) {
        if (proxy.TYPE === 'PRIMARY') {
          this.instanceUrl = 'http://' + this.instance.instancename + '.' + environment.BASEURL;
        }
      }
    }
  }

  toggle(open?: boolean) {
    if(typeof open === 'undefined') {
      this.isOpen = !this.isOpen;
    }
    else {
      this.isOpen = open;
    }
  }

  canManageInstance(): boolean {
    const isAdmin = this.userService.isRole(environment.KEYCLOAK_CONFIG.roles.admin);
    const doesInstanceOwnerMatch = this.userService.getUserID() === this.instance.installed_by_id;

    return isAdmin || doesInstanceOwnerMatch;
  }

  deleteInstance(): void {
    this.toggle(false);

    // const isAdmin = this.userService.isRole(KEYCLOAK_ROLES.admin);
    // const doesInstanceOwnerMatch = this.userService.getUserID() === this.instanceItem.installed_by;
    //
    // if (!(isAdmin || doesInstanceOwnerMatch)) {
    //   this.snackbar.open('You are not allowed to delete this instance', 'OK', {duration: 4000});
    //   return;
    // }

    // console.log('delete instance:' + this.instanceItem.instancename);


    const dialogRef = this.dialog.open(InstanceDeleteDialogComponent, {
      data: this.instance.instancename,
      panelClass: 'slim'
    });

    // this.instanceService.deleteInstance(this.instanceItem.instancename).subscribe(
    //   (res) => console.log(res)
    // );
    // this.router.navigateByUrl('/instances').then();
  }

  manageInstance(operation: string): void {
    this.toggle(false);

    this.instanceService.manageInstance(this.instance.instancename, operation).subscribe((res) => console.log(res));
  }
}
