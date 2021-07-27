import {Action} from '@ngrx/store';
import {ActivityItem} from '../models/activity.model';

export enum ActivityActionTypes {
  LOAD_ACTIVITIES = '[ACTIVITY] Load Activities',
  LOAD_ACTIVITIES_SUCCESS = '[ACTIVITY] Load Activities Success',
  LOAD_ACTIVITIES_FAILURE = '[ACTIVITY] Load Activities Failure',
}

export class LoadActivitiesAction implements Action {
  readonly type = ActivityActionTypes.LOAD_ACTIVITIES;
}


export class LoadActivitiesSuccessAction implements Action {
  readonly type = ActivityActionTypes.LOAD_ACTIVITIES_SUCCESS;
  constructor(public payload: ActivityItem[]) {}
}


export class LoadActivitiesFailureAction implements Action {
  readonly type = ActivityActionTypes.LOAD_ACTIVITIES_FAILURE;
  constructor(public payload: Error) {}
}

export type ActivityAction =
  LoadActivitiesAction
  | LoadActivitiesSuccessAction
  | LoadActivitiesFailureAction;
