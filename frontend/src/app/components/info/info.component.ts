import { Component, Inject, OnInit, ViewEncapsulation } from '@angular/core';
import { Editor } from 'ngx-editor';
import {UserService} from '../../store/services/user.service';
import { DOCUMENT } from '@angular/common';
import { KeyValueService } from '../../store/services/keyvalue.service';
import { KeyValueItem } from '../../store/models/keyvalue.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { toolbar } from '../../commons';
import { FormControl } from '@angular/forms';

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
      this.htmlStr.setValue(keyValueItem?.values || '');
      this.keyValueId = String(keyValueItem?.id);
    });

    // this.htmlStr = this._sanitizer.bypassSecurityTrustHtml(
    //   '<iframe width="100%" height="400" src="assets/landing.html"></iframe>',
    // );
  }

  ngOnDestroy(): void {
    this.document.body.classList.remove('layout-width-full', 'white-header');
  }

  async checkLogin(): Promise<void> {
    this.isLoggedin = await this.userService.isLoggedIn();

    if(this.isLoggedin) {
      this.userFullname = await this.userService.getFullOrUsername();
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
    this.keyvalueService.updateValueByKey('info', {
      id: this.keyValueId,
      keys: 'info',
      values: this.htmlStr.value,
      value: this.htmlStr.value
    }).subscribe();
    
    this.editText(false);

    this.snackbar.open('Text saved', 'OK', {duration: 4000});
  }
}
