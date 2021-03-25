import {Component, OnInit} from '@angular/core';
import {APP_TITLE_LONG} from '../../commons';
import {HttpClient} from '@angular/common/http';
import {Store} from '@ngrx/store';
import {InstanceService} from '../../store/services/instance.service';
import {ApplicationService} from '../../store/services/application.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = APP_TITLE_LONG;

  constructor(
    private http: HttpClient,
    private store: Store<{AppState}>,
    private readonly instanceService: InstanceService,
    private readonly applicationService: ApplicationService) { }

  ngOnInit(): void {
    this.instanceService.loadInstances();
    this.applicationService.loadApplications();
  }
}
