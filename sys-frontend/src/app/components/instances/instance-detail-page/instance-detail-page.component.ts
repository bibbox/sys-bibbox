import {Component, OnInit} from '@angular/core';
import {InstanceItem} from '../../../store/models/instance-item.model';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../../store/models/app-state.model';
import {Observable} from 'rxjs';
import {ActivatedRoute, Router} from '@angular/router';
import * as InstanceSelector from '../../../store/selectors/instance.selector';
import {MatSnackBar} from '@angular/material/snack-bar';
import {InstanceService} from '../../../store/services/instance.service';

@Component({
  selector: 'app-instance-detail-page',
  templateUrl: './instance-detail-page.component.html',
  styleUrls: ['./instance-detail-page.component.scss']
})
export class InstanceDetailPageComponent implements OnInit {
  tabIndex = 0;
  instance$: Observable<InstanceItem>;
  instanceItem: InstanceItem;
  instanceName: string;

  instanceLinks = [];
  instanceContainerNames = [];
  instanceContainerLogs = {}; // TODO

  instanceNameShort: string;
  instanceNameLong: string;
  instanceDescriptionShort: string;
  instanceDescriptionLong: string;

  constructor(
    private store: Store<AppState>,
    private route: ActivatedRoute,
    private router: Router,
    private snackbar: MatSnackBar,
    private instanceService: InstanceService
  ) {
    // redirect if state is empty -> caused by hard reloading current view
    if (this.router.getCurrentNavigation().extras.state === undefined){
      this.router.navigateByUrl('/instances').then();
    }
    this.tabIndex = this.router.getCurrentNavigation().extras.state.index;
  }

  ngOnInit(): void {

    this.instanceName = this.route.snapshot.paramMap.get('instance_name');
    this.instance$ = this.store.pipe(select(InstanceSelector.selectCurrentInstance, this.instanceName));
    this.instance$.subscribe(
      (instanceItem) => {
        this.instanceItem = instanceItem;
        this.loadGithubLinks();
        this.loadContainerNames();
        this.instanceNameLong = instanceItem.short_description;
        this.instanceNameShort = instanceItem.displayname;
      });
  }

  loadGithubLinks(): void {
    // get instance links
    this.instanceLinks = [
      { label: 'GitHub Repository:',
        url: 'https://www.github.com/bibbox/'
          + this.instanceItem.app.name},
      { label: 'Install Instructions:',
        url: 'https://www.github.com/bibbox/'
          + this.instanceItem.app.name
          + '/blob/'
          + this.instanceItem.app.version
          + '/INSTALL-APP.md', }
    ];
  }

  loadContainerNames(): void {
    // get container names of instance
    for (const entry of this.instanceItem.proxy) {

      // remove portinfo
      const containerName = entry.CONTAINER.replace(/:[0-9]+/, '');
      this.instanceContainerNames.push(containerName);
    }
  }

  deleteInstance(): void {
    console.log('delete instance:' + this.instanceItem.instancename);
    this.instanceService.deleteInstance(this.instanceItem.instancename).subscribe(
      (res: JSON) => console.log(res)
    );
    this.router.navigateByUrl('/instances').then();
  }

  startInstance(): void {
    console.log('startInstance ' + this.instanceItem.instancename);
  }

  saveInstanceChanges(): void {
    console.log('save instance changes');
    this.snackbar.open(JSON.stringify(this.instanceItem), 'OK', {horizontalPosition: 'center', verticalPosition: 'bottom'});
  }
}
