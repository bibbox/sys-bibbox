import { Component, Inject, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import {UserService} from '../../store/services/user.service';
import { DomSanitizer } from "@angular/platform-browser";
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.scss']
})
export class InfoComponent implements OnInit {

  isLoggedin = false;
  public htmlStr: any;

  constructor(
    private router: Router,
    private userService: UserService,
    private _sanitizer: DomSanitizer,
    @Inject(DOCUMENT) private document: Document
  ) {
  }

  async ngOnInit(): Promise<void> {
    await this.checkLogin();
    this.document.body.classList.add('layout-width-full');

    if(this.isLoggedin) {
      this.document.body.classList.add('white-header');
    }

    this.htmlStr = this._sanitizer.bypassSecurityTrustHtml(
      '<iframe width="100%" height="400" src="assets/landing.html"></iframe>',
    );
  }

  ngOnDestroy(): void {
    this.document.body.classList.remove('layout-width-full', 'white-header');
  }

  async checkLogin(): Promise<void> {
    this.isLoggedin = await this.userService.isLoggedIn();
  }

  initiateLogin(): void {
    this.userService.login();
  }
}
