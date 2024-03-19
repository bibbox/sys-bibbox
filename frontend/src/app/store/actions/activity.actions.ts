import {Action} from '@ngrx/store';
import {ActivityItem, IActivityFilters} from '../models/activity.model';

export enum ActivityActionTypes {
  LOAD_ACTIVITIES = '[ACTIVITY] Load Activities',
  LOAD_ACTIVITIES_SUCCESS = '[ACTIVITY] Load Activities Success',
  LOAD_ACTIVITIES_FAILURE = '[ACTIVITY] Load Activities Failure',
  UPDATE_ACTIVITIES_FILTERS = '[ACTIVITY] Update Activity filters'
}

export class LoadActivitiesAction implements Action {
  readonly type = ActivityActionTypes.LOAD_ACTIVITIES;
}


export class LoadActivitiesSuccessAction implements Action {
  readonly type = ActivityActionTypes.LOAD_ACTIVITIES_SUCCESS;
  constructor(public payload: ActivityItem[]) {
  //  console.log('LoadActivitiesSuccessAction');
  }
}


export class LoadActivitiesFailureAction implements Action {
  readonly type = ActivityActionTypes.LOAD_ACTIVITIES_FAILURE;
  constructor(public payload: Error) {
  //  console.log('LoadActivitiesFailureAction');
  }
}

export class UpdateActivityFiltersAction implements Action {
  readonly type = ActivityActionTypes.UPDATE_ACTIVITIES_FILTERS;

  constructor(public payload: IActivityFilters) {}
}


export type ActivityAction =
  LoadActivitiesAction
  | LoadActivitiesSuccessAction
  | LoadActivitiesFailureAction
  | UpdateActivityFiltersAction;
