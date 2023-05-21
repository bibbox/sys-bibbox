import {Component, ElementRef, OnDestroy, OnInit, Renderer2} from '@angular/core';
import {ActivityService} from '../../store/services/activity.service';
import {ChangeDetectorRef } from '@angular/core';
import {interval, Subscription} from 'rxjs';
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
  timeInterval: Subscription = interval(4000).subscribe();
  activeContainerScrollHeight = 0;

  constructor(
    private as: ActivityService,
    private elementRef: ElementRef,
    private renderer: Renderer2,
  ) { }

  ngOnInit(): void {
    this.loadContainerNames();
  }
  ngOnDestroy(): void {
    this.timeInterval.unsubscribe();
    this.sysLogs = [];
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

  periodicallyRefresh(containerName: string): void {
    const refresh_period = 5000;
    // Initial call to loadContainerLogs
    this.loadContainerLogs(containerName);

    // Set interval to refresh every 5 seconds
    setInterval(() => {
      this.loadContainerLogs(containerName);
    }, refresh_period);
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
