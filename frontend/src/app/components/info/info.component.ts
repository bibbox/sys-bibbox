import { Component, Inject, OnInit, ViewEncapsulation } from '@angular/core';
import { Editor } from 'ngx-editor';
import {UserService} from '../../store/services/user.service';
import { DOCUMENT } from '@angular/common';
import { KeyValueService } from '../../store/services/keyvalue.service';
import { KeyValueItem } from '../../store/models/keyvalue.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { toolbar } from '../../commons';
import { FormControl } from '@angular/forms';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class InfoComponent implements OnInit {

  isLoggedin = false;
  userFullname: string = '';
  editMode: boolean = false;
  htmlStr = new FormControl('');
  editor: Editor;
  toolbar = toolbar;
  keyValueId: string;
  keyExistsYet: boolean = false;
  isAdmin: boolean = false;

  constructor(
    private userService: UserService,
    private snackbar: MatSnackBar,
    @Inject(DOCUMENT) private document: Document,
    private keyvalueService: KeyValueService
  ) {
  }

  async ngOnInit(): Promise<void> {
    await this.checkLogin();
    this.document.body.classList.add('layout-width-full');

    if(this.isLoggedin) {
      this.document.body.classList.add('white-header');
    }

    (await this.keyvalueService.getValueByKey('info')).subscribe((keyValueItem: KeyValueItem) => {
      if(!!keyValueItem?.values) {
        this.keyExistsYet = true;
      }

      this.htmlStr.setValue(keyValueItem?.values || '');
      this.keyValueId = String(keyValueItem?.id);
    });
  }

  ngOnDestroy(): void {
    this.document.body.classList.remove('layout-width-full', 'white-header');
  }

  async checkLogin(): Promise<void> {
    this.isLoggedin = await this.userService.isLoggedIn();

    if(this.isLoggedin) {
      this.userFullname = await this.userService.getFullOrUsername();
      this.isAdmin = await this.userService.isRole(environment.KEYCLOAK_CONFIG.roles.admin);
    }
  }

  initiateLogin(): void {
    this.userService.login();
  }

  switchAccounts(): void {
    this.userService.switchAccount();
  }

  editText(edit: boolean): void {
    if(edit) {
      this.editor = new Editor();
    }
    else if(!!this.editor) {
      this.editor.destroy();
    }

    this.editMode = edit;
  }

  saveText(): void {
    const payload = {
      id: this.keyValueId,
      keys: 'info',
      values: this.htmlStr.value,
      value: this.htmlStr.value
    };

    if(this.keyExistsYet) {
      this.keyvalueService.updateValueByKey('info', payload).subscribe();
    }
    else {
      this.keyvalueService.createValueByKey('info', payload).subscribe(() => {
        this.keyExistsYet = true;
      });
    }
    
    this.editText(false);

    this.snackbar.open('Text saved', 'OK', {duration: 4000});
  }
}
