import {Component, Input, OnInit} from '@angular/core';
import {InstanceItem} from '../../../store/models/instance-item.model';
import {environment} from '../../../../environments/environment';
import { UserService } from '../../../store/services/user.service';
import { InstanceService } from '../../../store/services/instance.service';
import { Store } from '@ngrx/store';
import { AppState } from '../../../store/models/app-state.model';
import { DeleteInstanceAction } from '../../../store/actions/instance.actions';
import { MatDialog } from '@angular/material/dialog';
import { InstanceDeleteDialogComponent } from '../instance-delete-dialog/instance-delete-dialog.component';

@Component({
  selector: 'app-instance-list-item',
  templateUrl: './instance-list-item.component.html',
  styleUrls: ['./instance-list-item.component.scss']
})
export class InstanceListItemComponent implements OnInit {

  constructor(private store: Store<AppState>, private instanceService: InstanceService, private userService: UserService, public dialog: MatDialog) { }

  @Input() instance: InstanceItem;
  instanceUrl: string;
  repositoryUrl: string;
  installGuideUrl: string;
  isOpen = false;
  sanitizedDescription: string;
  description: string;
  shortenDescription = false;
  showFullDescription = false;

  ngOnInit(): void { 
    this.sanitizedDescription = this.instance.description_short;
    this.sanitizedDescription = this.sanitizedDescription.replace(/<li>/gi, "\n");
    this.sanitizedDescription = this.sanitizedDescription.replace(/<\/ul>/gi, "\n");
    this.sanitizedDescription = this.sanitizedDescription.replace(/<\/p>/gi, "\n");
    this.sanitizedDescription = this.sanitizedDescription.replace(/<a.*href="(.*?)".*>(.*?)<\/a>/gi, " $2 ($1) ");
    this.sanitizedDescription = this.sanitizedDescription.replace(/<br\s*[\/]?>/gi, "\n");
    this.sanitizedDescription = this.sanitizedDescription.replace(/<[^>]+>/g, "");

    if(this.sanitizedDescription.length > 60) {
      this.description = this.sanitizedDescription.substring(0, 60);
      this.shortenDescription = true;
    }
    else {
      this.description = this.sanitizedDescription;
    }

    this.getInstanceUrl();

    this.repositoryUrl = this.getRepositoryUrl(this.instance.app.name, this.instance.app.version);
    this.installGuideUrl = this.getInstallGuideUrl(this.instance.app.name, this.instance.app.version);
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

    const dialogRef = this.dialog.open(InstanceDeleteDialogComponent, {
      data: this.instance.instancename,
      panelClass: 'slim'
    });
  }

  manageInstance(operation: string): void {
    this.toggle(false);

    this.instanceService.manageInstance(this.instance.instancename, operation).subscribe((res) => console.log(res));
  }

  getRepositoryUrl(appName: string, version: string) {
    return `https://github.com/bibbox/${appName}/tree/${version}`;
  }

  getInstallGuideUrl(appName: string, version: string) {
    return `${this.getRepositoryUrl(appName, version)}/INSTALL-APP.md`;
  }

  toggleShowFully(e): void {
    e.stopPropagation();
    this.showFullDescription = !this.showFullDescription;

    if(this.showFullDescription) {
      this.description = this.sanitizedDescription;
    }
    else {
      this.description = this.sanitizedDescription?.substring(0, 60);
    }
  }
}
