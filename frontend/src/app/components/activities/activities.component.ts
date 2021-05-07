import {Component, OnInit} from '@angular/core';
import {SVG_PATHS} from '../../commons';
import {ActivityService} from '../../store/services/activity.service';
import {ActivityItem, LogItem} from '../../store/models/activity.model';
import {ActivatedRoute} from '@angular/router';
import {Subject} from 'rxjs';

@Component({
  selector: 'app-activities',
  templateUrl: './activities.component.html',
  styleUrls: ['./activities.component.scss']
})
export class ActivitiesComponent implements OnInit {

  focussedActivityID: Subject<number> = this.route.snapshot.params?.activityID || 0;

  svgPaths = SVG_PATHS;
  activityStates = {
    finished : 'assets/done.png',
    error: 'assets/error.png',
    ongoing: 'assets/loading.gif'
  };
  activityList: ActivityItem[] = [];
  activityLogs: LogItem[] = [];
  constructor(
    private activityService: ActivityService,
    private route: ActivatedRoute) {}

  ngOnInit(): void {
    console.log('focussed activity: ', this.focussedActivityID);
    this.getActivities();
  }

  getActivities(): void {
    this.activityService.getActivities().subscribe(
      (res) => this.activityList = res
    );
    // this.activityList.sort((a, b) => (a.id < b.id) ? 1 : -1);
  }

  getLogsOfActivity(activityID: number): void {
    this.activityService.getLogsOfActivity(activityID).subscribe(
      (res) => this.activityLogs = res
    );
  }
}
