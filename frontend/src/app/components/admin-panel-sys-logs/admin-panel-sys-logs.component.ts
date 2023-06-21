import {Component, ElementRef, OnDestroy, OnInit, Renderer2} from '@angular/core';
import {ActivityService} from '../../store/services/activity.service';
import {ChangeDetectorRef } from '@angular/core';
import {interval, Subscription, TimeInterval} from 'rxjs';
import {startWith, switchMap} from 'rxjs/operators';
import {LogItem, SysContainerLogs, SysContainerNames} from '../../store/models/activity.model';

@Component({
  selector: 'app-sys-logs',
  templateUrl: './admin-panel-sys-logs.component.html',
  styleUrls: ['./admin-panel-sys-logs.component.scss']
})
export class AdminPanelSysLogsComponent implements OnInit, OnDestroy {

  sysLogs = {};
  containerNames: string[];
  activeContainerScrollHeight = 0;

  timeInterval: any;
  refreshIntervals: { [container: string]: any} = {};
  refresh_period: number = 5000;

  constructor(
    private as: ActivityService,
    private elementRef: ElementRef,
    private renderer: Renderer2,
  ) { }

  ngOnInit(): void {
    this.loadContainerNames();
  }

  ngOnDestroy(): void {
    for (const containerName in this.refreshIntervals) {
      this.clearRefreshInterval(containerName);
    }
  }

  loadContainerNames(): void {
    this.as.getNamesOfSysContainers().subscribe(
      (res: SysContainerNames) => {
        this.containerNames = res.names;
      }
    )
  }

  loadContainerLogs(containerName: string): void {
    this.as.getSysLogsOfContainer(containerName).subscribe(
      (res: SysContainerLogs) => {
        this.sysLogs[containerName] = res.logs;
        // Update the value in the containerNames array if necessary
        const index = this.containerNames.findIndex(name => name === containerName);
        if (index !== -1) {
          this.containerNames[index] = containerName; // Update with the new value if needed
        }
        // Scroll to the bottom of the log container element
        const logContainer = this.elementRef.nativeElement.querySelector('.sys-container-log-item__container');
        this.renderer.setProperty(logContainer, 'scrollTop', logContainer.scrollHeight);
      }
    )
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
    this.loadContainerLogs(containerName);

    // clear interval if it exists
    this.clearRefreshInterval(containerName);

    // Set interval to refresh every 5 seconds
    const interval = setInterval(() => {
      this.loadContainerLogs(containerName);
    }, this.refresh_period);

    // Save the interval in the refreshIntervals object
    this.refreshIntervals[containerName] = interval;
  }

  stopPeriodicRefresh(containername: string): void {
    this.clearRefreshInterval(containername);
  }


  // loadSysContainerLogs(): void {
  //   this.timeInterval = interval(5000)
  //     .pipe(
  //       startWith(0),
  //       switchMap(() => this.as.getSysLogs())
  //     ).subscribe((res) => {
  //         this.sysLogs = res;
  //         this.containerNames = Object.keys(this.sysLogs);
  //       }
  //     );
  // }

  setScrollHeight(h: number): void {
    this.activeContainerScrollHeight = h;
  }
}
