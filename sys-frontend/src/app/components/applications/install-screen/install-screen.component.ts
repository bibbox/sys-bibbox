import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ApplicationItem, EnvironmentParameters, IVersions} from '../../../store/models/application-group-item.model';
import {ApplicationService} from '../../../store/services/application.service';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {InstanceService} from '../../../store/services/instance.service';
import {AppState} from '../../../store/models/app-state.model';
import {Store} from '@ngrx/store';
import {AddInstanceAction} from '../../../store/actions/instance.actions';

@Component({
  selector: 'app-install-screen',
  templateUrl: './install-screen.component.html',
  styleUrls: ['./install-screen.component.scss']
})
export class InstallScreenComponent implements OnInit {

  appItem: ApplicationItem;
  selectedVersion: IVersions;
  environmentParameters: EnvironmentParameters[];

  installForm: FormGroup;
  envParamFormGroup: FormGroup;

  constructor(
    private store: Store<AppState>,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private appService: ApplicationService,
    private instanceService: InstanceService,
    private formBuilder: FormBuilder
  ) {

    // TODO: Find better Workaround
    // this prevents opening this view from somewhere other than the install screen dialog, as we get no state passed then
    if (this.router.getCurrentNavigation().extras.state === undefined){
      this.router.navigateByUrl('/applications').then();
    }
  }


  ngOnInit(): void {
    this.appItem = history.state[0];
    this.selectedVersion = history.state[1];

    this.installForm = this.formBuilder.group(
      {
        app_name: this.appItem.app_name,
        version: this.selectedVersion.docker_version,
        instance_id: ['', Validators.required],
        instance_name: ['', Validators.required],
        envParams: new FormGroup({}),
      });

    this.loadEnvParams().then();
  }

  async loadEnvParams(): Promise<void> {
    console.warn(this.selectedVersion.environment_parameters);
    await this.appService.getAppEnvParams(this.selectedVersion.environment_parameters)
      .toPromise()
      .then(
        res => this.environmentParameters = res
      );
    this.initEnvParamFormFields();
  }


  initEnvParamFormFields(): void {
    this.envParamFormGroup = this.installForm.get('envParams') as FormGroup;
    for (const envParam of this.environmentParameters) {
      this.envParamFormGroup.addControl(
        envParam.id.valueOf(),
        new FormControl(
          envParam.default_value.valueOf(), [
            Validators.required,
            Validators.minLength(Number(envParam.min_length)),
            Validators.minLength(Number(envParam.max_length)),
          ]));
    }
  }

  cancel(): void {
    this.router.navigateByUrl('/applications').then();
  }

  install(): void {
    if (this.installForm.valid) { //        || 1
      console.log('install');
      console.log(this.envParamFormGroup.value);
      const payload = {
        displayname_short : this.installForm.value.instance_name,
        app : {
          organization : 'bibbox',
          name         : this.installForm.value.app_name,
          version      : this.installForm.value.version,
        },
        parameters  : this.envParamFormGroup.value
      };

      console.log(JSON.stringify(payload));
      this.store.dispatch(new AddInstanceAction(this.installForm.value.instance_id, JSON.stringify(payload)));
      // this.instanceService.postInstance(this.installForm.value.instance_id, JSON.stringify(payload))
      //   .toPromise()
      //   .then(
      //     res => console.log(res)
      //   );
      this.router.navigateByUrl('/instances').then();
    }
    else {
      console.log('form not valid');
    }
  }

  test(value: string): void {
    value = this.installForm.value.instance_name;
    console.log(value);
  }


}


