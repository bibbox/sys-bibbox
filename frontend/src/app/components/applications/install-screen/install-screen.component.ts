import {Component, Inject, OnDestroy, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import { Editor } from 'ngx-editor';
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
import {UserService} from '../../../store/services/user.service';
import { toolbar } from '../../../commons';

@Component({
  selector: 'app-install-screen',
  templateUrl: './install-screen.component.html',
  styleUrls: ['./install-screen.component.scss']
})
export class InstallScreenComponent implements OnInit, OnDestroy {

  constructor(
    private store: Store<AppState>,
    private router: Router,
    private appService: ApplicationService,
    private instanceService: InstanceService,
    private formBuilder: FormBuilder,
    private validatorService: ValidatorService,
    private userService: UserService
  ) {

    // TODO: Find better Workaround
    // this prevents opening this view from somewhere other than the install screen dialog, as we get no state passed then
    if (this.router.getCurrentNavigation().extras.state === undefined) {
      this.router.navigateByUrl('/applications').then();
    }
  }

  appItem: ApplicationItem;
  selectedVersion: IVersions;
  installGuideUrl: string;
  applicationDocumentationUrl: string;
  environmentParameters: EnvironmentParameters[] = [];
  installForm: FormGroup;
  envParamForm: FormGroup;
  entered_values: Record<string, string> = {};
  editor: Editor;
  toolbar = toolbar;

  ngOnInit(): void {
    this.appItem = history.state[0];
    this.selectedVersion = history.state[1];
    this.installGuideUrl = history.state[2];
    this.applicationDocumentationUrl = history.state[3];
    this.loadEnvParams();

    this.installForm = this.formBuilder.group(
      {
        app_name: this.appItem.app_name,
        version: this.selectedVersion.app_version,
        instance_id: ['',
          [
            Validators.required,
            this.validatorService.noWhitespaceValidator,
            Validators.pattern(/^(?!0)[a-z0-9]+([a-z0-9]+)*$/),
            Validators.maxLength(48)
          ],
          [
            this.asyncInstanceNameValidator()
          ]
        ],
        instance_title: ['',
          [
            Validators.required,
            Validators.maxLength(48)
          ]
        ],
        instance_subtitle: ['',
          [
            Validators.maxLength(100)
          ]
        ],
        instance_information: [history.state[4] || '']
      });
    this.envParamForm = this.formBuilder.group({});

    this.editor = new Editor();

    setTimeout(() => {
      console.log('now', window?.scrollTo);
      window.scrollTo(0, 0);
    }, 500);
  }

  ngOnDestroy(): void {
    this.editor?.destroy();
  }

  loadEnvParams(): void {
    this.appService.getAppEnvParams(this.selectedVersion.environment_parameters).subscribe({
    next: (res) => { this.environmentParameters = res; },
    complete: () => {this.initEnvParamFormFields(); }
  });
  }


  initEnvParamFormFields(): void {
    let increment=0;
    for (const envParam of this.environmentParameters) {
      envParam.name = envParam.id.valueOf();

      if(!this.envParamForm.contains(envParam.name)) {
        this.entered_values[envParam.name] = envParam.default_value;
        //Validators.required,
          this.envParamForm.addControl(
            envParam.id.valueOf(),
            this.formBuilder.control('', [Validators.minLength(1), Validators.maxLength(Number(envParam.max_length))])
          );
      } else {
        increment++;
        envParam.id = `${envParam.id.valueOf()}${increment}`;
      }
    }
  }

  cancel(): void {
    this.router.navigateByUrl('/applications').then();
  }

  async install(): Promise<void> {
    if (this.installForm.valid && this.envParamForm.valid) {

      // If nothing entered use default values
      for (const envParamName in this.envParamForm.controls){
        if (this.envParamForm.controls[envParamName].value == ""){
          this.envParamForm.controls[envParamName].setValue(this.entered_values[envParamName]);
        }
      }
      const payload = {
        displayname_short: this.installForm.value.instance_title,
        displayname_long: this.installForm.value.instance_subtitle,
        description_short: this.installForm.value.instance_information,
        app: {
          organization: 'bibbox',
          name: this.installForm.value.app_name,
          version: this.installForm.value.version,
          application_documentation_url: this.applicationDocumentationUrl,
          repository_url: this.getRepositoryUrl(this.installForm.value.app_name, this.installForm.value.version),
          install_guide_url: this.installGuideUrl
        },
        parameters: this.envParamForm.value,
        installed_by_id: this.userService.getUserID(),
        installed_by_name: await this.userService.getFullOrUsername()
      };

      this.store.dispatch(new AddInstanceAction(this.installForm.value.instance_id, JSON.stringify(payload)));
      this.router.navigateByUrl('/instances', {state: [this.installForm.value.instance_title, '']}).then();
    }
    else {
      console.log('errors occurred');
      this.validatorService.getFormValidationErrors(this.installForm);
      this.validatorService.getFormValidationErrors(this.envParamForm);
    }
  }

  onRadioChange(selectedValue: string, inputName:string) {
    this.entered_values[inputName] = selectedValue;
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

  getRepositoryUrl(appName: string, version: string) {
    return `https://github.com/bibbox/${appName}/tree/${version}`;
  }
}


