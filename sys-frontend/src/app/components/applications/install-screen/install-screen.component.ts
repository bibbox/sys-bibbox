import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ApplicationItem, EnvironmentParameters, IVersions} from '../../../store/models/application-group-item.model';
import {ApplicationService} from '../../../store/services/application.service';
import {Form, FormArray, FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {InstanceService} from '../../../store/services/instance.service';

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
  envParamFormArray: FormArray;

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private appService: ApplicationService,
    private instanceService: InstanceService,
    private formBuilder: FormBuilder
  ) {

    // TODO: Find better Workaround
    // this prevents opening this view from somewhere other than the install screen dialog, as we get no state passed then
    if (!(history.state[0])){
      this.router.navigateByUrl('/applications').then();
    }
  }


  ngOnInit(): void {
    this.appItem = history.state[0];
    this.selectedVersion = history.state[1];
    this.loadEnvParams().then();

    this.installForm = this.formBuilder.group(
      {
        app_name: this.appItem.app_name,
        version: this.selectedVersion.docker_version,
        instance_id: ['', Validators.required],
        instance_name: ['', Validators.required],
        envParams: this.formBuilder.array([]),
      });
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
    this.envParamFormArray = this.installForm.get('envParams') as FormArray;
    for (const envParam of this.environmentParameters) {
      this.envParamFormArray.push(this.addEnvParamFormField(envParam));
    }
  }

  addEnvParamFormField(envParamEntry: EnvironmentParameters): FormControl {
    console.warn(envParamEntry);
    console.warn(envParamEntry.default_value.valueOf());
    return this.formBuilder.control({
      value: [envParamEntry.default_value.valueOf(),
      [
        Validators.required,
        Validators.minLength(Number(envParamEntry.min_length)),
        Validators.minLength(Number(envParamEntry.max_length)),
      ]
    ]});
  }


  cancel(): void {
    this.router.navigateByUrl('/applications').then();
  }

  install(): void {
  const payload = {
    displayname : this.installForm.value.instance_name,
    app : {
      organization : 'bibbox',
      name         : this.installForm.value.app_name,
      version      : this.installForm.value.version,
    },
    parameters  : { }
  };


  // TODO: get inserted form values.
  // for (const envParam of this.envParamForms.value) {
  //   payload.parameters[envParam] = envParam.value;
  // }

  console.log(payload);
  // this.instanceService.addInstance(this.installForm.value.instance_id, payload);
  }

  test(value: string): void {
    value = this.installForm.value.instance_name;
    console.log(value);
  }
}


