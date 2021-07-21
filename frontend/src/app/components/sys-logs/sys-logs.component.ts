import {Component, OnDestroy, OnInit} from '@angular/core';
import {ActivityService} from '../../store/services/activity.service';
import {ChangeDetectorRef } from '@angular/core';
import {interval, Subscription} from 'rxjs';
import {startWith, switchMap} from 'rxjs/operators';
import {LogItem} from '../../store/models/activity.model';

@Component({
  selector: 'app-sys-logs',
  templateUrl: './sys-logs.component.html',
  styleUrls: ['./sys-logs.component.scss']
})
export class SysLogsComponent implements OnInit, OnDestroy {

  sysLogs = {};
  containerNames = [];
  timeInterval: Subscription = interval(4000).subscribe();
  activeContainerScrollHeight = 0;

  constructor(
    private as: ActivityService,
  ) { }

  ngOnInit(): void {
    this.loadSysContainerLogs();
  }
  ngOnDestroy(): void {
    this.timeInterval.unsubscribe();
  }

  loadSysContainerLogs(): void {
    this.timeInterval = interval(5000)
      .pipe(
        startWith(0),
        switchMap(() => this.as.getSysLogs())
      ).subscribe((res) => {
          this.sysLogs = res;
          this.containerNames = Object.keys(this.sysLogs);
        }
      );
  }

  setScrollHeight(h: number): void {
    this.activeContainerScrollHeight = h;
  }
}
