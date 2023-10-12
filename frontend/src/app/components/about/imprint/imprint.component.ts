import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FormControl } from '@angular/forms';
import { Editor } from 'ngx-editor';
import {UserService} from '../../../store/services/user.service';
import { KeyValueService } from '../../../store/services/keyvalue.service';
import { KeyValueItem } from '../../../store/models/keyvalue.model';
import { toolbar } from '../../../commons';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-imprint',
  templateUrl: './imprint.component.html',
  styleUrls: ['./imprint.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class ImprintComponent implements OnInit {

  isLoggedin = false;
  editMode: boolean = false;
  prevText: string;
  htmlStr = new FormControl('');
  editor: Editor;
  toolbar = toolbar;
  keyValueId: string;
  keyExistsYet: boolean = false;
  isAdmin: boolean = false;

  constructor(
    private userService: UserService,
    private snackbar: MatSnackBar,
    private keyvalueService: KeyValueService
  ) {
  }

  async ngOnInit(): Promise<void> {
    this.isLoggedin = await this.userService.isLoggedIn();

    if(this.isLoggedin) {
      this.isAdmin = await this.userService.isRole(environment.KEYCLOAK_CONFIG.roles.admin);
    }

    (await this.keyvalueService.getValueByKey('imprint')).subscribe((keyValueItem: KeyValueItem) => {
      if(!!keyValueItem?.values) {
        this.keyExistsYet = true;
      }

      this.htmlStr.setValue(keyValueItem?.values || '');
      this.keyValueId = String(keyValueItem?.id);
    });
  }

  editText(edit: boolean, restore = true): void {
    if(edit) {
      this.prevText = this.htmlStr.value;
      this.editor = new Editor();
    }
    else if(!!this.editor) {
      if(restore) {
        this.htmlStr.setValue(this.prevText)
      }

      this.editor.destroy();
    }

    this.editMode = edit;
  }

  saveText(): void {
    const payload = {
      id: this.keyValueId,
      keys: 'imprint',
      values: this.htmlStr.value,
      value: this.htmlStr.value
    };

    if(this.keyExistsYet) {
      this.keyvalueService.updateValueByKey('imprint', payload).subscribe();
    }
    else {
      this.keyvalueService.createValueByKey('imprint', payload).subscribe(() => {
        this.keyExistsYet = true;
      });
    }
    
    this.editText(false, false);

    this.snackbar.open('Text saved', 'OK', {duration: 4000});
  }
}
