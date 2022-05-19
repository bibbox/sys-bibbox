import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ApplicationItem, EnvironmentParameters, IVersions} from '../../../store/models/application-group-item.model';
import {ApplicationService} from '../../../store/services/application.service';
import {
  AbstractControl,
  AsyncValidatorFn,
  FormBuilder,
  FormGroup,
  ValidationErrors,
  Validators
} from '@angular/forms';
import {InstanceService} from '../../../store/services/instance.service';
import {AppState} from '../../../store/models/app-state.model';
import {Store} from '@ngrx/store';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {AddInstanceAction} from '../../../store/actions/instance.actions';
import {ValidatorService} from '../../../store/services/validator.service';

@Component({
  selector: 'app-install-screen',
  templateUrl: './install-screen.component.html',
  styleUrls: ['./install-screen.component.scss']
})
export class InstallScreenComponent implements OnInit {

  constructor(
    private store: Store<AppState>,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private appService: ApplicationService,
    private instanceService: InstanceService,
    private formBuilder: FormBuilder,
    private validatorService: ValidatorService
  ) {

    // TODO: Find better Workaround
    // this prevents opening this view from somewhere other than the install screen dialog, as we get no state passed then
    if (this.router.getCurrentNavigation().extras.state === undefined) {
      this.router.navigateByUrl('/applications').then();
    }
  }

  appItem: ApplicationItem;
  selectedVersion: IVersions;
  environmentParameters: EnvironmentParameters[] = [];
  installForm: FormGroup;
  envParamForm: FormGroup;

  ngOnInit(): void {
    this.appItem = history.state[0];
    this.selectedVersion = history.state[1];
    this.loadEnvParams();

    this.installForm = this.formBuilder.group(
      {
        app_name: this.appItem.app_name,
        version: this.selectedVersion.app_version,
        instance_id: ['',
          [
            Validators.required,
            this.validatorService.noWhitespaceValidator,
            Validators.pattern(/^[a-z0-9]+([-_][a-z0-9]+)*$/),
            Validators.maxLength(48)
          ],
          [
            this.asyncInstanceNameValidator()
          ]
        ],
        instance_name: ['',
          [
            Validators.required,
            Validators.maxLength(48)
          ]
        ],
      });
    this.envParamForm = this.formBuilder.group({});
  }

  loadEnvParams(): void {
    this.appService.getAppEnvParams(this.selectedVersion.environment_parameters).subscribe({
    next: (res) => { this.environmentParameters = res; },
    complete: () => {this.initEnvParamFormFields(); }
  });
  }


  initEnvParamFormFields(): void {
    for (const envParam of this.environmentParameters) {
      this.envParamForm.addControl(
        envParam.id.valueOf(),
        this.formBuilder.control('', [
          Validators.required,
          Validators.minLength(Number(envParam.min_length)),
          Validators.maxLength(Number(envParam.max_length))]
        )
      );
    }
  }

  cancel(): void {
    this.router.navigateByUrl('/applications').then();
  }

  install(): void {
    if (this.installForm.valid && this.envParamForm.valid) {
      console.log('install');
      const payload = {
        displayname_short : this.installForm.value.instance_name,
        app : {
          organization : 'bibbox',
          name         : this.installForm.value.app_name,
          version      : this.installForm.value.version,
        },
        parameters  : this.envParamForm.value
      };

      console.log(this.installForm.value.instance_id, JSON.stringify(payload));

      this.store.dispatch(new AddInstanceAction(this.installForm.value.instance_id, JSON.stringify(payload)));
      // this.instanceService.postInstance(this.installForm.value.instance_id, JSON.stringify(payload))
      //   .toPromise()
      //   .then(
      //     res => console.log(res)
      //   );
      this.router.navigateByUrl('/instances').then();
    }
    else {
      console.log('errors occurred');
      this.validatorService.getFormValidationErrors(this.installForm);
      this.validatorService.getFormValidationErrors(this.envParamForm);
    }
  }


  asyncInstanceNameValidator(): AsyncValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      return this.instanceService.checkIfInstanceExists(this.installForm.controls.instance_id.value)
        .pipe(
          map((res: string) => {
              if (res === 'true') {
                return {
                  nameAlreadyExists: true
                };
              }
              else {
                return null;
              }
            }
          )
        );
    };
  }

}


