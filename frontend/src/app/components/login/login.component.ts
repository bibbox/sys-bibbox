import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  public loginForm: FormGroup;
  public userName: string;
  public password: string;


  constructor(
    private formBuilder: FormBuilder,
    // public readonly userService: UserService,
  ) {
    this.loginForm = formBuilder.group(
      {
        username: ['', Validators.required],
        password: ['', Validators.required]
      });
  }

  getUsername(): string {
    return this.loginForm.value.username;
  }

  getPassword(): string {
    return this.loginForm.value.password;
  }

  logFunct(usr: string, pw: string): void {
    console.log('login ', usr, ' pw: ', pw);
  }
}
