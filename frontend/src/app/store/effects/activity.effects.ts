import {Injectable} from '@angular/core';
import {Actions, createEffect, ofType} from '@ngrx/effects';
import {
  ActivityActionTypes,
  LoadActivitiesAction, LoadActivitiesSuccessAction, LoadActivitiesFailureAction
} from '../actions/activity.actions';
import {catchError, map, mergeMap} from 'rxjs/operators';
import {ActivityService} from '../services/activity.service';
import {of} from 'rxjs';

@Injectable()
export class ActivityEffects {

  loadActivities$ =  createEffect(() =>
    this.actions$.pipe(
      ofType<LoadActivitiesAction>(ActivityActionTypes.LOAD_ACTIVITIES),
      mergeMap(
        () => this.activityService.getActivities()
          .pipe(
            map(data => new LoadActivitiesSuccessAction(data)),
            catchError(error => of(new LoadActivitiesFailureAction(error)))
          )
      )
    )
  );

  constructor(private actions$: Actions, private activityService: ActivityService) {

  }

}
