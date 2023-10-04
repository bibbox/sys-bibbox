import {Component, ElementRef, OnDestroy, OnInit, Renderer2, ViewChild} from '@angular/core';
import {InstanceItem} from '../../../store/models/instance-item.model';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../../store/models/app-state.model';
import {Observable} from 'rxjs';
import {ActivatedRoute, Router} from '@angular/router';
import * as InstanceSelector from '../../../store/selectors/instance.selector';
import {MatSnackBar} from '@angular/material/snack-bar';
import {InstanceService} from '../../../store/services/instance.service';
import {FormBuilder, Validators} from '@angular/forms';
import {SVG_PATHS, toolbar} from '../../../commons';
import {environment} from '../../../../environments/environment';
import {UserService} from '../../../store/services/user.service';
import {DeleteInstanceAction} from '../../../store/actions/instance.actions';
import {Location} from '@angular/common';
import { Editor } from 'ngx-editor';
import { ApplicationService } from '../../../store/services/application.service';
import { AppInfo } from '../../../store/models/application-group-item.model';

@Component({
  selector: 'app-instance-detail-page',
  templateUrl: './instance-detail-page.component.html',
  styleUrls: ['./instance-detail-page.component.scss']
})
export class InstanceDetailPageComponent implements OnInit, OnDestroy {
  tabIndex = 0; // 0: Dashboard, 1: Logs
  instance$: Observable<InstanceItem>;
  instanceItem: InstanceItem;
  instanceNameFromUrl: string;
  baseurl = environment.BASEURL;
  cannotManageInstanceTooltip: string = 'Only admins and instance owners can manage instances.';
  time_of_installation: Date;
  time_of_last_stop: Date;
  isActionsOpen: boolean;
  editor: Editor;
  toolbar = toolbar;
  gotNames: boolean = false;
  appInfo: AppInfo | null;
  activeContainerScrollHeight = 0;
  timeInterval: any;
  refreshIntervals: { [container: string]: any} = {};
  refresh_period: number = 5000;

  @ViewChild('scrollContainer') container: ElementRef;
  scrollTop: number = null;

  instanceLinks = {}; // external Links to GitHub repo
  instanceContainerLogs = {}; // dictionary -> key: containerName, value: logs of container

  svgPaths = SVG_PATHS;

  // form fields for patch request
  instanceDetailForm = this.fb.group({
    displayname_short: ['',
      [
        Validators.required,
        Validators.maxLength(48)
      ]
    ],
    displayname_long: ['',
      [
        Validators.maxLength(96)
      ]
    ],
    description_short: ['', ],
    description_long: ['', ]
  });


  constructor(
    private store: Store<AppState>,
    private route: ActivatedRoute,
    private router: Router,
    private snackbar: MatSnackBar,
    private instanceService: InstanceService,
    private fb: FormBuilder,
    private userService: UserService,
    private _location: Location,
    private elementRef: ElementRef,
    private renderer: Renderer2
  ) {
    // redirect if state is empty -> caused by hard reloading current view
    if (this.router.getCurrentNavigation().extras.state === undefined){
      this.router.navigateByUrl('/instances').then();
    }
    this.tabIndex = this.router.getCurrentNavigation().extras.state.index;

    // TODO: use like this, get instanceName from route
    // if (this.router.getCurrentNavigation().extras.state !== undefined){
    //   this.tabIndex = this.router.getCurrentNavigation().extras.state.index;
    // }
  }

  async ngOnInit(): Promise<void> {
    this.instanceNameFromUrl = this.route.snapshot.paramMap.get('instance_name');
    this.instance$ = this.store.pipe(select(InstanceSelector.selectCurrentInstance, this.instanceNameFromUrl));
    this.instance$.subscribe(
      (instanceItem) => {
        this.instanceItem = instanceItem;

        if (this.instanceItem.time_of_installation) {
          this.time_of_installation = new Date(parseInt(this.instanceItem.time_of_installation) * 1000);
        }
        if (this.instanceItem.last_stop_time) {
          this.time_of_last_stop = new Date(parseInt(this.instanceItem.last_stop_time) * 1000);
        }

        this.loadGithubLinks();
        this.loadContainerLogs();
        this.updateForm();
      });

      // await this.loadAppInfo().then(() => {
        
      // });

      this.editor = new Editor();
  }

  ngOnDestroy(): void {
    this.editor?.destroy();
  }

  updateForm(): void {
    if(!this.gotNames) {
      this.instanceDetailForm.patchValue({
        displayname_long: this.instanceItem.displayname_long,
        displayname_short: this.instanceItem.displayname_short,
        description_long: this.instanceItem.description_long,
        description_short: this.instanceItem.description_short
      });

      this.gotNames = true;
    }
  }

  loadGithubLinks(): void {
    let versionBranch = this.instanceItem.app.version;
    // TODO do we need a special case for development?
    // if (this.instanceItem.app.version === 'development') {
    if (this.instanceItem.app.version === 'latest') {
      versionBranch = 'master';
    }
    // get instance links
    this.instanceLinks = {
      documentation: '',
      repository: 'https://www.github.com/bibbox/',
      installGuide: 'https://www.github.com/bibbox/' + this.instanceItem.app.name + '/blob/' + versionBranch + '/INSTALL-APP.md'
    };
  }

  canManageInstance(): boolean {
    const isAdmin = this.userService.isRole(environment.KEYCLOAK_CONFIG.roles.admin);
    const doesInstanceOwnerMatch = this.userService.getUserID() === this.instanceItem.installed_by_id;

    return isAdmin || doesInstanceOwnerMatch;
  }


  deleteInstance(): void {
    // const isAdmin = this.userService.isRole(KEYCLOAK_ROLES.admin);
    // const doesInstanceOwnerMatch = this.userService.getUserID() === this.instanceItem.installed_by;
    //
    // if (!(isAdmin || doesInstanceOwnerMatch)) {
    //   this.snackbar.open('You are not allowed to delete this instance', 'OK', {duration: 4000});
    //   return;
    // }

    // console.log('delete instance:' + this.instanceItem.instancename);

    this.store.dispatch(new DeleteInstanceAction(this.instanceItem.instancename));

    // this.instanceService.deleteInstance(this.instanceItem.instancename).subscribe(
    //   (res) => console.log(res)
    // );
    this.router.navigateByUrl('/instances').then();
  }

  manageInstance(operation: string): void {
    this.instanceService.manageInstance(this.instanceItem.instancename, operation).subscribe((res) => console.log(res));
  }

  saveInstanceChanges(): void {
    if (this.canManageInstance() === false) {
      this.snackbar.open('You are not allowed to edit this instance', 'OK', {duration: 4000});
      return;
    }

    // this.snackbar.open(JSON.stringify(this.instanceDetailForm.value) + this.instanceDetailForm.valid, 'OK', {duration: 4000});
    this.snackbar.open('Changes saved', 'OK', {duration: 20000});

    if (this.instanceDetailForm.valid) {
      this.instanceService.updateInstanceDescription(this.instanceItem.instancename, JSON.stringify(this.instanceDetailForm.value))
        .subscribe(
        (res) => console.log(res)
      );
    }
  }

  backClicked(): void {
    this._location.back();
  }

  toggle() {
    this.isActionsOpen = !this.isActionsOpen;
  }

  loadContainerLogs(): void {
    this.instanceService.getInstanceContainerLogs(this.instanceItem.instancename).subscribe(
      (res: JSON) => {
        this.instanceContainerLogs = res;
      }
    );

    // Scroll to the bottom of the log container element
    setTimeout(() => {
      const logContainer = this.elementRef.nativeElement.querySelector('.logs');
      this.renderer.setProperty(logContainer, 'scrollTop', logContainer.scrollHeight);
    }, 0);
  }

  clearRefreshInterval(containerName: string): void {
    const interval = this.refreshIntervals[containerName];
    if (interval) {
      clearInterval(interval);
      delete this.refreshIntervals[containerName];
    }
  }

  periodicallyRefresh(containerName: string): void {
    // this.stopPeriodicRefresh();

    // Initial call to loadContainerLogs
    this.loadContainerLogs();

    // clear interval if it exists
    this.clearRefreshInterval(containerName);

    // Set interval to refresh every 5 seconds
    const interval = setInterval(() => {
      this.loadContainerLogs();
    }, this.refresh_period);

    // Save the interval in the refreshIntervals object
    this.refreshIntervals[containerName] = interval;
  }

  stopPeriodicRefresh(containername: string): void {
    this.clearRefreshInterval(containername);
  }

  setScrollHeight(h: number): void {
    this.activeContainerScrollHeight = h;
  }
}
