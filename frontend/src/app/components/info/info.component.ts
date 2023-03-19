import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import {UserService} from '../../store/services/user.service';

@Component({
  selector: 'app-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.scss']
})
export class InfoComponent implements OnInit {

  isLoggedin = false;

  constructor(
    private router: Router,
    private userService: UserService,
  ) {
  }

  ngOnInit(): void {
    this.checkLogin().then(r => this.redirectIfLoggedIn())
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
