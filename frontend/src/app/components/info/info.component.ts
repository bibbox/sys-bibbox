import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import {UserService} from '../../store/services/user.service';
import { DomSanitizer, SafeHtml } from "@angular/platform-browser";

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
    private _sanitizer: DomSanitizer
  ) {
  }

  ngOnInit(): void {
    // this.checkLogin().then(r => this.redirectIfLoggedIn())
    this.htmlStr = this._sanitizer.bypassSecurityTrustHtml(
      '<iframe width="100%" height="800" src="assets/landing.html"></iframe>',
    );
  }

  async checkLogin(): Promise<void> {
    this.isLoggedin = await this.userService.isLoggedIn();
  }

  redirectIfLoggedIn(): void {
    if (this.isLoggedin) {
      this.router.navigate(['/instances']);
    }
  }

}
